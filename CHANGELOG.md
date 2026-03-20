# CHANGELOG


## v0.0.0 (2026-03-20)

### Continuous Integration

- Add CI/CD workflows and semantic release configuration
  ([#1](https://github.com/jakub-k-slys/substack-gateway-oss/pull/1),
  [`544491c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/544491ca6fcbbc0719bac6bf321526403b62b40e))

## Summary This PR introduces automated release and pull request validation workflows, along with
  semantic versioning configuration to streamline the development and release process.

## Key Changes - **Added release workflow** (`.github/workflows/release.yaml`): Automated workflow
  that runs on a schedule (Monday, Wednesday, Saturday at 3 AM UTC) and on manual trigger. It uses
  Python Semantic Release to automatically version bumps, creates releases, builds the package with
  `uv build`, and publishes to PyPI. - **Added PR linting workflow**
  (`.github/workflows/lintpr.yaml`): Validates pull request titles against the Conventional Commits
  specification, providing helpful feedback via sticky comments when titles don't conform. - **Added
  semantic release configuration** (`pyproject.toml`): Configured Python Semantic Release with: -
  Version source pointing to `pyproject.toml:project.version` - Main branch as the release branch -
  Conventional commit message format for releases - Version-only tag format - **Updated
  documentation** (`README.md`): Replaced the "Drafts" API section with a "Comments" section
  documenting the `GET /api/v1/comments/{comment_id}` endpoint.

## Notable Implementation Details - The release workflow uses OIDC authentication (`id-token:
  write`) for PyPI publishing, improving security over token-based authentication - PR title
  validation provides inline feedback with a sticky comment that automatically clears when the title
  is corrected - The release workflow is conditional—package building and PyPI publishing only occur
  if a new release was actually created

https://claude.ai/code/session_01WquMu3U4e5rd4c1edAufGa

- Agents.md added
  ([`6bafc6c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/6bafc6c7de5a68b54287d9ae55d23799073b89f6))

- Update pyproject.toml
  ([`e5a7140`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e5a714005727a2c86d42fe0244c1655f9c3d2a3f))

- Update release workflow to use new token and remove schedule
  ([`a9ef276`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/a9ef276bd6d14b7a7fb3435706de0a8e666450e1))

Removed scheduled trigger and updated GitHub token secrets.
