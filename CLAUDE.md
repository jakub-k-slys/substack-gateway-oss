# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies (dev included)
uv sync --dev

# Run the server (dev mode with reload)
uv run python -m gateway_oss.main

# Lint
uv run ruff check .

# Format check / fix
uv run ruff format --check .
uv run ruff format .

# Type-check
uv run ty check .

# Unit tests (pytest)
uv run pytest tests/

# Run a single test file
uv run pytest tests/test_markdown.py

# BDD integration tests (behave)
uv run behave features/

# Run a single feature file
uv run behave features/api/notes.feature

# Build the package
uv build
```

When introducing changes, validate them before finishing the task. Prefer targeted runs first, but the expected OSS validation set is:
- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run ty check .`
- `uv build`
- `uv run pytest tests/`
- `uv run behave features/`

## Architecture

This is a **Starlette-based gateway** that wraps the Substack private API and exposes two interfaces:

- **`/api/v1/*`** — a FastAPI REST API (`src/gateway_oss/api/`)
- **`/mcp`** — a FastMCP MCP server (`src/gateway_oss/mcp/`)

Both share the same service layer and HTTP clients, wired together by `app_factory.py`.

### Request flow

```
Client request
  → Starlette app (app_factory.py)
    → /api/v1/* → FastAPI (api/app.py) → deps.py → Services → HTTP clients
    → /mcp      → FastMCP (mcp/app.py) → mcp/deps.py → Services → HTTP clients
```

### Authentication

Requests carry a **base64-encoded JSON Bearer token** containing `publication_url`, `substack_sid`, and `connect_sid` (Substack session cookies plus the target publication URL). The `auth.py` module decodes this token; `api/deps.py` and `mcp/deps.py` use it to construct per-request HTTP clients.

The MCP layer has a second path: if OAuth is active (all three of `SUBSTACK_GATEWAY_BASE_URL`, `SUBSTACK_GATEWAY_DATABASE_URL`, `SUBSTACK_GATEWAY_JWT_SECRET` are set), `mcp/deps.py` will look up credentials via the `CredentialProvider` interface instead of reading request headers.

### HTTP clients

- `SubstackHTTPBase` (`client/base.py`) — shared async httpx layer, raises `SubstackAuthError` (401/403) or `SubstackAPIError` (all other failures).
- `SubstackClient` — talks to `https://substack.com/api/v1/*` (global API: user settings, handles, profiles, following).
- `PublicationClient` (`client/publication.py`) — talks to a per-publication subdomain URL (notes, posts, comments). The publication URL comes from the Bearer token's `publication_url` field.

Most API endpoints need **both** clients; `ProfilesService` only needs `SubstackClient`.

### Services

`services/` contains thin domain classes (`NotesService`, `PostsService`, `ProfilesService`, `FollowingService`) that coordinate calls across the two HTTP clients. They are instantiated per-request via FastAPI/FastMCP dependency injection.

### Models

- `models/substack.py` — Pydantic models that mirror the raw Substack API response shapes.
- `models/schemas.py` — Outward-facing API/MCP response models with `.from_substack()` factory methods that translate from raw shapes.

### Converters

`converters/markdown.py` has two separate concerns:
1. `markdown_to_doc` / `markdown_to_note_payload` — converts Markdown to Substack's ProseMirror JSON format (used when creating notes).
2. `html_to_markdown` — converts Substack post HTML to Markdown using `markdownify` (used in `FullPostResponse`).

### Extension system

Extensions allow plugging in extra routes, MCP tools, lifespan hooks, and credential/auth providers without modifying core code. They are loaded from:
1. `substack_gateway_oss.extensions` entry-points (installed packages).
2. `GATEWAY_EXTENSION_MODULES` env var (comma-separated `module:attr` strings).

An extension implements the `GatewayExtension` protocol (`extensions/base.py`). Only one `CredentialProvider` and one MCP auth provider may be active at a time.

### Configuration

All settings are in `config.py` with the `SUBSTACK_GATEWAY_` env prefix (e.g. `SUBSTACK_GATEWAY_LOG_LEVEL`). Key settings: `gateway_key`, `admin_token`, and the optional OAuth trio (`base_url`, `database_url`, `jwt_secret`). Request-level publication targeting is not a header anymore; it is carried in the Bearer token's `publication_url`.

### Tests

- **pytest** (`tests/`) — unit tests; currently covers the markdown converter.
- **behave** (`features/`) — BDD integration tests that spin up the full Starlette app via `TestClient` with `respx` for HTTP mocking. Step definitions live in `features/steps/`; shared helpers and fixture setup are in `features/steps/common.py` and `features/environment.py`.

Behave tests load fixture data from a `samples/` directory (four levels above `features/steps/`) — this directory is not committed; create it at the repo root when adding new BDD fixtures.
