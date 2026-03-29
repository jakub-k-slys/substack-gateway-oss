These instructions apply to the entire repository unless a deeper `AGENTS.md` overrides them.
- `substack-gateway` is a Python 3.10+ FastAPI service that proxies authenticated requests to Substack.
- The monorepo is split into `packages/gateway_oss/` and `packages/gateway_pro/`.
- `gateway_oss.main:app` is the application entry point.
- The OSS app code lives in `packages/gateway_oss/src/gateway_oss/`.
- Pro-only OAuth code lives in `packages/gateway_pro/src/gateway_pro/oauth/`.
- Gateway authentication and Substack authentication are separate concerns.
- Authenticated REST requests pass Substack credentials in the `x-gateway-token` header, whose value is a base64-encoded JSON object containing `publication_url`, `substack_sid`, and `connect_sid`.
- Install dependencies with `uv sync --dev`.
- Run the app locally with `uv run uvicorn gateway_oss.main:app --host 0.0.0.0 --port 5001 --reload`.
- Lint with `uv run ruff check .`.
- Check formatting with `uv run ruff format --check .`.
- Type-check with `uv run ty check .`.
- Run unit tests with `uv run pytest`.
- Run BDD tests with `uv run behave packages/gateway_oss/features/`.
- Prefer targeted validation for the area you changed before running broader suites.
- When introducing changes, validate them before finishing the task. At minimum, run the relevant combination of:
  `uv run ruff check .`,
  `uv run ruff format --check .`,
  `uv run ty check .`,
  `uv build`,
  `uv run pytest`,
  `uv run behave packages/gateway_oss/features/`,
  `uv run behave packages/gateway_pro/features/`.
- Behave is currently run separately for OSS and PRO. In the monorepo, run the suite for the package you changed, and run both when the change crosses the package boundary.
- `packages/gateway_oss/src/gateway_oss/api/`: FastAPI app wiring and request dependencies.
- `packages/gateway_oss/src/gateway_oss/client/`: HTTP clients and upstream error handling.
- `packages/gateway_oss/src/gateway_oss/services/`: business logic for drafts, notes, posts, profiles, and following.
- `packages/gateway_oss/src/gateway_oss/models/`: Pydantic schemas and upstream response models.
- `packages/gateway_oss/src/gateway_oss/converters/markdown.py`: Markdown/Substack document conversion.
- `packages/gateway_oss/src/gateway_oss/mcp/`: MCP app and dependency wiring.
- `packages/gateway_pro/src/gateway_pro/oauth/`: OAuth provider, DB access, login flow, and router.
- `packages/gateway_oss/tests/`: OSS-focused pytest coverage.
- `packages/gateway_oss/features/`: OSS Behave coverage and step definitions.
- `samples/`: example Substack payloads used as reference fixtures.
- Match the existing Python style: async-first, typed code, Pydantic models, and small focused functions.
- Keep changes surgical. Fix the root cause instead of layering workarounds.
- Reuse existing service and dependency boundaries rather than moving logic into route handlers.
- Keep external API behavior stable unless the task explicitly requires a contract change.
- Use double quotes and keep Ruff clean.
- Avoid adding new dependencies unless they are clearly justified.
- Add or update the smallest relevant tests for behavior changes.
- For API behavior, prefer Behave coverage in `packages/gateway_oss/features/` when similar scenarios already exist.
- For pure logic changes, prefer `pytest` tests in `packages/gateway_oss/tests/`.
- When touching Markdown conversion, OAuth, or model translation, check for both unit and feature-level coverage nearby before adding new tests.
- There are generated/cache directories in the repo already; do not commit new generated artifacts.
- Respect existing user changes in the working tree. Do not revert unrelated modifications.
- If a task affects auth, cookies, bearer decoding, or embedded `publication_url`, verify error handling paths as well as success paths.
