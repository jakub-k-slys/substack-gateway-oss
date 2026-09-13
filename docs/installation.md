# Installation

## Requirements

- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/)
- Substack credentials if you plan to use authenticated endpoints

## Install Dependencies

This repository is a uv workspace; install every member (the shell,
`gateway_core`, and every domain trio) from the repository root:

```bash
uv sync --all-packages --dev
```

## Run the Gateway

Start the application locally:

```bash
uv run python -m substack_gateway.main
```

By default the app listens on `http://0.0.0.0:5001`.

## Smoke Test

Check the root metadata endpoint:

```bash
curl http://127.0.0.1:5001/
```

Check the public liveness probe:

```bash
curl http://127.0.0.1:5001/api/v1/health/live
```
