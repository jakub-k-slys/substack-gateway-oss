# Substack Gateway OSS

[![CI](https://github.com/jakub-k-slys/substack-gateway-oss/actions/workflows/ci.yaml/badge.svg)](https://github.com/jakub-k-slys/substack-gateway-oss/actions/workflows/ci.yaml)
[![E2E Tests](https://github.com/jakub-k-slys/substack-gateway-oss/actions/workflows/e2e.yaml/badge.svg)](https://github.com/jakub-k-slys/substack-gateway-oss/actions/workflows/e2e.yaml)
[![Deployed on Vercel](https://img.shields.io/badge/deployed%20on-Vercel-000000?logo=vercel)](https://substack-gateway.vercel.app)

A stateless Python gateway for [Substack](https://substack.com) that exposes
a REST API and an MCP server on top of the same service layer.

Designed to make Substack data and actions accessible from scripts,
applications, and AI tooling — without duplicating integration logic across
different interfaces.

## What You Can Do

- Read public Substack profiles, posts, notes, and comments
- Access authenticated `me` endpoints with a base64-encoded credential token
- Create and delete notes through the REST API
- Use the same gateway as an MCP server for AI tools and agent workflows
- Extend the app with custom routes, MCP tools, auth providers, and lifespan
  hooks

## Interfaces

- **REST API** at `/api/v1/*`
- **MCP server** at `/mcp`

Both share the same service layer and HTTP clients.

## Quickstart

Requirements:

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

Install dependencies:

```bash
uv sync --dev
```

Run the application locally:

```bash
uv run python -m gateway_oss.main
```

Check the root metadata endpoint:

```bash
curl http://127.0.0.1:5001/
```

Check the liveness probe:

```bash
curl http://127.0.0.1:5001/api/v1/health/live
```

Fetch a public profile:

```bash
curl http://127.0.0.1:5001/api/v1/profiles/<slug>
```

## REST Example

Public profile lookup:

```bash
curl http://127.0.0.1:5001/api/v1/profiles/<slug>
```

Authenticated request:

```bash
curl \
  -H "x-gateway-token: <base64-encoded-json>" \
  http://127.0.0.1:5001/api/v1/me
```

The REST API is mounted under `/api/v1` and includes endpoints for health,
profiles, posts, notes, comments, and authenticated `me` operations.

## Authentication

Gateway access and Substack access are separate concerns.

For this OSS repository, Substack credentials are passed as a base64-encoded
JSON object. REST requests send that value as the `x-gateway-token` header.

Credential shape:

```json
{
  "publication_url": "https://example.substack.com",
  "substack_sid": "s%3A...",
  "connect_sid": "s%3A..."
}
```

Encode it with:

```bash
echo '{"publication_url":"https://example.substack.com","substack_sid":"s%3A...","connect_sid":"s%3A..."}' | base64
```

Treat `substack_sid` and `connect_sid` as bearer credentials. Do not commit
real values to the repository.

## MCP

The MCP server is mounted at `/mcp` and served over streamable HTTP.

Public OSS MCP tools include:

- `get_note`
- `get_post`
- `get_post_comments`
- `get_profile`
- `get_profile_posts`
- `get_profile_notes`

## Project Layout

Core application code lives in `src/gateway_oss/`.

- `api/v1/`: FastAPI route handlers
- `mcp/`: FastMCP tool surface and transport integration
- `services/`: shared business logic
- `client/`: Substack HTTP client wrappers
- `models/`: schemas and pagination models
- `converters/`: Markdown conversion
- `extensions/`: runtime extension hooks

## Configuration

Application settings are environment-driven via the `SUBSTACK_GATEWAY_` prefix.

Common examples include:

- `SUBSTACK_GATEWAY_LOG_LEVEL`
- `SUBSTACK_GATEWAY_SUBSTACK_BASE_URL`
- `SUBSTACK_GATEWAY_SUBSTACK_TIMEOUT_SEC`

## Validation

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check .
uv build
uv run pytest tests/
uv run behave features/
```

## Documentation

The repository includes MkDocs and Read the Docs configuration:

- [Docs home](docs/index.md)
- [Introduction](docs/introduction.md)
- [Installation guide](docs/installation.md)
- [Authentication](docs/authentication.md)
- [API reference](docs/api-reference.md)
- [MCP documentation](docs/mcp.md)
- [Development guide](docs/development.md)
- [Contributing guide](CONTRIBUTING.md)

Read the Docs can build the site directly from `.readthedocs.yaml` and `mkdocs.yml`.

## Author

Built by [Jakub Slys](https://iam.slys.dev) — Backend Engineer building
distributed systems for telecoms, running a self-hosted Kubernetes homelab,
and building AI automation pipelines with n8n, MCP, and Claude.

This gateway is the backend I use to automate my own Substack at
[iam.slys.dev](https://iam.slys.dev), where I write about system design,
machine learning fundamentals, and the AI tools I actually build and run
in production.

If you want to understand how this gateway works under the hood — the
architecture decisions, what I got wrong the first time, and how it fits
into a full content automation stack — that's what the newsletter is for.

→ [iam.slys.dev](https://iam.slys.dev)
