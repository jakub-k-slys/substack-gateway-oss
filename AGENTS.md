# Repository Guidelines

## Project Structure & Module Organization
The root `src/substack_gateway/` package composes the Starlette app (`app_factory.py`, `api_app.py`, `mcp_app.py`, `registry.py`, `ext_loader.py`, `runtime.py`); it does not hold domain logic itself. `packages/gateway_core/` is the shared foundation: auth, HTTP clients, config, the capability protocol, converters, and models. Each domain (notes, posts, profiles, following, comments, drafts, stats, ...) ships as a trio of packages — `gateway_<domain>` for the service layer, `gateway_<domain>_rest` for its FastAPI router, `gateway_<domain>_mcp` for its FastMCP tools — each `_rest`/`_mcp` package registering itself through the `substack_gateway.capabilities` entry-point group. `me` is an exception: `gateway_me_rest`/`gateway_me_mcp` exist as a two-package (REST + MCP only) capability pair with no `gateway_me` service package, composing `NotesService`, `PostsService`, and `ProfilesService` from other domains instead. `packages/gateway_oss/` is now an aggregator: health routes, the extension protocol, versioning, and backward-compat shims. Unit tests live under each package's `tests/`; BDD coverage is in `packages/gateway_oss/features/` with step definitions under `features/steps/`. Use `packages/gateway_oss/samples/` for request examples and treat `dist/` as build output.

## Build, Test, and Development Commands
Install the pinned toolchain and dev dependencies with `uv sync --all-packages --dev`. Run the app locally with `uv run python -m substack_gateway.main`; this serves the API and MCP endpoints on port `5001` by default. Build distributable artifacts with `uv build --all-packages`.

Quality checks:
- `uv run ruff check .` runs lint rules.
- `uv run ruff format --check .` verifies formatting.
- `uv run ty check .` runs static type checks.
- `uv build --all-packages` verifies every package builds.
- `uv run pytest` runs unit tests across every package, including `packages/gateway_drafts/tests/` and `packages/gateway_stats/tests/`.
- `uv run behave packages/gateway_oss/features/` runs BDD and integration scenarios.

When introducing changes, run the relevant validation before finishing the task. Prefer targeted checks for the touched area first, but the default OSS validation bar is lint, format, type-check, build, pytest, and behave.
Before committing or pushing, always run the relevant lint, format, type-check, and test commands for the touched area. Do not skip validation just because the change looks small.

## Coding Style & Naming Conventions
Target Python `3.10+` and keep code compatible with the `src/` layout. Ruff enforces 4-space indentation, double quotes, import sorting, and an 88-character line length. Prefer explicit module names like `posts.py`, `profiles.py`, and `markdown.py`; use `snake_case` for functions, variables, and files, and `PascalCase` for Pydantic models and other classes. Keep route handlers thin and move reusable logic into `services/` or `client/`.

## Testing Guidelines
Place fast unit tests in `tests/test_*.py`. Add behavior coverage in `features/**/*.feature` when changing API contracts, MCP tools, or converter behavior, and keep step implementations in `features/steps/` focused on reusable actions. Run `ruff check`, `ruff format --check`, `ty check`, `uv build`, `pytest`, and `behave` before opening a PR.

## Commit & Pull Request Guidelines
Follow Conventional Commits. Recent history uses prefixes such as `ci:`, and release automation depends on semantic commit messages. Keep commits scoped and imperative, for example `feat: add profile notes pagination`. PR titles must also follow Conventional Commits. Include a short description, linked issue if applicable, config or env changes, and example requests/responses when API behavior changes.
Use semver-style prefixes consistently for commit titles, for example `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, and `ci:`. Prefer the narrowest correct prefix. For breaking changes, use Conventional Commits semver signaling with `!` in the type or scope, and/or include a `BREAKING CHANGE:` footer in the commit body.

## Configuration & Security
Configuration is environment-driven via the `SUBSTACK_GATEWAY_` prefix (`gateway_core.config.Settings`). Do not commit real Substack cookies, publication URLs, or JWT secrets. When adding settings, document them in `README.md` and keep authenticated endpoints aligned with the existing Bearer-token auth model, where `publication_url` is embedded in the base64 JSON credentials.

Publication analytics caching (`gateway_stats`) adds three settings: `SUBSTACK_GATEWAY_STATS_SNAPSHOT_CACHE_TTL_SEC` (default `900`), `SUBSTACK_GATEWAY_STATS_TIMESERIES_TTL_SEC` (default `86400`), and `SUBSTACK_GATEWAY_STATS_TIMESERIES_WATERMARK_LAG_DAYS` (default `2`).
