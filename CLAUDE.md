# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Substack Gateway is a monorepo containing two packages:

- **`packages/gateway_oss`** — the core OSS Starlette app. Exposes a FastAPI REST API (`/api/v1/*`) and a FastMCP MCP server (`/mcp`). Proxies authenticated requests to the Substack API using session cookies decoded from a base64 Bearer token.
- **`packages/gateway_pro`** — a pro extension that plugs into gateway_oss via the extension system. Adds OAuth 2.1 (with Neon DB persistence), a draft management API, and extended MCP tools. Deployable to Vercel.

## Commands

```bash
# Install dependencies
uv sync --dev

# Run dev server (http://0.0.0.0:5001, auto-reloads)
uv run python -m gateway_oss.main

# Lint & format
uv run ruff check .
uv run ruff format --check .

# Type-check
uv run ty check .

# Run unit tests (pytest)
uv run pytest packages/gateway_pro/tests/

# Run OSS BDD integration tests
uv run behave packages/gateway_oss/features/

# Run pro-only BDD integration tests (OAuth, drafts, MCP)
uv run behave packages/gateway_pro/features/

# Run both BDD suites
uv run behave packages/gateway_oss/features/ packages/gateway_pro/features/

# Run a single feature
uv run behave packages/gateway_oss/features/api/health.feature
```

CI runs: `uv build`, lint, format check, and type-check. No tests in CI currently.

When introducing changes, validate them before finishing the task. Prefer targeted runs first, but the expected validation set is:
- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run ty check .`
- `uv build`
- `uv run pytest`
- `uv run behave packages/gateway_oss/features/`
- `uv run behave packages/gateway_pro/features/`

Behave is currently run separately for OSS and PRO. In this monorepo, run the suite for the package you changed, and run both when the change spans OSS and PRO.

Before committing or pushing, always run the relevant lint, format, type-check, and test commands for the touched area. Do not skip validation just because the change looks small.

Commit and PR titles must use Conventional Commits / semver-style prefixes such as `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, or `ci:`. Prefer the narrowest correct prefix and keep the subject concise and imperative. For breaking changes, use Conventional Commits semver signaling with `!` in the type or scope, and/or include a `BREAKING CHANGE:` footer in the commit body.

## Architecture

```
Client request
  → Starlette app (app_factory.py)
    → /api/v1/* → FastAPI (api/app.py) → api/deps.py → Services → HTTP clients
    → /mcp      → FastMCP (mcp/app.py) → mcp/deps.py → Services → HTTP clients
    → /.well-known/* and /login/* → gateway_pro OAuth app (mounted at "/")
```

### HTTP Clients (`client/`)

- `SubstackHTTPBase` (`client/base.py`) — shared async httpx layer. Raises `SubstackAuthError` (401/403) or `SubstackAPIError` (all other failures).
- `SubstackClient` (`client/substack.py`) — talks to `https://substack.com/api/v1/*` (global: user settings, handles, profiles, following). Uses `alru_cache` for per-request profile caching.
- `PublicationClient` (`client/publication.py`) — talks to a per-publication subdomain URL (notes, posts, comments). The publication URL is decoded from the Bearer token's `publication_url` field.

Most API endpoints need both clients. `ProfilesService` only needs `SubstackClient`.

### Services (`services/`)

Thin domain classes (`NotesService`, `PostsService`, `ProfilesService`, `FollowingService`) that coordinate calls across the two HTTP clients. Instantiated per-request via FastAPI/FastMCP dependency injection.

### Authentication

Two auth paths:

1. **Bearer token** — Every request (except `GET /api/v1/health/live`) passes `Authorization: Bearer <base64-encoded-json>` where the JSON must contain `publication_url`, `substack_sid`, and `connect_sid`. Decoded in `auth.py`; `api/deps.py` and `mcp/deps.py` construct per-request HTTP clients from it.
2. **OAuth (pro only)** — When `SUBSTACK_GATEWAY_BASE_URL`, `SUBSTACK_GATEWAY_DATABASE_URL`, and `SUBSTACK_GATEWAY_JWT_SECRET` are all set, the MCP layer authenticates via OAuth 2.1 and looks up credentials from the Neon DB via the `CredentialProvider` interface instead of reading request headers.

The `gateway_key` (default `WW91IHNoYWxsIG5vdCBwYXNzCg==`) must also be present in the Bearer JSON to access draft endpoints; missing/wrong key → 403. All error responses show only a generic `"Invalid credentials"` message; the specific reason is logged at WARNING level.

### Extension System (`extensions/`)

Extensions plug in extra routes, MCP tools, lifespan hooks, and credential/auth providers without touching core code. Loaded from:
1. `substack_gateway_oss.extensions` entry-points (installed packages).
2. `GATEWAY_EXTENSION_MODULES` env var (comma-separated `module:attr` strings).

Each extension implements the `GatewayExtension` protocol (`extensions/base.py`): `register_api`, `register_app`, `register_mcp`, `get_lifespan_hooks`, `get_credential_provider`, `get_mcp_auth_provider`. Only one `CredentialProvider` and one MCP auth provider may be active at a time.

`gateway_pro` registers itself as an extension via its `ProExtension` class (`packages/gateway_pro/src/gateway_pro/extension.py`), wiring in the OAuth router, pro API routes, and pro MCP tools.

### Models

- `models/substack.py` — Pydantic models mirroring raw Substack API responses. Key models: `SubstackPublicProfile`, `SubstackNote`, `SubstackFullPost`, `SubstackDraft`.
- `models/schemas.py` — Outward-facing API/MCP response and request models with `.from_substack()` factory methods. Key models: `BearerCredentials`, `HealthResponse`, `ProfileResponse`, `NoteResponse`, `FullPostResponse`, `CreateDraftRequest`, `UpdateDraftRequest`, `DraftResponse`.
- `models/pagination.py` — Shared pagination helpers.

### Converters (`converters/markdown.py`)

Two separate concerns:
1. `markdown_to_note_payload` — Markdown → Substack ProseMirror JSON (used when creating notes).
2. `markdown_to_draft_body` / `draft_body_to_markdown` — Markdown ↔ ProseMirror JSON string for the draft `body` field. In pro: `html_to_markdown` converts Substack post HTML to Markdown via `markdownify`.

### Configuration (`config.py`)

`pydantic-settings` with `SUBSTACK_GATEWAY_` env prefix. Key settings:

| Env var | Default | Purpose |
|---|---|---|
| `SUBSTACK_GATEWAY_GATEWAY_KEY` | `WW91...` | Protects draft endpoints |
| `SUBSTACK_GATEWAY_ADMIN_TOKEN` | `WW91...` | Admin operations |
| `SUBSTACK_GATEWAY_BASE_URL` | `None` | Required for OAuth |
| `SUBSTACK_GATEWAY_DATABASE_URL` | `None` | Required for OAuth (Neon DB) |
| `SUBSTACK_GATEWAY_JWT_SECRET` | `None` | Required for OAuth |

### Testing

- **pytest** (`packages/gateway_pro/tests/`) — unit tests for OAuth DB, provider, and draft compatibility.
- **behave** — BDD integration tests using `respx` to mock Substack HTTP responses and FastAPI's `TestClient`. Step definitions in `features/steps/`; setup in `features/environment.py`. Fixture JSON files live in `packages/gateway_oss/samples/` (referenced by OSS tests) and equivalents for pro.

## Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/api/v1/health/live` | None | Liveness probe |
| `GET` | `/api/v1/health/ready` | Bearer | Connectivity check. `?show=true` includes decoded credentials. |
| `GET` | `/api/v1/me` | Bearer | Own profile |
| `GET` | `/api/v1/me/notes` | Bearer | Own notes (paginated, `?cursor=`) |
| `GET` | `/api/v1/me/posts` | Bearer | Own posts (paginated, `?limit=&offset=`) |
| `GET` | `/api/v1/me/following` | Bearer | Following list |
| `GET` | `/api/v1/notes/{note_id}` | Bearer | Single note by ID |
| `POST` | `/api/v1/notes` | Bearer | Publish a note (Markdown → Substack format) |
| `DELETE` | `/api/v1/notes/{note_id}` | Bearer | Delete a note by ID |
| `GET` | `/api/v1/posts/{post_id}` | Bearer | Full post by ID |
| `GET` | `/api/v1/posts/{post_id}/comments` | Bearer | Comments for a post |
| `GET` | `/api/v1/profiles/{slug}` | Bearer | Public profile |
| `GET` | `/api/v1/profiles/{slug}/posts` | Bearer | Profile posts |
| `GET` | `/api/v1/profiles/{slug}/notes` | Bearer | Profile notes |
| `POST` | `/api/v1/drafts` | Bearer + gateway_key | Create a post draft (body accepts Markdown) |
| `GET` | `/api/v1/drafts/{draft_id}` | Bearer + gateway_key | Fetch a draft (body returned as Markdown) |
| `PUT` | `/api/v1/drafts/{draft_id}` | Bearer + gateway_key | Delta-update a draft (body accepts Markdown) |
| `DELETE` | `/api/v1/drafts/{draft_id}` | Bearer + gateway_key | Delete a draft by ID |

OAuth endpoints (pro, when OAuth enabled): `GET /login/`, `POST /login/`, `GET /login/token`, `POST /login/token`, and `/.well-known/*` discovery routes. The phase-2 token form expects the publication URL to already be embedded in the submitted base64 token.

## Code Conventions

- Python >=3.10, async throughout
- Ruff: line-length 88, double quotes, rules E/F/I/UP (E501 ignored)
- Type checker `ty` excludes package feature directories
- All route handlers are async; all HTTP calls use `httpx.AsyncClient`
- Pydantic `BaseModel` for all data structures
- Delta updates: use `model_fields_set` + `model_dump(exclude_unset=True)` to send only explicitly provided fields to Substack
- `response_model_exclude_none=True` on endpoints where optional fields should be omitted entirely from the JSON response
