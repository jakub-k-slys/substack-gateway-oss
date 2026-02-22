# Substack Gateway

A REST API gateway for [Substack](https://substack.com), built with [FastAPI](https://fastapi.tiangolo.com/). Proxies authenticated requests to the Substack API using session-based auth. Deployable to [Vercel](https://vercel.com).

## API Endpoints

All endpoints require two headers:

| Header | Description |
|--------|-------------|
| `Authorization` | `Bearer <substack-session-token>` (your Substack `connect.sid` cookie) |
| `x-publication-url` | Your publication URL (e.g. `https://example.substack.com`) |

### `GET /api/v1/health`

Check connectivity to the Substack API.

```json
{ "connected": true }
```

### `GET /api/v1/me`

Fetch the authenticated user's profile.

```json
{
  "id": 42,
  "slug": "testuser",
  "handle": "testuser",
  "name": "Test User",
  "url": "https://substack.com/@testuser",
  "avatar_url": "https://...",
  "bio": "Optional bio"
}
```

## Getting Started

Install dependencies using [uv](https://docs.astral.sh/uv/):

```bash
uv sync --dev
```

Or with pip:

```bash
python -m venv .venv
source .venv/bin/activate
pip install .
```

## Running Locally

Start the development server on http://0.0.0.0:5001 (auto-reloads on changes):

```bash
uv run main.py
```

## Testing

Integration tests use [Behave](https://behave.readthedocs.io/) (BDD):

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
npm install -g vercel
vercel --prod
```

Or `git push` with [Vercel git integration](https://vercel.com/docs/deployments/git).
