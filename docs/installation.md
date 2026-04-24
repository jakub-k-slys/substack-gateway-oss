# Installation

## Requirements

- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/)
- Substack credentials if you plan to use authenticated endpoints

## Install Dependencies

From the repository root:

```bash
uv sync --dev
```

## Run the Gateway

Start the application locally:

```bash
uv run python -m gateway_oss.main
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

## Read the Docs

This repository includes:

- `mkdocs.yml` for MkDocs site configuration
- `.readthedocs.yaml` for Read the Docs build configuration
- `docs/requirements.txt` for documentation-only dependencies

If you connect the repository to Read the Docs, it can build the site directly from those files.
