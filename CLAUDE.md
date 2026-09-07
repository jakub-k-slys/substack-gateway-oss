# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies (dev included, all workspace members)
uv sync --all-packages --dev

# Run the server (dev mode with reload)
uv run python -m substack_gateway.main

# Lint
uv run ruff check .

# Format check / fix
uv run ruff format --check .
uv run ruff format .

# Type-check
uv run ty check .

# Unit tests (pytest)
uv run pytest packages/gateway_oss/tests/
uv run pytest packages/gateway_drafts/tests/
uv run pytest packages/gateway_stats/tests/

# Run a single test file
uv run pytest packages/gateway_oss/tests/test_markdown.py

# BDD integration tests (behave)
uv run behave packages/gateway_oss/features/

# Run a single feature file
uv run behave packages/gateway_oss/features/api/notes.feature

# Build all workspace packages (shell + gateway_core + every domain trio)
uv build --all-packages
```

When introducing changes, validate them before finishing the task. Prefer targeted runs first, but the expected OSS validation set is:
- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run ty check .`
- `uv build --all-packages`
- `uv run pytest`
- `uv run behave packages/gateway_oss/features/`

Before committing or pushing, always run the relevant lint, format, type-check, and test commands for the touched area. Do not skip validation just because the change looks small.

Commit and PR titles must use Conventional Commits / semver-style prefixes such as `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, or `ci:`. Prefer the narrowest correct prefix and keep the subject concise and imperative. For breaking changes, use Conventional Commits semver signaling with `!` in the type or scope, and/or include a `BREAKING CHANGE:` footer in the commit body.

## Repository layout

This repository is a **uv workspace**. The root is a thin shell package
(`substack-gateway`, source in `src/substack_gateway/`) that composes the
Starlette app; functionality is provided by per-domain packages under
`packages/`.

```
pyproject.toml            # shell "substack-gateway": workspace root, console scripts, shared ruff/ty/behave/pytest config
src/substack_gateway/     # app composition: app_factory.py, api_app.py, mcp_app.py, registry.py, ext_loader.py, runtime.py
packages/
├── gateway_core/         # shared foundation: auth, HTTP clients, config, capabilities, converters, models
├── gateway_oss/          # aggregator: health routes, extension protocol, versioning, backward-compat shims
├── gateway_<domain>/         # domain service package, e.g. gateway_notes, gateway_posts, gateway_drafts, gateway_stats
├── gateway_<domain>_rest/    # FastAPI router for that domain, published as a capability
└── gateway_<domain>_mcp/     # FastMCP tools for that domain, published as a capability
```

Each domain ships as a **trio** — `gateway_<domain>` (service layer), `gateway_<domain>_rest`
(FastAPI router), `gateway_<domain>_mcp` (FastMCP tools). Current trios include
`comments`, `following`, `notes`, `posts`, `profiles`, `drafts`, and `stats`. `me` is an
exception: `gateway_me_rest` and `gateway_me_mcp` exist as a two-package (REST + MCP
only) capability pair with no `gateway_me` service package — they compose
`NotesService`, `PostsService`, and `ProfilesService` from other domains instead of
owning a service of their own.
Each `_rest`/`_mcp` package registers itself through the `substack_gateway.capabilities`
entry-point group (e.g. `drafts_rest = "gateway_drafts_rest:capability"` in that
package's `pyproject.toml`); `src/substack_gateway/registry.py` discovers every
installed capability at runtime, so adding a domain does not require editing the
shell. The workspace uses `members = ["packages/*"]`, so it does not hardcode any
optional module — a downstream consumer can drop an additional member into a
checkout and it is picked up automatically. Use `uv sync --all-packages` so every
present member is installed.

## Architecture

This is a **Starlette-based gateway** that wraps the Substack private API and exposes two interfaces:

- **`/api/v1/*`** — a FastAPI REST API, assembled in `src/substack_gateway/api_app.py` from each
  domain's `_rest` capability plus `gateway_oss`'s own health routes.
- **`/mcp`** — a FastMCP MCP server, assembled in `src/substack_gateway/mcp_app.py` from each
  domain's `_mcp` capability.

Both interfaces are composed by `src/substack_gateway/app_factory.py`, which wires in
`registry.py` (capability discovery), `ext_loader.py` and `runtime.py` (extension
loading), and share the same `gateway_core` HTTP clients and config.

The root endpoint `/` returns per-module metadata:
`{"application": "substack-gateway", "modules": [{"name": "gateway-oss", "version": ..., "features": [...]}]}`.
The `gateway-oss` module's feature list is the union of `gateway_oss`'s own
features and every registered capability's `features`; each extension additionally
contributes its own module via `get_module_info()`, and the core aggregates them
(no single-provider override, no `tier` field).

### Request flow

```
Client request
  → Starlette app (app_factory.py)
    → /api/v1/* → FastAPI (api_app.py) → registry.py → domain `_rest` capability → Services → HTTP clients
    → /mcp      → FastMCP (mcp_app.py) → registry.py → domain `_mcp` capability → Services → HTTP clients
```

### Authentication

Gateway authentication and Substack authentication are separate concerns. REST requests carry an `x-gateway-token` header whose value is a **base64-encoded JSON token** containing `publication_url`, `substack_sid`, and `connect_sid` (Substack session cookies plus the target publication URL). `gateway_core.auth` decodes this token; each domain's `_rest` package's `deps.py` uses it to construct per-request HTTP clients.

The MCP layer does not resolve Substack credentials through OAuth. Authenticated MCP tools take an explicit `token` argument carrying the same base64-encoded Substack credentials object. An extension's OAuth provider may still authorize access to the gateway itself, but it does not store or inject Substack credentials.

### HTTP clients

- `SubstackHTTPBase` (`gateway_core.client.base`) — shared async httpx layer, raises `SubstackAuthError` (401/403) or `SubstackAPIError` (all other failures).
- `SubstackClient` (`gateway_core.client.substack`) — talks to `https://substack.com/api/v1/*` (global API: user settings, handles, profiles, following).
- `PublicationClient` (`gateway_core.client.publication`) — talks to a per-publication subdomain URL (notes, posts, comments, drafts, analytics). The publication URL comes from the gateway token's `publication_url` field.

Most API endpoints and authenticated MCP tools need **both** clients; `ProfilesService` only needs `SubstackClient`.

### Services

Each domain package (`gateway_notes`, `gateway_posts`, `gateway_profiles`, `gateway_following`, `gateway_drafts`, `gateway_stats`, ...) ships a thin service class that coordinates calls across the two HTTP clients — e.g. `NotesService`, `PostsService`, `ProfilesService`, `FollowingService`, `DraftsService`, `StatsService`. The matching `_rest` package instantiates them via FastAPI dependencies; the matching `_mcp` package instantiates them in tool helpers.

### Models

- `gateway_core.models.substack` — Pydantic models that mirror the raw Substack API response shapes.
- Each domain's `schemas.py` — outward-facing API/MCP response models with `.from_substack()`-style factory methods that translate from raw shapes.

### Converters

`gateway_core.converters.markdown` has two separate concerns:
1. `markdown_to_doc` / `markdown_to_note_payload` — converts Markdown to Substack's ProseMirror JSON format (used when creating notes).
2. `html_to_markdown` — converts Substack post HTML to Markdown using `markdownify` (used in `FullPostResponse`).

`gateway_drafts.converters.markdown` is a separate, domain-specific converter: `markdown_to_draft_doc` converts Markdown to draft ProseMirror JSON (used when creating and updating drafts).

### Extension system

Extensions allow plugging in extra routes, MCP tools, lifespan hooks, and auth providers without modifying core code. They are loaded from:
1. `substack_gateway_oss.extensions` entry-points (installed packages).
2. `GATEWAY_EXTENSION_MODULES` env var (comma-separated `module:attr` strings).

An extension implements the `GatewayExtension` protocol (`gateway_oss/extensions/base.py`). Only one MCP auth provider may be active at a time.

### Configuration

All settings are in `gateway_core.config.Settings` with the `SUBSTACK_GATEWAY_` env prefix (e.g. `SUBSTACK_GATEWAY_LOG_LEVEL`); `gateway_oss.config` re-exports it for backward compatibility. Key settings: `admin_token`, the optional `redis_url` shared cache backend, and the publication-analytics cache settings `stats_snapshot_cache_ttl_sec`, `stats_timeseries_ttl_sec`, and `stats_timeseries_watermark_lag_days`. Request-level publication targeting is carried in the `x-gateway-token` header's `publication_url` field.

Publication analytics caching (`gateway_stats`) is controlled by three settings:
- `SUBSTACK_GATEWAY_STATS_SNAPSHOT_CACHE_TTL_SEC` (default `900`) — TTL for cached publication/post snapshot aggregates.
- `SUBSTACK_GATEWAY_STATS_TIMESERIES_TTL_SEC` (default `86400`) — TTL for cached timeseries rows.
- `SUBSTACK_GATEWAY_STATS_TIMESERIES_WATERMARK_LAG_DAYS` (default `2`) — how many trailing days are treated as still maturing and re-fetched rather than served from cache.

### Tests

- **pytest** — unit tests live under each package's `tests/` (e.g. `packages/gateway_oss/tests/`, `packages/gateway_drafts/tests/`, `packages/gateway_stats/tests/`).
- **behave** (`packages/gateway_oss/features/`) — BDD integration tests that spin up the full Starlette app via `TestClient` with `respx` for HTTP mocking. Step definitions live in `packages/gateway_oss/features/steps/`; shared helpers and fixture setup are in `features/steps/common.py` and `features/environment.py`.

Behave tests load fixture data from a `samples/` directory (`packages/gateway_oss/samples/`, resolved as `parents[2]` of `features/steps/`).
