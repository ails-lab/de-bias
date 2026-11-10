## Requirements

- Docker Engine with the Compose plugin (`docker compose version`).
- NVIDIA Container Toolkit set up for Docker. If it isn't yet:
  ```bash
  sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker
  ```
  To check that containers can see the GPUs:
  ```bash
  docker run --rm --gpus all ubuntu nvidia-smi
  ```
- An OpenAI-compatible LLM server reachable from the container. The API calls its
 `/v1/chat/completions` endpoint for ambiguous terms.
- For the build only: outbound HTTPS to `pypi.org`, `files.pythonhosted.org` and `huggingface.co`,
  about 7 GB of downloads. The finished image is about 10 GB.
- One GPU. The models (ELECTRA-large, CamemBERT-large and smaller ones for five languages) need a
  few GB of GPU memory. No CUDA install is needed in the image.

## First start

```bash
git clone https://github.com/ails-lab/de-bias.git
cd de-bias/deploy
cp .env.example .env
```

Edit `.env` and set at least `LLM_ENDPOINT`. Then build and start:

```bash
docker compose up -d --build
```

The first build takes a while (it downloads and checks all models). After the container starts, it
loads the five language pipelines onto the GPU before it answers requests, which takes a minute or
two. Wait until `docker compose ps` shows the container as `healthy`, then test it:

```bash
curl -s localhost:8000/simple -H 'Content-Type: application/json' \
  -d '{"language": "nl", "values": ["Enigszins geopende mond, kleine kin, spleetogen"], "useNER": true, "useLLM": false}'
```

To check that the LLM connection works, send the same request with `"useLLM":true`.

To confirm that the API is using the GPU:

```bash
docker compose exec debias python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

## Settings (`.env`)

| Variable | Default                       | Meaning |
|---|-------------------------------|---|
| `LLM_ENDPOINT` | (required for `useLLM: true`) | Base URL of the LLM server, without `/v1` |
| `LLM_MODEL` | empty                         | Model name to request; empty uses the model the server serves |
| `DEBIAS_GPU` | `0`                           | GPU index, as in `nvidia-smi` |
| `DEBIAS_HOST_ADDR` | `0.0.0.0`                     | Host address the API is published on |
| `DEBIAS_HOST_PORT` | `8000`                        | Host port the API is published on |

