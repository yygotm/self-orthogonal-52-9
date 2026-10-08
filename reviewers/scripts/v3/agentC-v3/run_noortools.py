# Run a script with OR-Tools made unimportable (sys.modules['ortools']=None).
import sys, runpy, os
sys.modules['ortools']=None
script=os.path.abspath(sys.argv[1]); sys.argv=sys.argv[1:]
sys.path.insert(0, os.path.dirname(script))
runpy.run_path(script, run_name='__main__')
