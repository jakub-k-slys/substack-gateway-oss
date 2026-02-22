# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Substack Gateway is a stateless FastAPI REST API that proxies authenticated requests to the Substack API. It extracts a Substack session token from the `Authorization: Bearer` header and a publication URL from the `x-publication-url` header, then forwards requests to Substack. Deployable to Vercel.

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

## Architecture

```
main.py  →  api/v1/{health,me}.py  →  api/deps.py  →  client/substack.py  →  Substack API
                                                         ↕
                                                    models/substack.py (Pydantic)
                                                    models/schemas.py (API responses)
```

- **`api/deps.py`** — FastAPI dependency injection: extracts Bearer token and `x-publication-url` header, creates `SubstackClient` instance. All route handlers receive the client via `Depends()`.
- **`client/substack.py`** — Async HTTP client using `httpx`. Converts the Bearer token into a `connect.sid` cookie for Substack auth. Two base URLs: publication-specific and main Substack.
- **`client/exceptions.py`** — `SubstackAuthError` (maps to 401) and `SubstackAPIError` (maps to 502).
- **`models/substack.py`** — Pydantic models for Substack API responses (e.g., `SubstackPublicProfile`). Uses `model_validate()` and `@classmethod` factory methods like `from_substack()`.
- **`models/schemas.py`** — API response schemas (`HealthResponse`, `ProfileResponse`).
- **`samples/`** — Real Substack API response JSON files used as reference for model design.

## Testing

Uses Behave (BDD) with Gherkin `.feature` files. Tests use `respx` to mock Substack HTTP responses and FastAPI's `TestClient`.

- `features/*.feature` — Gherkin scenarios
- `features/steps/` — Step implementations
- `features/environment.py` — Test setup/teardown hooks

## Code Conventions

- Python >=3.10, async throughout
- Ruff: line-length 88, double quotes, rules E/F/I/UP (E501 ignored)
- Type checker `ty` excludes `features/` directory
- All route handlers are async; all HTTP calls use `httpx.AsyncClient`
- Pydantic `BaseModel` for all data structures
