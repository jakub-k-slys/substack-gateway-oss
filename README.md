# Substack Gateway

A stateless REST API gateway for [Substack](https://substack.com), built with [FastAPI](https://fastapi.tiangolo.com/). Proxies authenticated requests to the Substack API using session-based auth. Deployable to [Vercel](https://vercel.com).

## Authentication

Every request (except `GET /api/v1/health/live`) requires two headers:

| Header | Description |
|--------|-------------|
| `Authorization` | `Bearer <token>` where `<token>` is a base64-encoded JSON credentials object |
| `x-publication-url` | Your publication URL, e.g. `https://example.substack.com` |

The credentials object must contain:

```json
{
  "substack_sid": "<your substack.sid cookie value>",
  "connect_sid": "<your connect.sid cookie value>",
  "gateway_key": "<gateway key for protected endpoints>"
}
```

Example — encode credentials:

```bash
echo '{"substack_sid":"s%3A...","connect_sid":"s%3A...","gateway_key":"WW91IHNoYWxsIG5vdCBwYXNzCg=="}' | base64
```

Pass the result as `Authorization: Bearer <base64string>`.

---

## API Endpoints

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

Add `?show=true` to include the decoded credentials in the response:

```json
{
  "connected": true,
  "tokens": {
    "substack_sid": "s%3A...",
    "connect_sid": "s%3A...",
    "gateway_key": "WW91..."
  }
}
```

---

### Me

#### `GET /api/v1/me`

Returns the authenticated user's own profile.

```json
{
  "id": 254824415,
  "handle": "jakubslys",
  "name": "Jakub Slys",
  "url": "https://substack.com/@jakubslys",
  "avatar_url": "https://...",
  "bio": "..."
}
```

#### `GET /api/v1/me/notes`

Returns a paginated list of the authenticated user's notes.

Query params: `cursor` (optional, for pagination).

```json
{
  "items": [ { "id": 1, "body": "...", "likes_count": 5, "author": { ... }, "published_at": "..." } ],
  "next_cursor": "..."
}
```

#### `GET /api/v1/me/posts`

Returns a paginated list of the authenticated user's posts.

Query params: `limit` (default 25), `offset` (default 0).

```json
{
  "items": [ { "id": 1, "title": "...", "subtitle": "...", "published_at": "..." } ],
  "next_cursor": "..."
}
```

#### `GET /api/v1/me/following`

Returns the list of users the authenticated user follows.

```json
{
  "items": [ { "id": 42, "handle": "someuser" } ]
}
```

---

### Notes

#### `GET /api/v1/notes/{note_id}`

Returns a single note by ID.

```json
{
  "id": 131648795,
  "body": "...",
  "likes_count": 3,
  "author": { "id": 42, "name": "...", "handle": "...", "avatar_url": "..." },
  "published_at": "2025-01-01T00:00:00Z"
}
```

#### `POST /api/v1/notes`

Publishes a new note. Body is converted from Markdown to Substack's editor format.

Request:

```json
{
  "content": "Hello **world**",
  "attachment": "https://example.com"
}
```

Response (`201 Created`):

```json
{ "id": 999 }
```

---

### Posts

#### `GET /api/v1/posts/{post_id}`

Returns a full post by ID.

```json
{
  "id": 167180194,
  "title": "...",
  "slug": "my-post",
  "subtitle": "...",
  "url": "https://...",
  "published_at": "...",
  "html_body": "...",
  "reactions": { "❤": 10 },
  "tags": ["tech"]
}
```

#### `GET /api/v1/posts/{post_id}/comments`

Returns all comments for a post.

```json
{
  "items": [ { "id": 1, "body": "Great post!", "is_admin": false } ]
}
```

---

### Profiles

#### `GET /api/v1/profiles/{slug}`

Returns a public profile by handle.

```json
{
  "id": 42,
  "handle": "jakubslys",
  "name": "Jakub Slys",
  "url": "https://substack.com/@jakubslys",
  "avatar_url": "https://...",
  "bio": "..."
}
```

#### `GET /api/v1/profiles/{slug}/posts`

Returns paginated posts for a profile.

Query params: `limit` (default 25), `offset` (default 0).

#### `GET /api/v1/profiles/{slug}/notes`

Returns paginated notes for a profile.

Query params: `cursor` (optional).

---

### Drafts

All draft endpoints require a valid `gateway_key` in the credentials. Requests with a missing or incorrect key are rejected with `403`.

#### `POST /api/v1/drafts`

Creates a new post draft. All fields are optional.

Request:

```json
{
  "title": "My Draft",
  "subtitle": "A subtitle",
  "body": "<p>Content here</p>"
}
```

Response (`201 Created`):

```json
{
  "id": 189531629,
  "uuid": "f0deca7a-b4c0-4389-9b0b-d4239790d914"
}
```

#### `GET /api/v1/drafts/{draft_id}`

Returns a draft by ID.

```json
{
  "title": "My Draft",
  "subtitle": "A subtitle",
  "body": "{\"type\":\"doc\",\"content\":[...]}"
}
```

#### `PUT /api/v1/drafts/{draft_id}`

Updates specific fields of a draft. Only the fields included in the request body are updated (delta update).

Request (any subset of fields):

```json
{
  "title": "Updated title"
}
```

Response:

```json
{
  "title": "Updated title",
  "subtitle": "A subtitle",
  "body": "{\"type\":\"doc\",\"content\":[...]}"
}
```

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
uv run main.py
```

## Testing

```bash
uv run behave features/
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
