# CHANGELOG


## v0.1.0 (2026-03-21)

### Features

- Provide version on endpoint
  ([`a08534f`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/a08534f8019472c9a40f81e1f35d790c47622bf9))


## v0.0.4 (2026-03-21)

### Bug Fixes

- Add uvloop dep
  ([`066da64`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/066da6448fe517c70b133ac84b2a362d3db2a85f))

- App startup
  ([`ebf67e9`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/ebf67e95ce11a7226d172eaee2791017e51e024a))

- Linter
  ([`e4dbde2`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e4dbde2915e9fec9f33c78ba56abc46e5b652584))


## v0.0.3 (2026-03-20)

### Bug Fixes

- Update commit author
  ([`0a8e4d2`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/0a8e4d22fc4d970aa3a12801c6c1264499bb122f))

- Update commit author
  ([`5587752`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/55877527d795a78b2a7c37b3adda63d548d9d280))

- Update commit author
  ([`909706d`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/909706d16b2600b97cac65c1c061ffd15272b7a2))


## v0.0.2 (2026-03-20)

### Bug Fixes

- Update commiter
  ([`1fd9314`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/1fd931487134d6fea6715a4526ae3090299dcd45))

### Continuous Integration

- Bump GHA versions
  ([`a41ecfc`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/a41ecfc171b9576533175fd894b4d788f551f216))

- Bump GHA versions
  ([`1885091`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/188509193d3e48428318b5364a3e3d5fe57f96e0))

- Update production GHA
  ([`367b05c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/367b05c713cb6f782263b2d7b64887597f8a6a23))


## v0.0.1 (2026-03-20)

### Bug Fixes

- Deployment
  ([`db778c9`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/db778c990236d33e17e9906f12ccbfe0c4fac93c))

- Deployment ([#2](https://github.com/jakub-k-slys/substack-gateway-oss/pull/2),
  [`e3823ef`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e3823efa45dff0932c4e4e9a4f5f707bf0938bb4))


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
