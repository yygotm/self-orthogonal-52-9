"""Bounded regression tests for v3.1's full-run success gate (no scans)."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from reproduce import ROOT, prepare_classification, verify_classification

OUTPUTS=['normalized36-classification.json','normalized36-second-rows-0.json',
         'normalized32-orbits.json','normalized32-classification.json',
         'exact36-results.json','exact40-results.json']


class ClassificationGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='.v31-gate-',dir=ROOT)
        if not Path(self.tmp.name).resolve().is_relative_to(ROOT.resolve()):
            raise RuntimeError('temporary test directory must be inside the package')
        self.addCleanup(self.tmp.cleanup)
        self.work=Path(self.tmp.name)
        self.data={name:json.loads((ROOT/name).read_text(encoding='utf-8')) for name in OUTPUTS}

    def write(self):
        for name,data in self.data.items():
            (self.work/name).write_text(json.dumps(data),encoding='utf-8')

    def test_archived_positive(self):
        self.write()
        result=verify_classification(self.work)
        self.assertEqual(result['normalized36']['classes'],1)
        self.assertEqual(result['normalized32']['classes'],1)

    def test_counterexamples_rejected(self):
        def split_classes(d,key):
            group=d[key][0]
            d[key]=[group[:1],group[1:]]
        mutations=[
            ('36 extra orbit','normalized36-classification.json',
             lambda d:d['first_orbits'].append(copy.deepcopy(d['first_orbits'][0]))),
            ('36 missing classes','normalized36-classification.json',
             lambda d:d['kernels'][0].pop('classes')),
            ('36 two classes','normalized36-classification.json',
             lambda d:split_classes(d['kernels'][0],'classes')),
            ('36 duplicate member','normalized36-classification.json',
             lambda d:d['kernels'][0]['classes'][0].__setitem__(0,d['kernels'][0]['classes'][0][1])),
            ('32 extra orbit','normalized32-orbits.json',
             lambda d:d['orbits'].append(copy.deepcopy(d['orbits'][0]))),
            ('32 two classes','normalized32-classification.json',
             lambda d:split_classes(d,'equivalence_classes')),
            ('32 missing candidate','normalized32-classification.json',
             lambda d:d['second_rows'].pop()),
            ('36 wrong candidate total','exact36-results.json',
             lambda d:d[0].__setitem__('enumerated',d[0]['enumerated']+1)),
            ('36 unknown status','exact36-results.json',
             lambda d:d[0].__setitem__('status','UNKNOWN')),
            ('40 unexpected solution','exact40-results.json',
             lambda d:d[0]['cases'][0].__setitem__('valid',1)),
        ]
        baseline=copy.deepcopy(self.data)
        for label,name,mutate in mutations:
            with self.subTest(label=label):
                self.data=copy.deepcopy(baseline)
                mutate(self.data[name]); self.write()
                with self.assertRaises((ValueError,KeyError)):
                    verify_classification(self.work)

    def test_missing_output_rejected(self):
        self.write()
        (self.work/'normalized36-classification.json').unlink()
        with self.assertRaises(FileNotFoundError):
            verify_classification(self.work)

    def test_fresh_stage_has_only_code_and_inputs(self):
        staged=self.work/'fresh'
        names=prepare_classification(staged)
        self.assertTrue(all(Path(name).suffix=='.py' or name.startswith('residual16-')
                            for name in names))
        self.assertFalse(list(staged.glob('*.json')))
        self.assertFalse(list(staged.glob('normalized*txt')))
        with self.assertRaises(FileNotFoundError):
            verify_classification(staged)


if __name__=='__main__':
    unittest.main(verbosity=2)
