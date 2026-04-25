# Introduction

Substack Gateway OSS wraps Substack's private HTTP APIs behind a stable gateway that is easier to consume from scripts, applications, and AI tooling.

The project is built with FastAPI for HTTP endpoints and FastMCP for the MCP surface. The OSS tier focuses on read access for public resources plus authenticated access for your own profile and note publishing workflows.

## Architecture

The application has four main layers:

- `api/v1/`: REST endpoints
- `mcp/`: MCP tool definitions and HTTP transport
- `services/`: business logic for profiles, posts, notes, and following
- `client/`: low-level Substack and publication HTTP clients

Supporting pieces include:

- `models/` for schema and pagination types
- `converters/` for Markdown conversion
- `extensions/` for optional runtime customization

## Application Endpoints

The root application exposes:

- `/`: basic application metadata
- `/api/v1/*`: REST API routes
- `/mcp`: streamable HTTP MCP endpoint

## OSS Scope

In this repository, public read operations are available without gateway auth on the MCP side. REST routes that depend on Substack access require the encoded credential token in the request headers.

The extension system also allows higher tiers or custom deployments to register additional MCP tools, app routes, API routes, and auth providers without modifying the core gateway package.
