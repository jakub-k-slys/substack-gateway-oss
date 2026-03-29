# Substack Gateway OSS

[![CI](https://github.com/jakub-k-slys/substack-gateway/actions/workflows/ci.yml/badge.svg)](https://github.com/jakub-k-slys/substack-gateway/actions/workflows/ci.yml)

A stateless gateway for [Substack](https://substack.com) that exposes two interfaces:

- **REST API** (`/api/v1/*`) — a FastAPI HTTP API
- **MCP server** (`/mcp`) — a [FastMCP](https://github.com/jlowin/fastmcp) server for AI tool use

Both share the same service layer and HTTP clients.

---

## Authentication

Gateway authentication and Substack authentication are separate concerns:

- Gateway authentication authorizes access to the gateway itself.
- Substack authentication provides the publication URL plus Substack session cookies needed to call Substack.

REST requests that need Substack authentication use one header:

| Header | Description |
|--------|-------------|
| `x-gateway-token` | Base64-encoded JSON credentials object |

The Substack credentials object must contain:

```json
{
  "publication_url": "https://example.substack.com",
  "substack_sid": "<your substack.sid cookie value>",
  "connect_sid": "<your connect.sid cookie value>"
}
```

Encode credentials:

```bash
echo '{"publication_url":"https://example.substack.com","substack_sid":"s%3A...","connect_sid":"s%3A..."}' | base64
```

Pass the result as `x-gateway-token: <base64string>`.

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

### Comments

#### `GET /api/v1/comments/{comment_id}`

Returns a single comment by ID.

---

## MCP Server

The MCP server is available at `/mcp` (streamable-http transport). In OSS it is read-only and public tools do not require gateway auth or Substack credentials:

| Tool | Description |
|------|-------------|
| `get_note` | Retrieve a single note by ID |
| `get_post` | Retrieve a full post by ID |
| `get_post_comments` | Retrieve comments for a post |
| `get_profile` | Retrieve a public profile by handle |
| `get_profile_posts` | Get paginated posts for a profile |
| `get_profile_notes` | Get paginated notes for a profile |

Authenticated MCP tools such as personal endpoints or writes are provided by PRO, not OSS. When present, they take an explicit `token` tool argument carrying the base64-encoded Substack credentials object; that token is separate from any gateway-level auth.

---

## Configuration

All settings use the `SUBSTACK_GATEWAY_` env prefix:

| Variable | Default | Description |
|----------|---------|-------------|
| `SUBSTACK_GATEWAY_LOG_LEVEL` | `INFO` | Log level |
| `SUBSTACK_GATEWAY_ADMIN_TOKEN` | (built-in default) | Admin token |
| `SUBSTACK_GATEWAY_SUBSTACK_BASE_URL` | `https://substack.com` | Substack API base URL |
| `SUBSTACK_GATEWAY_SUBSTACK_TIMEOUT_SEC` | `30.0` | Request timeout (seconds) |
| `SUBSTACK_GATEWAY_SUBSTACK_CONNECT_TIMEOUT_SEC` | `10.0` | Connect timeout (seconds) |
| `SUBSTACK_GATEWAY_BASE_URL` | — | Required for OAuth mode |
| `SUBSTACK_GATEWAY_DATABASE_URL` | — | Required for OAuth mode |
| `SUBSTACK_GATEWAY_JWT_SECRET` | — | Required for OAuth mode |

---

## Extension System

Extensions plug in extra routes, MCP tools, lifespan hooks, and auth providers without modifying core code. They are loaded from:

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
    def get_mcp_auth_provider(self, context: GatewayExtensionContext) -> Any | None: ...
```

Only one MCP auth provider may be active at a time.

---

## Error Responses

| Status | Meaning |
|--------|---------|
| `400` | Bad request (e.g. invalid publication URL) |
| `401` | Invalid credentials |
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
uv run pytest tests/

# BDD integration tests
uv run behave features/
```

## Linting & Type Checking

```bash
uv run ruff check .
uv run ruff format --check .
uv run ty check .
```
