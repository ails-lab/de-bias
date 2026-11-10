# Build from the repository root (deploy/compose.yaml does this):
#
#   docker build -f deploy/Dockerfile -t de-bias .
#
# GPU: torch 2.1.2 from PyPI bundles the CUDA 12.1 runtime, so no CUDA base image is needed.

FROM python:3.10-slim-bookworm AS deps

RUN pip install --no-cache-dir uv==0.13.5

ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_PYTHON_DOWNLOADS=never \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH=/opt/venv/bin:$PATH

WORKDIR /app

COPY pyproject.toml uv.lock /app/
RUN uv sync --locked --no-install-project --no-cache


# Downloads the pinned models, regenerates the *_customized.pt lemma models and checks every file's
# sha256. Only models/ and model_preprocessing/ are copied in, so code changes don't redownload.
# version.txt marks the cache as current: otherwise transformers tries to migrate it on every start
# and, since the app can't write to /models, logs a warning that loading will fail.
FROM deps AS models

COPY models/ /app/models/
COPY model_preprocessing/ /app/model_preprocessing/
RUN python models/fetch_models.py /models \
    && echo 1 > /models/huggingface/hub/version.txt


FROM deps

ENV PYTHONUNBUFFERED=1 \
    STANZA_RESOURCES_DIR=/models \
    HF_HOME=/models/huggingface \
    HF_HUB_OFFLINE=1 \
    VOCABULARIES_PATH=/app/vocabularies \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility

RUN useradd --system --uid 10001 --create-home --home-dir /home/app app

COPY --from=models /models /models
COPY vocabularies/ /app/vocabularies/
COPY src/ /app/src/

USER app

EXPOSE 8000

HEALTHCHECK --start-period=5m --interval=30s --timeout=10s --retries=5 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/openapi.json', timeout=8)"]

CMD ["python", "-m", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
