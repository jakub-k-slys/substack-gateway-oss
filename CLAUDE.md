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

Before committing or pushing, always run the relevant lint, format, type-check, and test commands for the touched area. Do not skip validation just because the change looks small.

Commit and PR titles must use Conventional Commits / semver-style prefixes such as `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, or `ci:`. Prefer the narrowest correct prefix and keep the subject concise and imperative. For breaking changes, use Conventional Commits semver signaling with `!` in the type or scope, and/or include a `BREAKING CHANGE:` footer in the commit body.

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
    → /mcp      → FastMCP (mcp/app.py) → tool helpers → Services → HTTP clients
```

### Authentication

Gateway authentication and Substack authentication are separate concerns. REST requests carry an `x-gateway-token` header whose value is a **base64-encoded JSON token** containing `publication_url`, `substack_sid`, and `connect_sid` (Substack session cookies plus the target publication URL). The `auth.py` module decodes this token; `api/deps.py` uses it to construct per-request HTTP clients.

The MCP layer no longer resolves Substack credentials through OAuth. Authenticated MCP tools take an explicit `token` argument carrying the same base64-encoded Substack credentials object. In PRO, OAuth may still authorize access to the gateway itself, but it does not store or inject Substack credentials.

### HTTP clients

- `SubstackHTTPBase` (`client/base.py`) — shared async httpx layer, raises `SubstackAuthError` (401/403) or `SubstackAPIError` (all other failures).
- `SubstackClient` — talks to `https://substack.com/api/v1/*` (global API: user settings, handles, profiles, following).
- `PublicationClient` (`client/publication.py`) — talks to a per-publication subdomain URL (notes, posts, comments). The publication URL comes from the gateway token's `publication_url` field.

Most API endpoints and authenticated MCP tools need **both** clients; `ProfilesService` only needs `SubstackClient`.

### Services

`services/` contains thin domain classes (`NotesService`, `PostsService`, `ProfilesService`, `FollowingService`) that coordinate calls across the two HTTP clients. REST instantiates them via FastAPI dependencies; MCP instantiates them in tool helpers.

### Models

- `models/substack.py` — Pydantic models that mirror the raw Substack API response shapes.
- `models/schemas.py` — Outward-facing API/MCP response models with `.from_substack()` factory methods that translate from raw shapes.

### Converters

`converters/markdown.py` has two separate concerns:
1. `markdown_to_doc` / `markdown_to_note_payload` — converts Markdown to Substack's ProseMirror JSON format (used when creating notes).
2. `html_to_markdown` — converts Substack post HTML to Markdown using `markdownify` (used in `FullPostResponse`).

### Extension system

Extensions allow plugging in extra routes, MCP tools, lifespan hooks, and auth providers without modifying core code. They are loaded from:
1. `substack_gateway_oss.extensions` entry-points (installed packages).
2. `GATEWAY_EXTENSION_MODULES` env var (comma-separated `module:attr` strings).

An extension implements the `GatewayExtension` protocol (`extensions/base.py`). Only one MCP auth provider may be active at a time.

### Configuration

All settings are in `config.py` with the `SUBSTACK_GATEWAY_` env prefix (e.g. `SUBSTACK_GATEWAY_LOG_LEVEL`). Key settings: `admin_token` and the optional OAuth trio (`base_url`, `database_url`, `jwt_secret`). Request-level publication targeting is carried in the `x-gateway-token` header's `publication_url` field.

### Tests

- **pytest** (`tests/`) — unit tests; currently covers the markdown converter.
- **behave** (`features/`) — BDD integration tests that spin up the full Starlette app via `TestClient` with `respx` for HTTP mocking. Step definitions live in `features/steps/`; shared helpers and fixture setup are in `features/steps/common.py` and `features/environment.py`.

Behave tests load fixture data from a `samples/` directory (four levels above `features/steps/`) — this directory is not committed; create it at the repo root when adding new BDD fixtures.
