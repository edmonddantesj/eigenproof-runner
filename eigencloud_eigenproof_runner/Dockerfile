FROM python:3.11-slim

ARG GIT_COMMIT=
ENV GIT_COMMIT=${GIT_COMMIT}

WORKDIR /app

COPY runner.py /app/runner.py
COPY sample_input.json /app/sample_input.json
COPY policy.json /app/policy.json

RUN python -V

ENTRYPOINT ["python","/app/runner.py"]
