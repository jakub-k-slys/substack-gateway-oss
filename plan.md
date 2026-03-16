# Plan: Split into OSS + Pro repos via uv workspace + git subtree

## Goal
Restructure into a uv workspace with two independent packages so that
`git subtree split --prefix=packages/gateway` yields a standalone OSS repo,
and `gateway_pro` is a separate package that layers on top.

---

## Phase 1 — Remove backward-compatibility shims

These shim files in `gateway` hard-import from `gateway_pro`, making the OSS
package uninstallable alone. Delete them and update all consumers to import
from `gateway_pro` directly.

### 1a. Delete shim files

- `src/gateway/oauth/__init__.py` (re-export)
- `src/gateway/oauth/bearer.py`
- `src/gateway/oauth/db.py`
- `src/gateway/oauth/login.py`
- `src/gateway/oauth/provider.py`
- `src/gateway/oauth/repositories.py`
- `src/gateway/oauth/router.py`
- `src/gateway/oauth/templates.py`
- `src/gateway/oauth/static/` (duplicate CSS; pro router already uses its own copy)
- `src/gateway/api/v1/drafts.py` (re-export of pro drafts router)
- `src/gateway/api/v1/users.py` (re-export of pro users router)
- `src/gateway/services/drafts.py` (re-export of pro DraftsService)

### 1b. Remove draft re-exports from shared models/converters

- `src/gateway/models/schemas.py` — delete lines 23 (`_pro_schemas = …`) and
  267-272 (the six `DraftXxx = _pro_schemas.…` aliases).
- `src/gateway/models/substack.py` — delete line 8 (`_pro_substack = …`) and
  lines 208-213 (the six `SubstackDraftXxx = _pro_substack.…` aliases).
- `src/gateway/converters/markdown.py` — delete the two wrapper functions
  `markdown_to_draft_body` and `draft_body_to_markdown` (lines 212-221).

### 1c. Update test/feature imports

| File | Old import path | New import path |
|------|----------------|-----------------|
| `tests/test_oauth_db.py` | `gateway.oauth.db` | `gateway_pro.oauth.db` |
| `tests/test_oauth_provider.py` | `gateway.oauth.bearer`, `gateway.oauth.provider` | `gateway_pro.oauth.bearer`, `gateway_pro.oauth.provider` |
| `features/steps/oauth_flow.py` | `gateway.oauth.db` | `gateway_pro.oauth.db` |
| `features/steps/oauth_provider.py` | `gateway.oauth.bearer`, `gateway.oauth.db`, `gateway.oauth.provider` | `gateway_pro.oauth.bearer`, `gateway_pro.oauth.db`, `gateway_pro.oauth.provider` |
| `features/steps/draft_body_converter.py` | `gateway.converters.markdown` (draft fns) | `gateway_pro.converters.markdown` |
| `features/steps/mcp_tools.py` | `gateway.services.drafts.DraftsService` | `gateway_pro.services.drafts.DraftsService` |
| `tests/test_pro_draft_compat.py` | Review and either delete (its purpose was testing the compat shim) or update imports |

### 1d. Remove `drafts_router` and `users_router` from `src/gateway/api/v1/__init__.py`

These routers should only be registered by `gateway_pro` via `_load_pro_router()` in
`api/app.py`. Verify `__init__.py` doesn't include them (current code already excludes them,
but confirm after deleting the shim files).

### 1e. Validate

- `uv run ruff check .`
- `uv run ruff format --check .`
- `uv run ty check .`
- `uv run behave features/`
- `uv run pytest tests/`
- `uv run python -c "from main import app; print(type(app).__name__)"` → Starlette

---

## Phase 2 — Restructure into uv workspace layout

Move packages under `packages/` so git subtree can cleanly split.

### 2a. New directory layout

```
pyproject.toml                  # root workspace definition only
packages/
  gateway/
    pyproject.toml              # OSS package metadata + deps
    src/gateway/                # (moved from src/gateway/)
  gateway_pro/
    pyproject.toml              # Pro package metadata + deps (depends on gateway)
    src/gateway_pro/            # (moved from src/gateway_pro/)
main.py                        # stays at root, imports gateway
features/                      # stays at root (integration tests)
tests/                         # stays at root (unit tests)
```

### 2b. Root pyproject.toml

Replace current single-package config with a workspace definition:

```toml
[project]
name = "substack-gateway"
version = "0.1.0"
requires-python = ">=3.10"

[tool.uv.workspace]
members = ["packages/*"]

[tool.uv.sources]
gateway = { workspace = true }
gateway-pro = { workspace = true }

[tool.ruff]
line-length = 88
# ... existing ruff config

[tool.ty]
# ... existing ty config
```

### 2c. packages/gateway/pyproject.toml (OSS)

```toml
[project]
name = "gateway"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "fastapi>=0.135.1",
    "httpx>=0.28.0",
    "pydantic>=2.0",
    "pydantic-settings>=2.0",
    "async-lru>=2.0",
    "uvicorn>=0.41.0",
    "fastmcp>=3.0.2",
    "markdownify>=1.2.2",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/gateway"]
```

### 2d. packages/gateway_pro/pyproject.toml (Pro)

```toml
[project]
name = "gateway-pro"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "gateway",
    "pyjwt>=2.11.0",
    "bcrypt>=5.0.0",
    "sqlalchemy>=2.0.48",
    "asyncpg>=0.31.0",
    "htpy>=25.12.0",
    "aiofiles>=24.1.0",
    "cryptography>=45.0.3",
]

[tool.uv.sources]
gateway = { workspace = true }

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/gateway_pro"]
```

### 2e. Move files

```bash
mkdir -p packages/gateway packages/gateway_pro
mv src/gateway packages/gateway/src/gateway
mv src/gateway_pro packages/gateway_pro/src/gateway_pro
rmdir src  # if empty
```

### 2f. Update main.py

No change needed — import paths remain `from gateway.app_factory import create_app`.

### 2g. Validate

- `uv sync --dev`
- All lint/format/type/test checks pass
- Verify `gateway` installs independently: `uv pip install packages/gateway`

---

## Phase 3 — Verify standalone OSS works

### 3a. Test gateway without gateway_pro

```bash
# Create a temp venv with only gateway
uv venv /tmp/oss-test
uv pip install --python /tmp/oss-test packages/gateway
/tmp/oss-test/bin/python -c "from gateway.app_factory import create_app; app = create_app(); print('OK')"
```

The conditional `try/except ImportError` blocks in `app_factory.py`, `api/app.py`,
`mcp/app.py`, and `mcp/deps.py` should all fall back gracefully.

### 3b. Confirm pro features activate when both are installed

```bash
uv sync --dev  # installs both via workspace
uv run python -c "from main import app; print(type(app).__name__)"
uv run behave features/
```

---

## Phase 4 — git subtree split (future, not implemented here)

Once the workspace structure is validated:

```bash
git subtree split --prefix=packages/gateway -b oss-gateway
# Push oss-gateway branch to a new public repo
```

The OSS repo would get its own `pyproject.toml`, `src/gateway/`, and could include
a subset of tests/features that don't touch pro features.

---

## Risks and considerations

- **import_module() at module level**: `schemas.py` and `substack.py` currently use
  `import_module("gateway_pro.…")` at the top of the file. This crashes on import
  if gateway_pro is absent. Phase 1b removes these.
- **BDD test split**: Draft/OAuth feature files test pro functionality but live in
  the root `features/` dir. For git subtree to give a clean OSS repo, pro-only
  features should eventually move under `packages/gateway_pro/tests/` or similar.
  This is deferred to a follow-up.
- **`gateway/oauth/static/`**: Duplicate of `gateway_pro/oauth/static/`. The pro
  router already references its own copy via `Path(__file__).parent / "static"`.
  Safe to delete the gateway copy.
- **`uv workspace` requires uv >= 0.6**: Ensure CI and dev environments use a
  recent uv version.
