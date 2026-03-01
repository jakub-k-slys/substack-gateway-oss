# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Substack Gateway is a stateless FastAPI REST API that proxies authenticated requests to the Substack API. It decodes a base64-encoded JSON credentials object from the `Authorization: Bearer` header and a publication URL from the `x-publication-url` header, then forwards requests to Substack using session cookies. Deployable to Vercel.

## Commands

```bash
# Install dependencies
uv sync --dev

# Run dev server (http://0.0.0.0:5001, auto-reloads)
uv run main.py

# Lint & format
uv run ruff check .
uv run ruff format --check .

# Type-check
uv run ty check .

# Run all integration tests
uv run behave features/

# Run a single test feature
uv run behave features/health.feature
```

CI runs: build (`uv build`), lint, format check, and type-check. No tests in CI currently.

## Authentication

Every request (except `GET /api/v1/health/live`) requires:

- `Authorization: Bearer <base64-encoded-json>` — the JSON must contain `substack_sid` and `connect_sid` (and optionally `gateway_key`).
- `x-publication-url` — your Substack publication URL.

The `gateway_key` is required for draft endpoints. The default key is `WW91IHNoYWxsIG5vdCBwYXNzCg==` (configured in `config.py` via `settings.gateway_key`). Requests with a missing or incorrect key receive a `403`.

All error responses expose only a generic `"Invalid credentials"` message. The specific reason (missing prefix, bad base64, missing fields, wrong gateway_key) is logged at WARNING level only.

## Architecture

```
main.py  →  api/v1/{health,me,notes,posts,profiles,drafts}.py
                    ↓
              api/deps.py  →  client/substack.py  →  Substack API
                    ↕                  ↕
             models/schemas.py   models/substack.py
```

- **`api/deps.py`** — Decodes the base64 Bearer token into a `BearerCredentials` Pydantic model, validates `x-publication-url`, creates a `SubstackClient` per request. Exposes `get_credentials`, `require_gateway_key`, and `get_substack_client` as FastAPI dependencies.
- **`client/substack.py`** — Async HTTP client using `httpx`. Passes `substack.sid` and `connect.sid` cookies to Substack. Two base URLs: `_pub_base` (publication-specific) and `_sub_base` (global `substack.com`). Uses `alru_cache` for per-request profile caching.
- **`client/exceptions.py`** — `SubstackAuthError` (maps to 401/403) and `SubstackAPIError` (maps to 502).
- **`models/substack.py`** — Pydantic models for Substack API responses. Uses `model_validate()`. Key models: `SubstackPublicProfile`, `SubstackNote`, `SubstackFullPost`, `SubstackDraft`, `SubstackDraftPayload`, `SubstackUserSettingsResponse`.
- **`models/schemas.py`** — API response and request schemas. Key models: `BearerCredentials`, `HealthResponse`, `ProfileResponse`, `NoteResponse`, `FullPostResponse`, `CreateDraftRequest`, `UpdateDraftRequest`, `DraftResponse`.
- **`config.py`** — App settings via `pydantic-settings`. Includes `gateway_key` for protecting draft endpoints.
- **`converters/markdown.py`** — Converts Markdown to Substack's ProseMirror note payload.
- **`samples/`** — Real Substack API response JSON files used as test fixtures and model design reference.

## Testing

Uses Behave (BDD) with Gherkin `.feature` files. Tests use `respx` to mock Substack HTTP responses and FastAPI's `TestClient`.

- `features/*.feature` — Gherkin scenarios
- `features/steps/` — Step implementations
- `features/environment.py` — Test setup/teardown hooks

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
| `GET` | `/api/v1/posts/{post_id}` | Bearer | Full post by ID |
| `GET` | `/api/v1/posts/{post_id}/comments` | Bearer | Comments for a post |
| `GET` | `/api/v1/profiles/{slug}` | Bearer | Public profile |
| `GET` | `/api/v1/profiles/{slug}/posts` | Bearer | Profile posts |
| `GET` | `/api/v1/profiles/{slug}/notes` | Bearer | Profile notes |
| `POST` | `/api/v1/drafts` | Bearer + gateway_key | Create a post draft |
| `GET` | `/api/v1/drafts/{draft_id}` | Bearer + gateway_key | Fetch a draft |
| `PUT` | `/api/v1/drafts/{draft_id}` | Bearer + gateway_key | Delta-update a draft |

## Code Conventions

- Python >=3.10, async throughout
- Ruff: line-length 88, double quotes, rules E/F/I/UP (E501 ignored)
- Type checker `ty` excludes `features/` directory
- All route handlers are async; all HTTP calls use `httpx.AsyncClient`
- Pydantic `BaseModel` for all data structures
- Delta updates: use `model_fields_set` + `model_dump(exclude_unset=True)` to send only explicitly provided fields to Substack
- `response_model_exclude_none=True` on endpoints where optional fields should be omitted entirely from the JSON response
