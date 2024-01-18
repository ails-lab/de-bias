FROM ai4culture.docker.ails.ece.ntua.gr/debias-base:latest

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

CMD python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000