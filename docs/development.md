# Development

## Project Layout

Core application code lives in `src/gateway_oss/`.

- `api/v1/`: FastAPI routes
- `mcp/`: FastMCP surface
- `services/`: business logic
- `client/`: Substack HTTP wrappers
- `models/`: schemas and pagination models
- `converters/`: Markdown conversion
- `extensions/`: extension hooks

Tests live in:

- `tests/` for unit tests
- `features/` for BDD scenarios

## Common Commands

Install dependencies:

```bash
uv sync --dev
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

Build:

```bash
uv build
```

Unit tests:

```bash
uv run pytest tests/
```

BDD tests:

```bash
uv run behave features/
```

## Extension System

Extensions can contribute:

- extra API routes
- extra app routes
- extra MCP tools
- lifespan hooks
- an MCP auth provider

The runtime loads extensions from Python entry points and from `GATEWAY_EXTENSION_MODULES`.

## Configuration

All application settings use the `SUBSTACK_GATEWAY_` prefix.

Important settings include:

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
