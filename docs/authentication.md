# Authentication

Gateway authentication and Substack authentication are separate concerns.
This repository has no notion of gateway-level accounts or sessions; what it
does have is a per-request Substack credential, carried differently on each
interface.

Substack credentials are a base64-encoded JSON object. REST requests send
that value as the `x-gateway-token` header. MCP tools accept the same
encoded value as an optional `token` argument.

On REST, every route under `/api/v1` requires `x-gateway-token` **except**
`GET /api/v1/health/live` — including read-only routes over public data such
as `GET /api/v1/profiles/{slug}`, because the header is what the gateway
uses to build the Substack HTTP clients for that request. A missing header
returns `422`; a malformed one returns `401`.

On MCP, the `token` argument is optional on every authenticated tool: if
supplied it is always used; if omitted, the gateway asks the installed
credential resolver (`gateway_core.credentials`) to map the caller to
Substack credentials. This repository installs no resolver, so an omitted
token raises `MissingCredentialsError`, whose message tells the caller to
pass `token`. The three `profiles` tools (`get_profile`,
`get_profile_posts`, `get_profile_notes`) are the exception — they read
Substack's public API directly and take no `token` at all. See
[MCP](mcp.md) for the full tool reference.

## Credential Shape

The credential object must contain:

```json
{
  "publication_url": "https://example.substack.com",
  "substack_sid": "s%3A...",
  "connect_sid": "s%3A..."
}
```

## Encode Credentials

```bash
echo '{"publication_url":"https://example.substack.com","substack_sid":"s%3A...","connect_sid":"s%3A..."}' | base64
```

Use the result as:

```text
x-gateway-token: <base64-encoded-json>
```

## REST Example

```bash
curl \
  -H "x-gateway-token: <base64-encoded-json>" \
  http://127.0.0.1:5001/api/v1/me
```

## MCP Example

Authenticated MCP tools use the same token value:

```json
{
  "token": "<base64-encoded-json>"
}
```

## Security Notes

- Do not commit real cookies, publication URLs, or secrets.
- Treat `substack_sid` and `connect_sid` as bearer credentials.
- Use environment variables or a secret manager in deployed environments.
