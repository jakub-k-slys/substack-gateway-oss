# Repository Guidelines

## Project Structure & Module Organization
Core application code lives in `src/gateway_oss/`. `api/v1/` holds FastAPI routes, `mcp/` exposes the FastMCP surface, `services/` contains shared business logic, `client/` wraps Substack HTTP calls, and `models/` defines schemas and pagination types. Markdown conversion lives in `converters/`, while extension hooks live in `extensions/`. Unit tests are in `tests/`, BDD coverage is in `features/` with step definitions under `features/steps/`. Use `samples/` for request examples and treat `dist/` as build output.

## Build, Test, and Development Commands
Install the pinned toolchain and dev dependencies with `uv sync --dev`. Run the app locally with `uv run python -m gateway_oss.main`; this serves the API and MCP endpoints on port `5001` by default. Build distributable artifacts with `uv build`.

Quality checks:
- `uv run ruff check .` runs lint rules.
- `uv run ruff format --check .` verifies formatting.
- `uv run ty check .` runs static type checks.
- `uv build` verifies the package builds.
- `uv run pytest tests/` runs unit tests.
- `uv run behave features/` runs BDD and integration scenarios.

When introducing changes, run the relevant validation before finishing the task. Prefer targeted checks for the touched area first, but the default OSS validation bar is lint, format, type-check, build, pytest, and behave.

## Coding Style & Naming Conventions
Target Python `3.10+` and keep code compatible with the `src/` layout. Ruff enforces 4-space indentation, double quotes, import sorting, and an 88-character line length. Prefer explicit module names like `posts.py`, `profiles.py`, and `markdown.py`; use `snake_case` for functions, variables, and files, and `PascalCase` for Pydantic models and other classes. Keep route handlers thin and move reusable logic into `services/` or `client/`.

## Testing Guidelines
Place fast unit tests in `tests/test_*.py`. Add behavior coverage in `features/**/*.feature` when changing API contracts, MCP tools, or converter behavior, and keep step implementations in `features/steps/` focused on reusable actions. Run `ruff check`, `ruff format --check`, `ty check`, `uv build`, `pytest`, and `behave` before opening a PR.

## Commit & Pull Request Guidelines
Follow Conventional Commits. Recent history uses prefixes such as `ci:`, and release automation depends on semantic commit messages. Keep commits scoped and imperative, for example `feat: add profile notes pagination`. PR titles must also follow Conventional Commits. Include a short description, linked issue if applicable, config or env changes, and example requests/responses when API behavior changes.

## Configuration & Security
Configuration is environment-driven via the `SUBSTACK_GATEWAY_` prefix. Do not commit real Substack cookies, publication URLs, or JWT secrets. When adding settings, document them in `README.md` and keep authenticated endpoints aligned with the existing Bearer-token auth model, where `publication_url` is embedded in the base64 JSON credentials.
