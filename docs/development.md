# Development

## Project Layout

This repository is a uv workspace (`members = ["packages/*"]`). The root is
a thin shell package, `substack-gateway`, whose source lives in
`src/substack_gateway/`:

- `app_factory.py`, `api_app.py`, `mcp_app.py`: compose the Starlette app,
  the FastAPI `/api/v1` mount, and the FastMCP `/mcp` mount.
- `registry.py`: discovers every installed `_rest`/`_mcp` capability at
  runtime through the `substack_gateway.capabilities` entry-point group.
- `ext_loader.py`, `runtime.py`: load and run extensions.

Functionality lives under `packages/`:

- `gateway_core/`: shared foundation — auth, HTTP clients, config,
  capabilities, converters, models.
- `gateway_oss/`: aggregator — health routes, the extension protocol,
  backward-compat shims, versioning.
- `gateway_<domain>/`, `gateway_<domain>_rest/`, `gateway_<domain>_mcp/`:
  the service / REST / MCP trio for each domain (`comments`, `following`,
  `notes`, `posts`, `profiles`, `drafts`, `stats`). `me` is REST+MCP only,
  with no standalone service package.

Tests live per-package:

- `packages/<pkg>/tests/`: pytest unit tests.
- `packages/gateway_oss/features/`: BDD (behave) integration tests that spin
  up the full Starlette app via `TestClient` with `respx` for HTTP mocking.
  Step definitions live in `features/steps/`; fixture data lives in
  `packages/gateway_oss/samples/`.

## Common Commands

Install dependencies (every workspace member, dev included):

```bash
uv sync --all-packages --dev
```

Lint:

```bash
uv run ruff check .
```

Formatting check:

```bash
uv run ruff format --check .
```

Type checking:

```bash
uv run ty check .
```

Build every workspace package:

```bash
uv build --all-packages
```

Unit tests (per package):

```bash
uv run pytest packages/gateway_oss/tests/
uv run pytest packages/gateway_drafts/tests/
uv run pytest packages/gateway_stats/tests/
```

Or all of them at once:

```bash
uv run pytest
```

BDD tests:

```bash
uv run behave packages/gateway_oss/features/
```

## Extension System

Extensions can contribute:

- extra API routes
- extra app routes
- extra MCP tools
- lifespan hooks
- an MCP auth provider (only one may be active at a time)
- a credential resolver, for mapping an authenticated MCP caller to Substack
  credentials
- a cache (OSS ships no caching of its own — see `gateway_stats.cache` for
  the one cache-shaped extension point that exists today)

The runtime loads extensions from `substack_gateway_oss.extensions`
entry-points (installed packages) and from the `GATEWAY_EXTENSION_MODULES`
env var (comma-separated `module:attr` strings). An extension implements the
`GatewayExtension` protocol in `packages/gateway_oss/src/gateway_oss/extensions/base.py`.

## Configuration

All application settings are in `gateway_core.config.Settings`, using the
`SUBSTACK_GATEWAY_` env prefix; `gateway_oss.config` re-exports it for
backward compatibility. Settings include:

- `SUBSTACK_GATEWAY_LOG_LEVEL`
- `SUBSTACK_GATEWAY_SUBSTACK_BASE_URL`
- `SUBSTACK_GATEWAY_SUBSTACK_TIMEOUT_SEC`
- `SUBSTACK_GATEWAY_SUBSTACK_CONNECT_TIMEOUT_SEC`
- `SUBSTACK_GATEWAY_SUBSTACK_REQUESTS_PER_SECOND`
- `SUBSTACK_GATEWAY_SUBSTACK_MAX_CONNECTIONS`
- `SUBSTACK_GATEWAY_SUBSTACK_MAX_KEEPALIVE_CONNECTIONS`
- `SUBSTACK_GATEWAY_SUBSTACK_RETRY_ATTEMPTS`
- `SUBSTACK_GATEWAY_SUBSTACK_RETRY_MIN_WAIT_SEC`
- `SUBSTACK_GATEWAY_SUBSTACK_RETRY_MAX_WAIT_SEC`
- `SUBSTACK_GATEWAY_ADMIN_TOKEN` (no default) — gates administrative
  surfaces an extension may expose. Nothing in this repository reads it,
  so leaving it unset costs a plain gateway nothing; an extension that
  does read it must refuse the request when it is unset rather than
  compare against nothing.
- `SUBSTACK_GATEWAY_STATS_TIMESERIES_WATERMARK_LAG_DAYS` (default `2`) — how
  many trailing days of publication analytics are treated as still maturing
  and re-fetched rather than reused

`SUBSTACK_GATEWAY_REDIS_URL` is not read by anything in this codebase —
caching was removed as a built-in feature in 4.0.0. An extension may install
its own cache and its own configuration for it.
