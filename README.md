# Substack Gateway OSS

[![CI](https://github.com/jakub-k-slys/substack-gateway-oss/actions/workflows/ci.yml/badge.svg)](https://github.com/jakub-k-slys/substack-gateway-oss/actions/workflows/ci.yml)
[![E2E Tests](https://github.com/jakub-k-slys/substack-gateway-oss/actions/workflows/e2e.yml/badge.svg)](https://github.com/jakub-k-slys/substack-gateway-oss/actions/workflows/e2e.yml)
[![Deployed on Vercel](https://img.shields.io/badge/deployed%20on-Vercel-000000?logo=vercel)](https://substack-gateway.vercel.app)

A stateless Python gateway for [Substack](https://substack.com) that exposes
a REST API and an MCP server on top of the same service layer.

Designed to make Substack data and actions accessible from scripts,
applications, and AI tooling — without duplicating integration logic across
different interfaces.

## What You Can Do

- Read Substack profiles, posts, notes, comments, drafts, and publication /
  post analytics
- Create, update, and delete notes, comments, and drafts
- Access authenticated `me` endpoints and MCP tools with a base64-encoded
  credential token
- Use the same gateway as a REST API or an MCP server for AI tools and agent
  workflows
- Extend the app with custom routes, MCP tools, auth providers, credential
  resolvers, and lifespan hooks

## Interfaces

- **REST API** at `/api/v1/*`
- **MCP server** at `/mcp`

Both share the same `gateway_core` HTTP clients and config. The thin
`substack_gateway` shell package assembles the application (REST + MCP
composition) from per-domain packages — notes, posts, profiles, following,
comments, me, drafts, and stats — each published as a capability, while
`gateway_oss` provides health routes and the extension surface.

## Quickstart

Requirements:

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

Install dependencies:

```bash
uv sync --all-packages --dev
```

Run the application locally:

```bash
uv run python -m substack_gateway.main
```

Check the root metadata endpoint:

```bash
curl http://127.0.0.1:5001/
```

Check the liveness probe:

```bash
curl http://127.0.0.1:5001/api/v1/health/live
```

Fetch a profile (every `/api/v1` route except `/health/live` requires the
`x-gateway-token` header, even for reads over public Substack data — see
[Authentication](docs/authentication.md)):

```bash
curl \
  -H "x-gateway-token: <base64-encoded-json>" \
  http://127.0.0.1:5001/api/v1/profiles/<slug>
```

## REST Example

Profile lookup:

```bash
curl \
  -H "x-gateway-token: <base64-encoded-json>" \
  http://127.0.0.1:5001/api/v1/profiles/<slug>
```

`me`:

```bash
curl \
  -H "x-gateway-token: <base64-encoded-json>" \
  http://127.0.0.1:5001/api/v1/me
```

The REST API is mounted under `/api/v1` and includes 45 endpoints across
health, profiles, posts, notes, comments, drafts, publication/post
analytics, following, and `me` — see the full
[API reference](docs/api-reference.md).

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

The MCP server is mounted at `/mcp` and served over streamable HTTP. It
exposes 43 tools across the same domains as the REST API — see the full
[MCP reference](docs/mcp.md).

Every tool takes an optional `token` argument carrying the same
base64-encoded credentials as `x-gateway-token`; when omitted, the gateway
asks an installed credential resolver (this repository installs none, so an
omitted token raises an error telling the caller to pass one). Only the
three `profiles` tools need no credentials at all:

- `get_profile`
- `get_profile_posts`
- `get_profile_notes`

## Project Layout

The root `src/substack_gateway/` package composes the app (`app_factory.py`,
`api_app.py`, `mcp_app.py`, `registry.py`). `packages/gateway_core/` is the
shared foundation: auth, HTTP clients, config, converters, and models. Each
domain ships as a trio of packages:

- `gateway_<domain>/`: service layer
- `gateway_<domain>_rest/`: FastAPI router, published as a capability
- `gateway_<domain>_mcp/`: FastMCP tools, published as a capability

`packages/gateway_oss/` provides health routes, the extension protocol, and
versioning.

## Configuration

Application settings are environment-driven via the `SUBSTACK_GATEWAY_` prefix.

Common examples include:

- `SUBSTACK_GATEWAY_LOG_LEVEL`
- `SUBSTACK_GATEWAY_SUBSTACK_BASE_URL`
- `SUBSTACK_GATEWAY_SUBSTACK_TIMEOUT_SEC`
- `SUBSTACK_GATEWAY_STATS_TIMESERIES_WATERMARK_LAG_DAYS` (default `2`)

OSS performs no caching; an extension may install one.

## Validation

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check .
uv build --all-packages
uv run pytest
uv run behave packages/gateway_oss/features/
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
