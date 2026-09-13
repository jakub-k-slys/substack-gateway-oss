# Introduction

Substack Gateway OSS wraps Substack's private HTTP APIs behind a stable
gateway that is easier to consume from scripts, applications, and AI
tooling. It exposes a REST API and an MCP server on top of the same service
layer, so both interfaces stay behaviorally aligned.

The project is a **uv workspace**: a thin shell package
(`substack_gateway`) composes the Starlette app; the REST surface is built
with FastAPI and the MCP surface with FastMCP. Functionality lives in
per-domain packages under `packages/`.

## Architecture

Each domain — `comments`, `following`, `notes`, `posts`, `profiles`,
`drafts`, and `stats` — ships as a trio of packages:

- `gateway_<domain>/`: the service layer that coordinates calls across the
  Substack HTTP clients.
- `gateway_<domain>_rest/`: a FastAPI router, published as a capability.
- `gateway_<domain>_mcp/`: FastMCP tools, published as a capability.

`me` is an exception: `gateway_me_rest`/`gateway_me_mcp` are a two-package
pair with no standalone service package — they compose `NotesService`,
`PostsService`, and `ProfilesService` from the other domains instead.

`packages/gateway_core/` is the shared foundation: auth, HTTP clients,
config, converters, and Substack-shape models. `packages/gateway_oss/`
aggregates health routes, the extension protocol, and versioning.
`src/substack_gateway/registry.py` discovers every installed `_rest`/`_mcp`
capability at runtime through the `substack_gateway.capabilities`
entry-point group, so the shell never hardcodes a domain list.

## Application Endpoints

The root application exposes:

- `/`: application and per-module metadata
- `/api/v1/*`: the REST API (see [API Reference](api-reference.md))
- `/mcp`: the streamable-HTTP MCP endpoint (see [MCP](mcp.md))

## OSS Scope

Gateway authentication and Substack authentication are separate concerns
(see [Authentication](authentication.md)). On REST, every `/api/v1` route
requires the `x-gateway-token` header except the liveness probe — even
reads over public Substack data go through it, because the header is what
builds the request's Substack HTTP clients. On MCP, most tools accept an
optional `token` argument and fall back to an installed credential resolver
(this repository installs none); only the `profiles` tools
(`get_profile`, `get_profile_posts`, `get_profile_notes`) need no
credentials at all.

OSS performs no caching of its own — that was removed in 4.0.0. The
extension system lets a downstream deployment register additional routes,
MCP tools, an MCP auth provider, a credential resolver, lifespan hooks, or a
cache, without modifying the core gateway packages.
