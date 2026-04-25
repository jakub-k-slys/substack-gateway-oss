# API Reference

The REST API is mounted under `/api/v1`.

## Health

### `GET /api/v1/health/live`

Public liveness probe.

Response:

```json
{ "status": "ok" }
```

### `GET /api/v1/health/ready`

Authenticated readiness probe that verifies Substack connectivity. Optional query parameter:

- `show`: when `true`, includes the decoded credential payload in the response

## Me

These endpoints require `x-gateway-token`.

### `GET /api/v1/me`

Returns the authenticated user's profile.

### `GET /api/v1/me/notes`

Returns the authenticated user's notes. Query parameters:

- `cursor`

### `GET /api/v1/me/posts`

Returns the authenticated user's posts. Query parameters:

- `limit` default `25`
- `offset` default `0`

### `GET /api/v1/me/following`

Returns the list of profiles the authenticated user follows.

## Notes

### `GET /api/v1/notes/{note_id}`

Returns a single note by numeric ID.

### `POST /api/v1/notes`

Creates a note from Markdown content.

Request body:

```json
{
  "content": "Hello **world**",
  "attachment": "https://example.com"
}
```

Returns `201 Created`.

### `DELETE /api/v1/notes/{note_id}`

Deletes a note by numeric ID. Returns `204 No Content`.

## Posts

### `GET /api/v1/posts/{post_id}`

Returns a full post by numeric ID.

### `GET /api/v1/posts/{post_id}/comments`

Returns comments for the given post.

## Profiles

### `GET /api/v1/profiles/{slug}`

Returns a public profile by handle.

### `GET /api/v1/profiles/{slug}/posts`

Returns a page of posts for the profile. Query parameters:

- `limit` default `25`
- `offset` default `0`

### `GET /api/v1/profiles/{slug}/notes`

Returns a page of notes for the profile. Query parameters:

- `cursor`

## Comments

### `GET /api/v1/comments/{comment_id}`

Returns a single comment using the same response schema as note-style reader content.

## Common Error Semantics

- `400`: invalid request payload, such as invalid note content
- `401`: invalid credentials
- `404`: upstream not found, passed through where applicable
- `422`: validation or missing header errors
- `429`: upstream rate limiting, passed through where applicable
- `502`: upstream API failure mapped to bad gateway
