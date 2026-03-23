# Substack Gateway

[![CI](https://github.com/jakub-k-slys/substack-gateway/actions/workflows/ci.yml/badge.svg)](https://github.com/jakub-k-slys/substack-gateway/actions/workflows/ci.yml)

A stateless gateway for [Substack](https://substack.com) that exposes two interfaces:

- **REST API** (`/api/v1/*`) — a FastAPI HTTP API
- **MCP server** (`/mcp`) — a [FastMCP](https://github.com/jlowin/fastmcp) server for AI tool use

Both share the same service layer and HTTP clients. Deployable to [Vercel](https://vercel.com).

---

## Authentication

Every request (except `GET /api/v1/health/live`) requires one header:

| Header | Description |
|--------|-------------|
| `Authorization` | `Bearer <token>` where `<token>` is a base64-encoded JSON credentials object |

The credentials object must contain:

```json
{
  "publication_url": "https://example.substack.com",
  "substack_sid": "<your substack.sid cookie value>",
  "connect_sid": "<your connect.sid cookie value>"
}
```

For protected endpoints such as drafts, include `gateway_key` in the same JSON object.

Encode credentials:

```bash
echo '{"publication_url":"https://example.substack.com","substack_sid":"s%3A...","connect_sid":"s%3A...","gateway_key":"WW91IHNoYWxsIG5vdCBwYXNzCg=="}' | base64
```

Pass the result as `Authorization: Bearer <base64string>`.

---

## REST API Endpoints

### Health

#### `GET /api/v1/health/live`

Public liveness probe. No authentication required.

```json
{ "status": "ok" }
```

#### `GET /api/v1/health/ready`

Authenticated readiness probe. Verifies connectivity to Substack.

```json
{ "connected": true }
```

Add `?show=true` to include the decoded credentials in the response.

---

### Me

#### `GET /api/v1/me`

Returns the authenticated user's own profile.

#### `GET /api/v1/me/notes`

Returns paginated notes for the authenticated user. Query params: `cursor`.

#### `GET /api/v1/me/posts`

Returns paginated posts for the authenticated user. Query params: `limit` (default 25), `offset` (default 0).

#### `GET /api/v1/me/following`

Returns the list of users the authenticated user follows.

---

### Notes

#### `GET /api/v1/notes/{note_id}`

Returns a single note by ID.

#### `POST /api/v1/notes`

Publishes a new note. `content` is Markdown; converted to Substack's editor format automatically.

```json
{ "content": "Hello **world**", "attachment": "https://example.com" }
```

Returns `201 Created` with `{ "id": 999 }`.

#### `DELETE /api/v1/notes/{note_id}`

Deletes a note by ID. Returns `204 No Content`.

---

### Posts

#### `GET /api/v1/posts/{post_id}`

Returns a full post by ID, including HTML body as Markdown.

#### `GET /api/v1/posts/{post_id}/comments`

Returns all comments for a post.

---

### Profiles

#### `GET /api/v1/profiles/{slug}`

Returns a public profile by handle.

#### `GET /api/v1/profiles/{slug}/posts`

Returns paginated posts for a profile. Query params: `limit`, `offset`.

#### `GET /api/v1/profiles/{slug}/notes`

Returns paginated notes for a profile. Query params: `cursor`.

---

### Drafts

All draft endpoints require a valid `gateway_key` in the credentials. Requests without it are rejected with `403`.

#### `POST /api/v1/drafts`

Creates a new post draft. `body` accepts Markdown.

```json
{ "title": "My Draft", "subtitle": "A subtitle", "body": "Hello **world**." }
```

Returns `201 Created` with `{ "id": 189531629, "uuid": "..." }`.

#### `GET /api/v1/drafts/{draft_id}`

Returns a draft by ID. `body` is returned as Markdown.

#### `PUT /api/v1/drafts/{draft_id}`

Delta-updates a draft. Only included fields are updated. `body` accepts Markdown.

#### `DELETE /api/v1/drafts/{draft_id}`

Deletes a draft by ID. Returns `204 No Content`.

---

## MCP Server

The MCP server is available at `/mcp` (streamable-http transport). It exposes the same operations as the REST API as MCP tools:

| Tool | Description |
|------|-------------|
| `get_note` | Retrieve a single note by ID |
| `create_note` | Publish a new note from Markdown |
| `delete_note` | Delete a note by ID |
| `get_me` | Get the authenticated user's profile |
| `get_my_notes` | Get the authenticated user's notes |
| `get_my_posts` | Get the authenticated user's posts |
| `get_my_following` | Get the list of followed profiles |
| `get_post` | Retrieve a full post by ID |
| `get_post_comments` | Retrieve comments for a post |
| `get_profile` | Retrieve a public profile by handle |
| `get_profile_posts` | Get paginated posts for a profile |
| `get_profile_notes` | Get paginated notes for a profile |
| `create_draft` | Create a new post draft (pro) |
| `get_draft` | Fetch a draft by ID (pro) |
| `update_draft` | Delta-update a draft (pro) |
| `delete_draft` | Delete a draft by ID (pro) |

The MCP server supports two authentication modes:
1. **Header-based** — pass `Authorization` with a base64-encoded credentials object that includes `publication_url` (same as the REST API).
2. **OAuth** — enabled when `SUBSTACK_GATEWAY_BASE_URL`, `SUBSTACK_GATEWAY_DATABASE_URL`, and `SUBSTACK_GATEWAY_JWT_SECRET` are all set; credentials are looked up via the active `CredentialProvider`.

---

## Configuration

All settings use the `SUBSTACK_GATEWAY_` env prefix:

| Variable | Default | Description |
|----------|---------|-------------|
| `SUBSTACK_GATEWAY_LOG_LEVEL` | `INFO` | Log level |
| `SUBSTACK_GATEWAY_GATEWAY_KEY` | (built-in default) | Key required for draft endpoints |
| `SUBSTACK_GATEWAY_ADMIN_TOKEN` | (built-in default) | Admin token |
| `SUBSTACK_GATEWAY_SUBSTACK_BASE_URL` | `https://substack.com` | Substack API base URL |
| `SUBSTACK_GATEWAY_SUBSTACK_TIMEOUT_SEC` | `30.0` | Request timeout (seconds) |
| `SUBSTACK_GATEWAY_SUBSTACK_CONNECT_TIMEOUT_SEC` | `10.0` | Connect timeout (seconds) |
| `SUBSTACK_GATEWAY_BASE_URL` | — | Required for OAuth mode |
| `SUBSTACK_GATEWAY_DATABASE_URL` | — | Required for OAuth mode (Neon DB) |
| `SUBSTACK_GATEWAY_JWT_SECRET` | — | Required for OAuth mode |

---

## Extension System

Extensions plug in extra routes, MCP tools, lifespan hooks, and credential/auth providers without modifying core code. Loaded from:

1. `substack_gateway_oss.extensions` entry-points (installed packages).
2. `GATEWAY_EXTENSION_MODULES` env var (comma-separated `module:attr` strings).

An extension implements the `GatewayExtension` protocol (`src/gateway_oss/extensions/base.py`):

```python
class GatewayExtension(Protocol):
    name: str
    def register_api(self, api: FastAPI, context: GatewayExtensionContext) -> None: ...
    def register_app(self, app: Starlette, context: GatewayExtensionContext) -> None: ...
    def register_mcp(self, mcp: FastMCP, context: GatewayExtensionContext) -> None: ...
    def get_lifespan_hooks(self, context: GatewayExtensionContext) -> Sequence[LifespanHook]: ...
    def get_credential_provider(self, context: GatewayExtensionContext) -> CredentialProvider | None: ...
    def get_mcp_auth_provider(self, context: GatewayExtensionContext) -> Any | None: ...
```

Only one `CredentialProvider` and one MCP auth provider may be active at a time.

---

## Error Responses

| Status | Meaning |
|--------|---------|
| `400` | Bad request (e.g. invalid publication URL) |
| `401` | Invalid credentials |
| `403` | Invalid or missing gateway key |
| `422` | Missing required headers or malformed request |
| `502` | Substack API error or unreachable |

---

## Getting Started

Install dependencies using [uv](https://docs.astral.sh/uv/):

```bash
uv sync --dev
```

## Running Locally

Start the development server on http://0.0.0.0:5001 (auto-reloads on changes):

```bash
uv run python -m gateway_oss.main
```

## Testing

```bash
# Unit tests
uv run pytest packages/gateway_pro/tests/

# BDD integration tests
uv run behave packages/gateway_oss/features/ packages/gateway_pro/features/
```

## Linting & Type Checking

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check .
```

## Deploying to Vercel

```bash
vercel --prod
```

Or push with [Vercel git integration](https://vercel.com/docs/deployments/git).
