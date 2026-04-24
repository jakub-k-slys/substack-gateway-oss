# Contributing

Thanks for contributing to Substack Gateway OSS.

This project exposes a REST API and an MCP server on top of a shared service
layer for Substack data and actions. Contributions should preserve that shared
architecture, keep behavior well-covered by tests, and stay aligned with the
existing tooling and release process.

## Before You Start

- Check existing issues and pull requests before starting overlapping work.
- Prefer small, focused changes over broad refactors.
- Keep API, MCP, and converter changes backwards-compatible unless the change is
  intentionally breaking and documented as such.
- If your change affects public behavior, update the relevant docs in `docs/`
  and examples in `samples/` when applicable.

## Development Setup

This repository uses Python 3.10+ and `uv` for dependency management.

Install dependencies:

```bash
uv sync --dev
```

Run the application locally:

```bash
uv run python -m gateway_oss.main
```

The app serves the REST API and MCP endpoints on port `5001` by default.

Liveness check:

```bash
curl http://127.0.0.1:5001/api/v1/health/live
```

## Project Layout

Core application code lives in `src/gateway_oss/`.

- `api/v1/`: FastAPI route handlers
- `mcp/`: FastMCP surface
- `services/`: shared business logic
- `client/`: Substack HTTP client wrappers
- `models/`: schemas and pagination models
- `converters/`: Markdown conversion
- `extensions/`: extension hooks and runtime integration

Tests and supporting material live in:

- `tests/`: unit tests
- `features/`: BDD scenarios
- `features/steps/`: Behave step definitions
- `samples/`: example requests and fixtures
- `docs/`: project documentation

## Coding Standards

- Target Python `3.10+`.
- Follow Ruff formatting and linting rules.
- Use 4-space indentation, double quotes, and sorted imports.
- Use `snake_case` for functions, variables, and modules.
- Use `PascalCase` for classes and Pydantic models.
- Keep route handlers thin; move reusable logic into `services/` or `client/`.
- Prefer explicit module names such as `posts.py`, `profiles.py`, and
  `markdown.py`.

## Validation

Run the relevant checks for the area you changed before opening a pull request.
For most contributions, the expected validation bar is:

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check .
uv build
uv run pytest tests/
uv run behave features/
```

If your change is narrowly scoped, start with targeted checks, but do not skip
the relevant lint, format, type-check, and test commands before you submit.

## Testing Expectations

- Add or update unit tests in `tests/test_*.py` for business logic and client
  behavior.
- Add or update BDD scenarios in `features/**/*.feature` when changing API
  contracts, MCP tools, authentication flows, or converter behavior.
- Keep step definitions reusable and focused on behavior rather than
  implementation details.
- Prefer tests that exercise externally visible behavior over tests tightly
  coupled to private implementation.

## Documentation Expectations

Update documentation when your change affects:

- installation or configuration
- authentication or required headers
- request or response formats
- environment variables
- extension or MCP behavior

Relevant docs live under `docs/`, and the main repository overview is in
`README.md`.

## Commits and Pull Requests

Use Conventional Commits for commit messages and pull request titles.

Examples:

- `feat: add profile notes pagination`
- `fix: handle empty comment pages`
- `docs: clarify gateway token format`

Use the narrowest correct type, such as `feat:`, `fix:`, `docs:`, `refactor:`,
`test:`, `chore:`, or `ci:`.

For breaking changes, use Conventional Commits semver signaling with `!` and/or
include a `BREAKING CHANGE:` footer in the commit body.

Pull requests should include:

- a short description of the change
- linked issue or context when applicable
- notes about config or environment changes
- example requests and responses when API behavior changes

## Configuration and Security

Configuration is environment-driven via the `SUBSTACK_GATEWAY_` prefix.

- Do not commit real Substack cookies, publication URLs, or JWT secrets.
- Keep authenticated flows aligned with the existing Bearer-token model, where
  `publication_url` is embedded in the base64 JSON credentials.
- Document any new configuration in `README.md` and the relevant files under
  `docs/`.

If you discover a security issue, do not open a public issue with exploit
details. Report it privately to the maintainer instead.
