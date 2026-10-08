FROM python:3.12-slim
RUN pip install --no-cache-dir ortools==9.12.4544 pynauty==2.8.8.1
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc6-dev && rm -rf /var/lib/apt/lists/*
