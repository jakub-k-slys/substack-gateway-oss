# Substack Gateway OSS Documentation

Substack Gateway OSS is a stateless Python gateway for Substack. It exposes:

- A REST API at `/api/v1/*`
- An MCP server at `/mcp`

Both interfaces share the same service layer and Substack clients, so the HTTP and MCP surfaces stay aligned.

## What You Can Do

- Read Substack profiles, posts, notes, comments, drafts, and publication /
  post analytics
- Create, update, and delete notes, comments, and drafts
- Access authenticated `me` endpoints and tools with a base64-encoded
  credential token
- Use the same gateway as a REST API or an MCP server for AI tools and agent
  workflows
- Extend the app with custom routes, MCP tools, auth providers, credential
  resolvers, and lifespan hooks

## Quick Links

- [Introduction](introduction.md)
- [Installation](installation.md)
- [Authentication](authentication.md)
- [API Reference](api-reference.md)
- [MCP](mcp.md)
- [Development](development.md)

## Repository

- GitHub: <https://github.com/jakub-k-slys/substack-gateway-oss>
