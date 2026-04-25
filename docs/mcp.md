# MCP

The MCP server is mounted at `/mcp` and served over streamable HTTP.

## Public OSS Tools

These tools are available in OSS without gateway auth:

- `get_note`
- `get_post`
- `get_post_comments`
- `get_profile`
- `get_profile_posts`
- `get_profile_notes`

These tools read public Substack content only.

## Authenticated Tools

The codebase also defines authenticated MCP operations for:

- `create_note`
- `delete_note`
- `get_me`
- `get_my_notes`
- `get_my_posts`
- `get_my_following`

Those tools require an explicit `token` argument carrying the base64-encoded Substack credential JSON.

Whether authenticated tools are exposed depends on the active runtime and extension setup.

## Transport Notes

- Path: `/mcp`
- Transport: streamable HTTP
- Root MCP app path: `/`
- HTTP mode: stateless

## Extension Hooks

Extensions can register more MCP tools through the `GatewayExtension` interface. This is how custom deployments can add additional capabilities or custom auth handling on top of OSS.
