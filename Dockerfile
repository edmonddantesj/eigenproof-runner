FROM python:3.11-slim

WORKDIR /app

COPY runner.py /app/runner.py
COPY sample_input.json /app/sample_input.json

RUN python -V

ENTRYPOINT ["python","/app/runner.py"]
