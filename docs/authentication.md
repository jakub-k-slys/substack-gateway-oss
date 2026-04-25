# Authentication

Gateway access and Substack access are separate concerns.

For this OSS repo, Substack credentials are passed as a base64-encoded JSON object. REST requests send that value as the `x-gateway-token` header. Authenticated MCP tools, when registered, accept the same encoded token as a `token` argument.

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
