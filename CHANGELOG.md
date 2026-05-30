# CHANGELOG


## v1.1.0 (2026-05-30)

### Bug Fixes

- Apply formatting updates
  ([`be13374`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/be13374e726202e0557ced99f91c3e4a9d31d67a))

- Log resolved application metadata at startup
  ([`5ce368e`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/5ce368ea5f8141dfbea469a83a777e45ac9840b7))

- Omit missing note authors and align ty excludes
  ([`14a342a`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/14a342a93bb6b4ced42eced2859e71bc12b4aa11))

- Prefer app version override for root metadata
  ([`fad3ba9`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/fad3ba927e3f6da0251d3f7d9c4bd8201ff47832))

- Preserve original authors for feed post items
  ([`7c63c99`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/7c63c99a21ca6e2bd2e8773f6c4de05e19d44573))

- Speed up behave Substack client settings
  ([`9000a85`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/9000a85158e84f32a620fa223db3b562995e6790))

- Use application version in root metadata
  ([`1e46541`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/1e465419c24f746e4e9c1a8b8e5e7a06c8e83351))

### Chores

- Sync gateway_oss subtree from upstream
  ([`98c8987`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/98c8987fa0474beb23d06c492909853d4cc87d49))

- Update Substack client default settings
  ([`ac3c90a`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/ac3c90ae9f3a71432586abdb4b7af2447426db1b))

- **deps**: Bump authlib from 1.6.11 to 1.6.12 in the uv group across 1 directory
  ([#39](https://github.com/jakub-k-slys/substack-gateway-oss/pull/39),
  [`6eeec01`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/6eeec0127fdb61dca35539aecd25df07c681c661))

Bumps the uv group with 1 update in the / directory: [authlib](https://github.com/authlib/authlib).

Updates `authlib` from 1.6.11 to 1.6.12 <details> <summary>Release notes</summary> <p><em>Sourced
  from <a href="https://github.com/authlib/authlib/releases">authlib's releases</a>.</em></p>
  <blockquote> <h2>v1.6.12</h2> <ul> <li> <ul> <li>Fix redirecting to unvalidated
  <code>redirect_uri</code> on <code>InvalidScopeError</code> in <code>OpenIDImplicitGrant</code>
  and <code>OpenIDHybridGrant</code>. <strong>Full Changelog</strong>: <a
  href="https://github.com/authlib/authlib/compare/v1.6.11...v1.6.12">https://github.com/authlib/authlib/compare/v1.6.11...v1.6.12</a></li>
  </ul> </li> </ul> </blockquote> </details> <details> <summary>Changelog</summary> <p><em>Sourced
  from <a href="https://github.com/authlib/authlib/blob/1.6.12/docs/changelog.rst">authlib's
  changelog</a>.</em></p> <blockquote> <h2>Version 1.6.12</h2> <p><strong>Released on may 4,
  2026</strong></p> <ul> <li>Fix redirecting to unvalidated <code>redirect_uri</code> on
  <code>InvalidScopeError</code> in <code>OpenIDImplicitGrant</code> and
  <code>OpenIDHybridGrant</code>.</li> </ul> </blockquote> </details> <details>
  <summary>Commits</summary> <ul> <li><a
  href="https://github.com/authlib/authlib/commit/e46e515b3a87ea63ab0606b248d75f69d83a2391"><code>e46e515</code></a>
  chore: bump to 1.6.12</li> <li><a
  href="https://github.com/authlib/authlib/commit/9babc131e13b018a267ae78747cba7caa6dfb7d5"><code>9babc13</code></a>
  fix: redirecting to unvalidated redirect_uri on InvalidScopeError in OIDC grants</li> <li>See full
  diff in <a href="https://github.com/authlib/authlib/compare/v1.6.11...1.6.12">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=authlib&package-manager=uv&previous-version=1.6.11&new-version=1.6.12)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore <dependency name> major version` will close this
  group update PR and stop Dependabot creating any more for the specific dependency's major version
  (unless you unignore this specific dependency's major version or upgrade to it yourself) -
  `@dependabot ignore <dependency name> minor version` will close this group update PR and stop
  Dependabot creating any more for the specific dependency's minor version (unless you unignore this
  specific dependency's minor version or upgrade to it yourself) - `@dependabot ignore <dependency
  name>` will close this group update PR and stop Dependabot creating any more for the specific
  dependency (unless you unignore this specific dependency or upgrade to it yourself) - `@dependabot
  unignore <dependency name>` will remove all of the ignore conditions of the specified dependency -
  `@dependabot unignore <dependency name> <ignore condition>` will remove the ignore condition of
  the specified dependency and ignore conditions You can disable automated security fix PRs for this
  repo from the [Security Alerts
  page](https://github.com/jakub-k-slys/substack-gateway-oss/network/alerts).

</details>

- **deps**: Bump authlib in the uv group across 1 directory
  ([`6ccd451`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/6ccd45155d88cff272d746351bd6df91ef8a3c01))

Bumps the uv group with 1 update in the / directory: [authlib](https://github.com/authlib/authlib).

Updates `authlib` from 1.6.11 to 1.6.12 - [Release
  notes](https://github.com/authlib/authlib/releases) -
  [Changelog](https://github.com/authlib/authlib/blob/1.6.12/docs/changelog.rst) -
  [Commits](https://github.com/authlib/authlib/compare/v1.6.11...1.6.12)

--- updated-dependencies: - dependency-name: authlib dependency-version: 1.6.12

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump fastapi from 0.136.0 to 0.136.1
  ([`35a5fd1`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/35a5fd15e53fdfce4a30510c8b6cfa98b088ff2d))

Bumps [fastapi](https://github.com/fastapi/fastapi) from 0.136.0 to 0.136.1. - [Release
  notes](https://github.com/fastapi/fastapi/releases) -
  [Commits](https://github.com/fastapi/fastapi/compare/0.136.0...0.136.1)

--- updated-dependencies: - dependency-name: fastapi dependency-version: 0.136.1

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump fastapi from 0.136.0 to 0.136.1
  ([#30](https://github.com/jakub-k-slys/substack-gateway-oss/pull/30),
  [`cf46a6a`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/cf46a6ac1ac26a54af2b4e74e359538687c124e2))

Bumps [fastapi](https://github.com/fastapi/fastapi) from 0.136.0 to 0.136.1. <details>
  <summary>Release notes</summary> <p><em>Sourced from <a
  href="https://github.com/fastapi/fastapi/releases">fastapi's releases</a>.</em></p> <blockquote>
  <h2>0.136.1</h2> <h3>Upgrades</h3> <ul> <li>⬆️ Update Pydantic v2 code to address deprecations. PR
  <a href="https://redirect.github.com/fastapi/fastapi/pull/15101">#15101</a> by <a
  href="https://github.com/svlandeg"><code>@​svlandeg</code></a>.</li> </ul> <h3>Internal</h3> <ul>
  <li>🔨 Tweak translation script. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15174">#15174</a> by <a
  href="https://github.com/YuriiMotov"><code>@​YuriiMotov</code></a>.</li> <li>⬆ Bump
  mkdocs-material from 9.7.1 to 9.7.6. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15408">#15408</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  inline-snapshot from 0.31.1 to 0.32.6. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15409">#15409</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  pytest-codspeed from 4.3.0 to 4.4.0. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15407">#15407</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  pytest-cov from 7.0.0 to 7.1.0. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15406">#15406</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  cloudflare/wrangler-action from 3.14.1 to 3.15.0. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15405">#15405</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump mypy
  from 1.19.1 to 1.20.1. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15410">#15410</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  python-dotenv from 1.2.1 to 1.2.2. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15400">#15400</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  starlette from 0.52.1 to 1.0.0. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15397">#15397</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  pygithub from 2.8.1 to 2.9.1. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15396">#15396</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  pyjwt from 2.12.0 to 2.12.1. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15393">#15393</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  zizmor from 1.23.1 to 1.24.1. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15394">#15394</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  strawberry-graphql from 0.312.3 to 0.314.3. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15395">#15395</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  python-multipart from 0.0.22 to 0.0.26. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15360">#15360</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  authlib from 1.6.9 to 1.6.11. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15373">#15373</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  aiohttp from 3.13.3 to 3.13.4. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15282">#15282</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  pygments from 2.19.2 to 2.20.0. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15263">#15263</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  pymdown-extensions from 10.20.1 to 10.21.2. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15391">#15391</a> by <a
  href="https://github.com/YuriiMotov"><code>@​YuriiMotov</code></a>.</li> <li>⬆ Bump pillow from
  12.1.1 to 12.2.0. PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15333">#15333</a>
  by <a href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆
  Bump pytest from 9.0.2 to 9.0.3. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15334">#15334</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  actions/upload-artifact from 7.0.0 to 7.0.1. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15374">#15374</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  actions/cache from 5.0.4 to 5.0.5. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15385">#15385</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>🔧 Update
  sponsors: remove Zuplo. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15369">#15369</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🔧 Update sponsors: remove
  Speakeasy. PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15368">#15368</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🔒️ Add zizmor and fix
  audit findings. PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15316">#15316</a> by
  <a href="https://github.com/YuriiMotov"><code>@​YuriiMotov</code></a>.</li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/fastapi/fastapi/commit/e54e5a8980ffa6d7ff68ee7b25a1c46036375521"><code>e54e5a8</code></a>
  🔖 Release version 0.136.1</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/9a8a5fd99902c3b80d4cc94b85e120e2b808825f"><code>9a8a5fd</code></a>
  📝 Update release notes</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/7815a32f2ed177b8b786a48b3e0712c05b5c644f"><code>7815a32</code></a>
  ⬆️ Update Pydantic v2 code to address deprecations (<a
  href="https://redirect.github.com/fastapi/fastapi/issues/15101">#15101</a>)</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/ef1c927b0558d414e199a666833942a6fabb3a51"><code>ef1c927</code></a>
  📝 Update release notes</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/38039e12a86e67f2001b9b7d96c219691d6cb4af"><code>38039e1</code></a>
  🔨 Tweak translation script (<a
  href="https://redirect.github.com/fastapi/fastapi/issues/15174">#15174</a>)</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/4fa826ce0a3b16884a04f51e5aac95d01790b599"><code>4fa826c</code></a>
  📝 Update release notes</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/c39415673e621665fdb7bbdde69beba7eb1dfd12"><code>c394156</code></a>
  ⬆ Bump mkdocs-material from 9.7.1 to 9.7.6 (<a
  href="https://redirect.github.com/fastapi/fastapi/issues/15408">#15408</a>)</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/ae230ad2f9d90a4e3f6222ff1a5d6e8da41ec0ad"><code>ae230ad</code></a>
  📝 Update release notes</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/d9eb39d1a1bf2f6e6e5d3a55088f61c712cb864e"><code>d9eb39d</code></a>
  ⬆ Bump inline-snapshot from 0.31.1 to 0.32.6 (<a
  href="https://redirect.github.com/fastapi/fastapi/issues/15409">#15409</a>)</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/4f8b5d14d324ae8e15cfae8d85adb4186d4c2175"><code>4f8b5d1</code></a>
  📝 Update release notes</li> <li>Additional commits viewable in <a
  href="https://github.com/fastapi/fastapi/compare/0.136.0...0.136.1">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=fastapi&package-manager=uv&previous-version=0.136.0&new-version=0.136.1)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps**: Bump fastapi from 0.136.1 to 0.136.3
  ([`a43628a`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/a43628a661955b0b6d4c7dcfb9f9c43a6d021712))

Bumps [fastapi](https://github.com/fastapi/fastapi) from 0.136.1 to 0.136.3. - [Release
  notes](https://github.com/fastapi/fastapi/releases) -
  [Commits](https://github.com/fastapi/fastapi/commits)

--- updated-dependencies: - dependency-name: fastapi dependency-version: 0.136.3

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump fastapi from 0.136.1 to 0.136.3
  ([#44](https://github.com/jakub-k-slys/substack-gateway-oss/pull/44),
  [`75b0c7e`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/75b0c7ecc7fad277bfd32c4353eb3c15348fc346))

Bumps [fastapi](https://github.com/fastapi/fastapi) from 0.136.1 to 0.136.3. <details>
  <summary>Release notes</summary> <p><em>Sourced from <a
  href="https://github.com/fastapi/fastapi/releases">fastapi's releases</a>.</em></p> <blockquote>
  <h2>0.136.3</h2> <h3>Refactors</h3> <ul> <li>♻️ Do not accept underscore headers when using
  <code>convert_underscores=True</code> (the default). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15589">#15589</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> </ul> <h2>0.136.2</h2>
  <h3>Refactors</h3> <ul> <li>♻️ Validate Server Sent Event fields to avoid applications from
  sending broken data. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15588">#15588</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> </ul> <h3>Docs</h3> <ul>
  <li>📝 Document <code>--entrypoint</code> CLI option. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15464">#15464</a> by <a
  href="https://github.com/YuriiMotov"><code>@​YuriiMotov</code></a>.</li> <li>📝 Update and simplify
  docs about help and management. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15583">#15583</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>📝 Add docs references to
  central contributing docs. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15580">#15580</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>📝 Update security policy.
  PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15577">#15577</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🍱 Update sponsors:
  TalorData image. PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15562">#15562</a> by
  <a href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>📝 Update docs,
  simplify usage of admonitions, only default ones. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15553">#15553</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>📝 Fix image URLs in
  <code>index.md</code>. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15534">#15534</a> by <a
  href="https://github.com/YuriiMotov"><code>@​YuriiMotov</code></a>.</li> <li>✏️ Fix Azkaban
  spelling typo in <code>virtual-environments.md‎</code>. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15463">#15463</a> by <a
  href="https://github.com/isaacbernat"><code>@​isaacbernat</code></a>.</li> <li>💄 Improve layout
  and styling. PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15462">#15462</a> by <a
  href="https://github.com/alejsdev"><code>@​alejsdev</code></a>.</li> <li>💄 Refactor opinions
  section with interactive tabs and new logos. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15458">#15458</a> by <a
  href="https://github.com/alejsdev"><code>@​alejsdev</code></a>.</li> <li>📝 Add FastAPI Conf '26
  announcement to docs. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15457">#15457</a> by <a
  href="https://github.com/alejsdev"><code>@​alejsdev</code></a>.</li> </ul> <h3>Translations</h3>
  <ul> <li>🌐 Improve translation consistency in
  <code>‎docs/pt/docs/advanced/generate-clients.md‎</code>. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15456">#15456</a> by <a
  href="https://github.com/Will-thom"><code>@​Will-thom</code></a>.</li> <li>🌐 Update translations
  for ja (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15530">#15530</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  uk (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15529">#15529</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  pt (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15528">#15528</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  de (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15527">#15527</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  tr (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15526">#15526</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  ko (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15525">#15525</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  zh-hant (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15524">#15524</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  fr (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15522">#15522</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  es (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15523">#15523</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  zh (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15520">#15520</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  ru (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15521">#15521</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Fix typos in Spanish
  LLM-prompt. PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15472">#15472</a> by <a
  href="https://github.com/crr004"><code>@​crr004</code></a>.</li> </ul> <h3>Internal</h3> <ul>
  <li>✅ Update tests, don't double dispose the engine. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15587">#15587</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>⚡️ Speed up test suite
  via caching and fixture scopes to make it ~24% faster. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/13583">#13583</a> by <a
  href="https://github.com/dikos1337"><code>@​dikos1337</code></a>.</li> <li>🔥 Remove config files
  now in central GitHub repo. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15585">#15585</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>⬆ Bump urllib3 from 2.6.3
  to 2.7.0. PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15502">#15502</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump idna
  from 3.11 to 3.15. PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15565">#15565</a>
  by <a href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆
  Bump cloudflare/wrangler-action from 3.15.0 to 4.0.0. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15571">#15571</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>🔧 Migrate
  docs from MkDocs to Zensical. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15563">#15563</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🔒️ Only allow team
  members to modify dependencies. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15548">#15548</a> by <a
  href="https://github.com/svlandeg"><code>@​svlandeg</code></a>.</li> </ul> <!-- raw HTML omitted
  --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Commits</summary> <ul>
  <li>See full diff in <a href="https://github.com/fastapi/fastapi/commits">compare view</a></li>
  </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=fastapi&package-manager=uv&previous-version=0.136.1&new-version=0.136.3)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps**: Bump fastmcp from 3.2.4 to 3.3.1
  ([`be2e6f8`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/be2e6f81e0e44f3a3a3e6679f60e6d219117b911))

Bumps [fastmcp](https://github.com/PrefectHQ/fastmcp) from 3.2.4 to 3.3.1. - [Release
  notes](https://github.com/PrefectHQ/fastmcp/releases) -
  [Changelog](https://github.com/PrefectHQ/fastmcp/blob/main/docs/changelog.mdx) -
  [Commits](https://github.com/PrefectHQ/fastmcp/compare/v3.2.4...v3.3.1)

--- updated-dependencies: - dependency-name: fastmcp dependency-version: 3.3.1

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump fastmcp from 3.2.4 to 3.3.1
  ([#42](https://github.com/jakub-k-slys/substack-gateway-oss/pull/42),
  [`0075a05`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/0075a050e27aee6f950bfe59a8024770fd0b72c5))

Bumps [fastmcp](https://github.com/PrefectHQ/fastmcp) from 3.2.4 to 3.3.1. <details>
  <summary>Release notes</summary> <p><em>Sourced from <a
  href="https://github.com/PrefectHQ/fastmcp/releases">fastmcp's releases</a>.</em></p> <blockquote>
  <h2>v3.3.1: Loop There It Is</h2> <p>FastMCP 3.3.1 is a hotfix for the 3.3 packaging split. Clean
  installs of 3.3.0 could fail on standalone component imports like <code>from fastmcp.tools import
  tool</code> because component modules reached auth and task primitives through
  <code>fastmcp.server</code>, pulling in the server/provider stack and exposing a circular
  import.</p> <p>Component-level auth and task primitives now live in lightweight utility modules,
  with the old server import paths preserved as compatibility re-exports. Component imports stay
  lightweight, existing server-facing imports continue to work, and the release also includes small
  docs corrections from the 3.3 rollout.</p> <!-- raw HTML omitted --> <h2>What's Changed</h2>
  <h3>Fixes 🐞</h3> <ul> <li>fix(docs): use valid FA icon on client-only package page by <a
  href="https://github.com/jlowin"><code>@​jlowin</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/4139">PrefectHQ/fastmcp#4139</a></li>
  <li>Decouple component imports from server by <a
  href="https://github.com/jlowin"><code>@​jlowin</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/4150">PrefectHQ/fastmcp#4150</a></li>
  </ul> <p><strong>Full Changelog</strong>: <a
  href="https://github.com/PrefectHQ/fastmcp/compare/v3.3.0...v3.3.1">https://github.com/PrefectHQ/fastmcp/compare/v3.3.0...v3.3.1</a></p>
  <h2>v3.3.0: Slim Reaper</h2> <p>FastMCP 3.3 ships <code>fastmcp-slim</code>, a new lightweight
  distribution that separates the client from the server stack. It also closes out a meaningful
  backlog of security hardening, observability improvements, and auth additions that accumulated
  through the 3.2 cycle.</p> <h2>fastmcp-slim</h2> <p>The full FastMCP package pulls in Starlette,
  Uvicorn, and the rest of the server machinery — necessary for running a server, but wasteful if
  you're writing a client, a script, or an agent that just needs to talk to MCP.
  <code>fastmcp-slim</code> is a dependency-light distribution that ships the client and transport
  layer without any of that.</p> <p>The import namespace is unchanged:</p> <pre
  lang="python"><code>from fastmcp import Client <p>async with Client(&quot;<a
  href="https://example.com/mcp">https://example.com/mcp</a>&quot;) as client: result = await
  client.call_tool(&quot;my_tool&quot;, {&quot;arg&quot;: &quot;value&quot;}) </code></pre></p>
  <p>Install <code>fastmcp-slim[client]</code> anywhere you want FastMCP's client without the server
  footprint — CI environments, lightweight agents, library dependencies that shouldn't force Uvicorn
  on downstream users.</p> <h2>Security</h2> <p>The OAuth proxy received three hardening upgrades.
  Silent consent is now guarded against AS-in-the-middle attacks — a malicious authorization server
  can no longer silently approve a consent it wasn't meant to handle. Redirect URI allowlist
  matching now rejects dot-segment paths (<code>/../</code>, <code>/./</code>) that could otherwise
  bypass prefix checks. And <code>ResponseCachingMiddleware</code> partitions its cache by access
  token, closing a gap where different users could see each other's cached responses.</p>
  <h2>Auth</h2> <p><code>AzureB2CProvider</code> adds first-class support for Azure AD B2C user
  flows. The OCI provider is fixed for 3.x installs. And <code>OAuthProxy</code> gains a public
  <code>update_scopes()</code> API for updating the proxy's required scopes after initialization —
  useful for servers that determine scope requirements at runtime.</p> <h2>Observability</h2>
  <p>OTEL instrumentation is now fully compliant with MCP semantic conventions. List operations
  (<code>list_tools</code>, <code>list_resources</code>, <code>list_prompts</code>,
  <code>list_resource_templates</code>) are instrumented, and delegate spans on proxy servers are
  enriched with backend attributes.</p> <h2>Thread Affinity</h2> <p>Sync tools run in a thread pool
  by default. If your tool holds thread-local state or is bound to a specific thread (UI frameworks,
  some database drivers), you can now opt out:</p> <!-- raw HTML omitted --> </blockquote> <p>...
  (truncated)</p> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/d8dcc273cac9f6f17889a1b60adbdc654f948a50"><code>d8dcc27</code></a>
  Decouple component imports from server (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/4150">#4150</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/255e3e491082d8fbaeb3ccf25be6983cbab8b657"><code>255e3e4</code></a>
  fix(docs): use valid FA icon on client-only package page (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/4139">#4139</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/73df4dcaeeba6f985607f633786d38db6caf23f7"><code>73df4dc</code></a>
  chore: Update SDK documentation (<a

href="https://redirect.github.com/PrefectHQ/fastmcp/issues/4096">#4096</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/ee48a0fd6e077e1c32e996f7b51fd442e31c514f"><code>ee48a0f</code></a>
  Refine fastmcp-slim packaging (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/4125">#4125</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/bb4894d2159cd10f0c07f038db9c56b14fb99586"><code>bb4894d</code></a>
  Add fastmcp-slim for client-only installs (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/4122">#4122</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/8209093871af25bc3ceb50bfbcec317632218afd"><code>8209093</code></a>
  fix(http): terminate active streamable-HTTP transports before lifespan shutdo...</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/cf59a4511ff1980fd932215ef886e665c829bdbf"><code>cf59a45</code></a>
  Fix OCI Provider issue in 3.x version. Add OCI auth provider example … (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/4116">#4116</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/89b99ecfb987781735295869d2e3d620dde7af4c"><code>89b99ec</code></a>
  fix(proxy): fall back to live identifier for backend_* span attributes (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/4109">#4109</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/310314cf149a18d0a76e5703ee98f80ffb035171"><code>310314c</code></a>
  fix: cli option --no-banner is NOT passed to cli but server-spec in-correctly...</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/28722f846a0319913a4a7b67dd65131d615214b6"><code>28722f8</code></a>
  fix: drop exc_info for expected tool failures, remove unreachable ValidationE...</li>
  <li>Additional commits viewable in <a
  href="https://github.com/PrefectHQ/fastmcp/compare/v3.2.4...v3.3.1">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=fastmcp&package-manager=uv&previous-version=3.2.4&new-version=3.3.1)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps**: Bump idna from 3.11 to 3.15 in the uv group across 1 directory
  ([#40](https://github.com/jakub-k-slys/substack-gateway-oss/pull/40),
  [`8bd51ab`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/8bd51abd9b7b1fb0a6dc4c2fcef63e1a43788e90))

Bumps the uv group with 1 update in the / directory: [idna](https://github.com/kjd/idna).

Updates `idna` from 3.11 to 3.15 <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/kjd/idna/blob/master/HISTORY.md">idna's changelog</a>.</em></p>
  <blockquote> <h2>3.15 (2026-05-12)</h2> <ul> <li>Enforce DNS-length cap on individual labels early
  in <code>check_label</code>, short-circuiting contextual-rule processing for oversized input while
  staying compatible with UTS 46 usage.</li> <li>Tidy core helpers: hoist bidi category sets to
  module-level frozensets (avoiding per-codepoint list construction), simplify length checks, and
  reuse the shared <code>_unicode_dots_re</code> from <code>idna.core</code> in the codec
  module.</li> <li>Use <code>raise ... from err</code> for proper exception chaining and switch
  internal string formatting to f-strings.</li> <li>Allow <code>flit_core</code> 4.x in the build
  backend.</li> <li>Expand the ruff lint set (flake8-bugbear, flake8-simplify, pyupgrade, perflint)
  and apply the surfaced fixes; pin lint CI to Python 3.14.</li> <li>Add Dependabot configuration
  for GitHub Actions.</li> <li>Convert README and HISTORY from reStructuredText to Markdown.</li>
  <li>Reference CVE-2026-45409 for the 3.14 advisory in place of the initial GHSA identifier.</li>
  </ul> <p>Thanks to Felix Yan, Stan Ulbrych, and metsw24-max for contributions to this release.</p>
  <h2>3.14 (2026-05-10)</h2> <ul> <li>Removed opportunity to process long inputs into quadratic time
  by rejecting oversize inputs up-front. Closes a bypass of the CVE-2024-3651 mitigation.
  [CVE-2026-45409]</li> </ul> <p>Thanks to Stan Ulbrych for reporting the issue.</p> <h2>3.13
  (2026-04-22)</h2> <ul> <li>Correct classification error for codepoint U+A7F1</li> </ul> <h2>3.12
  (2026-04-21)</h2> <ul> <li>Update to Unicode 17.0.0.</li> <li>Issue a deprecation warning for the
  transitional argument.</li> <li>Added lazy-loading to provide some performance improvements.</li>
  <li>Removed vestiges of code related to Python 2 support, including segmentation of data
  structures specific to Jython.</li> </ul> <p>Thanks to Rodrigo Nogueira for contributions to this
  release.</p> </blockquote> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/kjd/idna/commit/af30a092e158181d0b35ac66dfa813788126bdd8"><code>af30a09</code></a>
  Release 3.15</li> <li><a
  href="https://github.com/kjd/idna/commit/30314d4628744ca14cf2b5820564e5127a9f86f2"><code>30314d4</code></a>
  Pre-release 3.15rc0</li> <li><a
  href="https://github.com/kjd/idna/commit/05d4b219aa9eddc47371fcbd2000f0301016f3e9"><code>05d4b21</code></a>
  Merge pull request <a href="https://redirect.github.com/kjd/idna/issues/237">#237</a> from
  kjd/convert-docs-to-markdown</li> <li><a
  href="https://github.com/kjd/idna/commit/2987fdba1962bbb2358399e0084ba062b98a0bee"><code>2987fdb</code></a>
  Convert README and HISTORY from reStructuredText to Markdown</li> <li><a
  href="https://github.com/kjd/idna/commit/59fa8002d514bf4a5ce7b58f67b9ec587d53fa9c"><code>59fa800</code></a>
  Merge pull request <a href="https://redirect.github.com/kjd/idna/issues/236">#236</a> from
  kjd/dependabot/github_actions/actions-f3e34333ea</li> <li><a
  href="https://github.com/kjd/idna/commit/def69834ced5d4b3c50439d8b99c4c856ec19ca2"><code>def6983</code></a>
  Merge branch 'master' into dependabot/github_actions/actions-f3e34333ea</li> <li><a
  href="https://github.com/kjd/idna/commit/bbd8004a797185d8c56bb555cd5c88fde05e0631"><code>bbd8004</code></a>
  Merge pull request <a href="https://redirect.github.com/kjd/idna/issues/234">#234</a> from
  StanFromIreland/patch-1</li> <li><a
  href="https://github.com/kjd/idna/commit/edd07c05024344a6ccb517414ccb36683aee99fc"><code>edd07c0</code></a>
  Bump github/codeql-action from 3.35.2 to 4.35.2 in the actions group</li> <li><a
  href="https://github.com/kjd/idna/commit/5557db030c11bdec50d62aa5f631d705d33ba123"><code>5557db0</code></a>
  Merge branch 'master' into patch-1</li> <li><a
  href="https://github.com/kjd/idna/commit/f11746cf4981d25123ef7830d3ee60f07de8ae3d"><code>f11746c</code></a>
  Merge pull request <a href="https://redirect.github.com/kjd/idna/issues/235">#235</a> from
  StanFromIreland/patch-2</li> <li>Additional commits viewable in <a
  href="https://github.com/kjd/idna/compare/v3.11...v3.15">compare view</a></li> </ul> </details>
  <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=idna&package-manager=uv&previous-version=3.11&new-version=3.15)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore <dependency name> major version` will close this
  group update PR and stop Dependabot creating any more for the specific dependency's major version
  (unless you unignore this specific dependency's major version or upgrade to it yourself) -
  `@dependabot ignore <dependency name> minor version` will close this group update PR and stop
  Dependabot creating any more for the specific dependency's minor version (unless you unignore this
  specific dependency's minor version or upgrade to it yourself) - `@dependabot ignore <dependency
  name>` will close this group update PR and stop Dependabot creating any more for the specific
  dependency (unless you unignore this specific dependency or upgrade to it yourself) - `@dependabot
  unignore <dependency name>` will remove all of the ignore conditions of the specified dependency -
  `@dependabot unignore <dependency name> <ignore condition>` will remove the ignore condition of
  the specified dependency and ignore conditions You can disable automated security fix PRs for this
  repo from the [Security Alerts
  page](https://github.com/jakub-k-slys/substack-gateway-oss/network/alerts).

</details>

- **deps**: Bump idna in the uv group across 1 directory
  ([`29ab591`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/29ab5914ba0dffff7abec2f03277e231d402bfe9))

Bumps the uv group with 1 update in the / directory: [idna](https://github.com/kjd/idna).

Updates `idna` from 3.11 to 3.15 - [Release notes](https://github.com/kjd/idna/releases) -
  [Changelog](https://github.com/kjd/idna/blob/master/HISTORY.md) -
  [Commits](https://github.com/kjd/idna/compare/v3.11...v3.15)

--- updated-dependencies: - dependency-name: idna dependency-version: '3.15'

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump mkdocs-material from 9.6.14 to 9.7.6
  ([`1797cbc`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/1797cbc8808022d0ec7b71a4cf2b95cdd4d80e99))

Bumps [mkdocs-material](https://github.com/squidfunk/mkdocs-material) from 9.6.14 to 9.7.6. -
  [Release notes](https://github.com/squidfunk/mkdocs-material/releases) -
  [Changelog](https://github.com/squidfunk/mkdocs-material/blob/master/CHANGELOG) -
  [Commits](https://github.com/squidfunk/mkdocs-material/compare/9.6.14...9.7.6)

--- updated-dependencies: - dependency-name: mkdocs-material dependency-version: 9.7.6

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump mkdocs-material from 9.6.14 to 9.7.6
  ([#33](https://github.com/jakub-k-slys/substack-gateway-oss/pull/33),
  [`db4963b`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/db4963b2bee34401796e7e1d7a4631273bbb1e6d))

Bumps [mkdocs-material](https://github.com/squidfunk/mkdocs-material) from 9.6.14 to 9.7.6.
  <details> <summary>Release notes</summary> <p><em>Sourced from <a
  href="https://github.com/squidfunk/mkdocs-material/releases">mkdocs-material's
  releases</a>.</em></p> <blockquote> <h2>mkdocs-material-9.7.6</h2> <blockquote> <p>[!WARNING]</p>
  <p><strong>Material for MkDocs is in maintenance mode</strong></p> <p>Going forward, the Material
  for MkDocs team focuses on <a href="https://zensical.org">Zensical</a>, a next-gen static site
  generator built from first principles. We will provide critical bug fixes and security updates for
  Material for MkDocs until November 2026.</p> <p><a
  href="https://squidfunk.github.io/mkdocs-material/blog/2025/11/05/zensical/">Read the full
  announcement on our blog</a></p> </blockquote> <h2>Changes</h2> <ul> <li>Automatically disable
  MkDocs 2.0 warning for forks of MkDocs</li> </ul> <h2>mkdocs-material-9.7.5</h2> <blockquote>
  <p>[!WARNING]</p> <p><strong>Material for MkDocs is in maintenance mode</strong></p> <p>Going
  forward, the Material for MkDocs team focuses on <a href="https://zensical.org">Zensical</a>, a
  next-gen static site generator built from first principles. We will provide critical bug fixes and
  security updates for Material for MkDocs until November 2026.</p> <p><a
  href="https://squidfunk.github.io/mkdocs-material/blog/2025/11/05/zensical/">Read the full
  announcement on our blog</a></p> </blockquote> <h2>Changes</h2> <ul> <li>Limited version range of
  mkdocs to &lt;2</li> <li>Updated MkDocs 2.0 incompatibility warning (clarify relation with
  MkDocs)</li> </ul> <h2>mkdocs-material-9.7.4</h2> <blockquote> <p>[!WARNING]</p>
  <p><strong>Material for MkDocs is in maintenance mode</strong></p> <p>Going forward, the Material
  for MkDocs team focuses on <a href="https://zensical.org">Zensical</a>, a next-gen static site
  generator built from first principles. We will provide critical bug fixes and security updates for
  Material for MkDocs until November 2026.</p> <p><a
  href="https://squidfunk.github.io/mkdocs-material/blog/2025/11/05/zensical/">Read the full
  announcement on our blog</a></p> </blockquote> <h2>Changes</h2> <ul> <li>Hardened social cards
  plugin by switching to sandboxed environment (recommended by <a
  href="https://github.com/caveeroo"><code>@​caveeroo</code></a>)</li> <li>Updated MkDocs 2.0
  incompatibility warning</li> </ul> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p>
  </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/squidfunk/mkdocs-material/blob/master/CHANGELOG">mkdocs-material's
  changelog</a>.</em></p> <blockquote> <p>mkdocs-material-9.7.6 (2026-03-19)</p> <ul>
  <li>Automatically disable MkDocs 2.0 warning for forks of MkDocs</li> </ul>
  <p>mkdocs-material-9.7.5 (2026-03-10)</p> <ul> <li>Limited version range of mkdocs to &lt;2</li>
  <li>Updated MkDocs 2.0 incompatibility warning (clarify relation with MkDocs)</li> </ul>
  <p>mkdocs-material-9.7.4 (2026-03-03)</p> <ul> <li>Hardened social cards plugin by switching to
  sandboxed environment</li> <li>Updated MkDocs 2.0 incompatibility warning</li> </ul>
  <p>mkdocs-material-9.7.3 (2026-02-24)</p> <ul> <li>Fixed <a
  href="https://redirect.github.com/squidfunk/mkdocs-material/issues/8567">#8567</a>: Print MkDocs
  2.0 incompatibility warning to stderr</li> </ul> <p>mkdocs-material-9.7.2 (2026-02-18)</p> <ul>
  <li>Opened up version ranges of optional dependencies for forward-compatibility</li> <li>Added
  warning to 'mkdocs build' about impending MkDocs 2.0 incompatibility</li> </ul>
  <p>mkdocs-material-9.7.1 (2025-12-18)</p> <ul> <li>Updated requests to 2.30+ to mitigate CVE in
  urllib</li> <li>Fixed privacy plugin not picking up protocol-relative URLs</li> <li>Fixed <a
  href="https://redirect.github.com/squidfunk/mkdocs-material/issues/8542">#8542</a>: false
  positives and negatives captured in privacy plugin</li> </ul> <p>mkdocs-material-9.7.0
  (2025-11-11)</p> <p>⚠️ Material for MkDocs is now in maintenance mode</p> <p>This is the last
  release of Material for MkDocs that will receive new features. Going forward, the Material for
  MkDocs team focuses on Zensical, a next-gen static site generator built from first principles. We
  will provide critical bug fixes and security updates for Material for MkDocs for 12 months at
  least.</p> <p>Read the full announcement on our blog: <a
  href="https://squidfunk.github.io/mkdocs-material/blog/2025/11/05/zensical/">https://squidfunk.github.io/mkdocs-material/blog/2025/11/05/zensical/</a></p>
  <p>This release includes all features that were previously exclusive to the Insiders edition.
  These features are now freely available to everyone.</p> <p>Note on deprecated plugins: The
  projects and typeset plugins are included in this release, but must be considered deprecated. Both
  plugins proved unsustainable to maintain and represent architectural dead ends. They are provided
  as-is without ongoing support.</p> <p>Changes:</p> <!-- raw HTML omitted --> </blockquote> <p>...
  (truncated)</p> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/squidfunk/mkdocs-material/commit/6c52ed6289b171a153875491f059a94819ec3e10"><code>6c52ed6</code></a>
  Prepare 9.7.6 release</li> <li><a
  href="https://github.com/squidfunk/mkdocs-material/commit/51d9b76636431814df924bcda27485b16023978b"><code>51d9b76</code></a>
  Automatically disable MkDocs 2.0 warning for forks of MkDocs</li> <li><a
  href="https://github.com/squidfunk/mkdocs-material/commit/6f9a48b4048650341a654d9757da57fc1e3e323d"><code>6f9a48b</code></a>
  Updated links</li> <li><a
  href="https://github.com/squidfunk/mkdocs-material/commit/00b9933e5821fd852700268767d4fd53ae1ce1cb"><code>00b9933</code></a>
  Prepare 9.7.5 release</li> <li><a
  href="https://github.com/squidfunk/mkdocs-material/commit/37683d12c9cd62309aa917237741ee0886709b7c"><code>37683d1</code></a>
  Updated blog post on MkDocs 2.0</li> <li><a
  href="https://github.com/squidfunk/mkdocs-material/commit/199e31598055d5d6ea538618804c7558f5d81047"><code>199e315</code></a>
  Updated warning message to clarify relation to MkDocs</li> <li><a
  href="https://github.com/squidfunk/mkdocs-material/commit/10258334eb13545e6d708cf121c3867bfbdb6017"><code>1025833</code></a>
  Limited version range of mkdocs to &lt;2</li> <li><a
  href="https://github.com/squidfunk/mkdocs-material/commit/1532f523f6c650c9d6fd16229ee8bec0759b4151"><code>1532f52</code></a>
  Added update log to blog post</li> <li><a
  href="https://github.com/squidfunk/mkdocs-material/commit/d0c8b2862a966f5f268d4a4c35bb4fcfccebb9b1"><code>d0c8b28</code></a>
  Updated dependencies to fix vulnerabilities</li> <li><a
  href="https://github.com/squidfunk/mkdocs-material/commit/71d48699a0e2bef231e796818c4dc20b230a5f45"><code>71d4869</code></a>
  Updated blog post on MkDocs 2.0</li> <li>Additional commits viewable in <a
  href="https://github.com/squidfunk/mkdocs-material/compare/9.6.14...9.7.6">compare view</a></li>
  </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=mkdocs-material&package-manager=uv&previous-version=9.6.14&new-version=9.7.6)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps**: Bump pydantic from 2.13.3 to 2.13.4
  ([`e4df4a7`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e4df4a75d485ae123e91358910dbe87fa3255960))

Bumps [pydantic](https://github.com/pydantic/pydantic) from 2.13.3 to 2.13.4. - [Release
  notes](https://github.com/pydantic/pydantic/releases) -
  [Changelog](https://github.com/pydantic/pydantic/blob/v2.13.4/HISTORY.md) -
  [Commits](https://github.com/pydantic/pydantic/compare/v2.13.3...v2.13.4)

--- updated-dependencies: - dependency-name: pydantic dependency-version: 2.13.4

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump pydantic from 2.13.3 to 2.13.4
  ([#38](https://github.com/jakub-k-slys/substack-gateway-oss/pull/38),
  [`4edc265`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/4edc265f527c645d6639e7b194ab1dcc78be7b14))

Bumps [pydantic](https://github.com/pydantic/pydantic) from 2.13.3 to 2.13.4. <details>
  <summary>Release notes</summary> <p><em>Sourced from <a
  href="https://github.com/pydantic/pydantic/releases">pydantic's releases</a>.</em></p>
  <blockquote> <h2>v2.13.4 2026-05-06</h2> <h2>v2.13.4 (2026-05-06)</h2> <h3>What's Changed</h3>
  <h4>Packaging</h4> <ul> <li>Bump libc from 0.2.155 to 0.2.185 by <a
  href="https://github.com/Viicos"><code>@​Viicos</code></a> in <a
  href="https://redirect.github.com/pydantic/pydantic/pull/13109">#13109</a></li> <li>Adapt
  <code>pydantic-core</code> linker flags on macOS by <a
  href="https://github.com/washingtoneg"><code>@​washingtoneg</code></a> and <a
  href="https://github.com/Viicos"><code>@​Viicos</code></a> in <a
  href="https://redirect.github.com/pydantic/pydantic/pull/13147">#13147</a></li> </ul>
  <h4>Fixes</h4> <ul> <li>Preserve <code>RootModel</code> core metadata by <a
  href="https://github.com/Viicos"><code>@​Viicos</code></a> in <a
  href="https://redirect.github.com/pydantic/pydantic/pull/13129">#13129</a></li> </ul>
  <p><strong>Full Changelog</strong>: <a
  href="https://github.com/pydantic/pydantic/compare/v2.13.3...v2.13.4">https://github.com/pydantic/pydantic/compare/v2.13.3...v2.13.4</a></p>
  </blockquote> </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/pydantic/pydantic/blob/v2.13.4/HISTORY.md">pydantic's
  changelog</a>.</em></p> <blockquote> <h2>v2.13.4 (2026-05-06)</h2> <p><a
  href="https://github.com/pydantic/pydantic/releases/tag/v2.13.4">GitHub release</a></p> <h3>What's
  Changed</h3> <h4>Packaging</h4> <ul> <li>Bump libc from 0.2.155 to 0.2.185 by <a
  href="https://github.com/Viicos"><code>@​Viicos</code></a> in <a
  href="https://redirect.github.com/pydantic/pydantic/pull/13109">#13109</a></li> <li>Adapt
  <code>pydantic-core</code> linker flags on macOS by <a
  href="https://github.com/washingtoneg"><code>@​washingtoneg</code></a> and <a
  href="https://github.com/Viicos"><code>@​Viicos</code></a> in <a
  href="https://redirect.github.com/pydantic/pydantic/pull/13147">#13147</a></li> </ul>
  <h4>Fixes</h4> <ul> <li>Preserve <code>RootModel</code> core metadata by <a
  href="https://github.com/Viicos"><code>@​Viicos</code></a> in <a
  href="https://redirect.github.com/pydantic/pydantic/pull/13129">#13129</a></li> </ul>
  </blockquote> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/pydantic/pydantic/commit/cf67d4b3193c3fe43ede18612ed62785eee11382"><code>cf67d4b</code></a>
  Fix linting</li> <li><a
  href="https://github.com/pydantic/pydantic/commit/f0d8a214a5803036db46a56b1f62f1e56b81d662"><code>f0d8a21</code></a>
  Prepare release v2.13.4</li> <li><a
  href="https://github.com/pydantic/pydantic/commit/5e3fe1d41a00f441204241c66078003ae0391f9a"><code>5e3fe1d</code></a>
  Check for pydantic tag pattern in CI</li> <li><a
  href="https://github.com/pydantic/pydantic/commit/7f9edcc2a191d2eaa9751220eb910914e716a686"><code>7f9edcc</code></a>
  Document tagging conventions</li> <li><a
  href="https://github.com/pydantic/pydantic/commit/b46a0c9b8a4dd967fda8ec1a92f6437076bf262c"><code>b46a0c9</code></a>
  Adapt <code>pydantic-core</code> linker flags on macOS</li> <li><a
  href="https://github.com/pydantic/pydantic/commit/50629c851e61d887d5420452c311ec6203f1f400"><code>50629c8</code></a>
  Update to PyPy 7.3.22</li> <li><a
  href="https://github.com/pydantic/pydantic/commit/8522ebb71e5e9a6f7188af5f009f01785b8cf725"><code>8522ebb</code></a>
  Preserve <code>RootModel</code> core metadata</li> <li><a
  href="https://github.com/pydantic/pydantic/commit/a37f3aff090ca342dc5f48304889963530b993f8"><code>a37f3af</code></a>
  Adapt <code>MISSING</code> sentinel test to work with unreleased <code>typing_extensions</code>
  ver...</li> <li><a
  href="https://github.com/pydantic/pydantic/commit/909259a9df660518033aa686b689f045a6eaf9d2"><code>909259a</code></a>
  Remove Logfire example in documentation</li> <li><a
  href="https://github.com/pydantic/pydantic/commit/2c4174c366606fc2dc46cb806833a080aefa77df"><code>2c4174c</code></a>
  Bump libc from 0.2.155 to 0.2.185</li> <li>See full diff in <a
  href="https://github.com/pydantic/pydantic/compare/v2.13.3...v2.13.4">compare view</a></li> </ul>
  </details> <br />

- **deps**: Bump pydantic-settings from 2.14.0 to 2.14.1
  ([`65fa631`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/65fa631c2b666f29453f28e7f44ef0d7a67a6fc1))

Bumps [pydantic-settings](https://github.com/pydantic/pydantic-settings) from 2.14.0 to 2.14.1. -
  [Release notes](https://github.com/pydantic/pydantic-settings/releases) -
  [Commits](https://github.com/pydantic/pydantic-settings/compare/v2.14.0...v2.14.1)

--- updated-dependencies: - dependency-name: pydantic-settings dependency-version: 2.14.1

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump pydantic-settings from 2.14.0 to 2.14.1
  ([#36](https://github.com/jakub-k-slys/substack-gateway-oss/pull/36),
  [`84e34f2`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/84e34f2298c10fdfd82b9a8918722d513b92ea8b))

Bumps [pydantic-settings](https://github.com/pydantic/pydantic-settings) from 2.14.0 to 2.14.1.
  <details> <summary>Release notes</summary> <p><em>Sourced from <a
  href="https://github.com/pydantic/pydantic-settings/releases">pydantic-settings's
  releases</a>.</em></p> <blockquote> <h2>v2.14.1</h2> <h2>What's Changed</h2> <ul> <li>Bump the
  python-packages group with 4 updates by <a
  href="https://github.com/dependabot"><code>@​dependabot</code></a>[bot] in <a
  href="https://redirect.github.com/pydantic/pydantic-settings/pull/850">pydantic/pydantic-settings#850</a></li>
  <li>Bump the python-packages group with 5 updates by <a
  href="https://github.com/dependabot"><code>@​dependabot</code></a>[bot] in <a
  href="https://redirect.github.com/pydantic/pydantic-settings/pull/854">pydantic/pydantic-settings#854</a></li>
  <li>Bump the github-actions group with 3 updates by <a
  href="https://github.com/dependabot"><code>@​dependabot</code></a>[bot] in <a
  href="https://redirect.github.com/pydantic/pydantic-settings/pull/853">pydantic/pydantic-settings#853</a></li>
  <li>Bump the python-packages group with 2 updates by <a
  href="https://github.com/dependabot"><code>@​dependabot</code></a>[bot] in <a
  href="https://redirect.github.com/pydantic/pydantic-settings/pull/856">pydantic/pydantic-settings#856</a></li>
  <li>Fix field named <code>cls</code> conflicting with classmethod parameter by <a
  href="https://github.com/hramezani"><code>@​hramezani</code></a> in <a
  href="https://redirect.github.com/pydantic/pydantic-settings/pull/858">pydantic/pydantic-settings#858</a></li>
  <li>Prepare release 2.14.1 by <a href="https://github.com/hramezani"><code>@​hramezani</code></a>
  in <a
  href="https://redirect.github.com/pydantic/pydantic-settings/pull/859">pydantic/pydantic-settings#859</a></li>
  </ul> <p><strong>Full Changelog</strong>: <a
  href="https://github.com/pydantic/pydantic-settings/compare/v2.14.0...v2.14.1">https://github.com/pydantic/pydantic-settings/compare/v2.14.0...v2.14.1</a></p>
  </blockquote> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/pydantic/pydantic-settings/commit/e95c30bec8cfaee88ee275138c064aea97a25bdf"><code>e95c30b</code></a>
  Prepare release 2.14.1 (<a
  href="https://redirect.github.com/pydantic/pydantic-settings/issues/859">#859</a>)</li> <li><a
  href="https://github.com/pydantic/pydantic-settings/commit/0c8734581b6cf70a995afad603ac456631d00621"><code>0c87345</code></a>
  Fix field named <code>cls</code> conflicting with classmethod parameter (<a
  href="https://redirect.github.com/pydantic/pydantic-settings/issues/858">#858</a>)</li> <li><a
  href="https://github.com/pydantic/pydantic-settings/commit/7bd0072795a800065b42210b6dca90fc9b83daf7"><code>7bd0072</code></a>
  Bump the python-packages group with 2 updates (<a
  href="https://redirect.github.com/pydantic/pydantic-settings/issues/856">#856</a>)</li> <li><a
  href="https://github.com/pydantic/pydantic-settings/commit/b03e573d017ed48e1c2774a5e0b715db9766c76b"><code>b03e573</code></a>
  Bump the github-actions group with 3 updates (<a
  href="https://redirect.github.com/pydantic/pydantic-settings/issues/853">#853</a>)</li> <li><a
  href="https://github.com/pydantic/pydantic-settings/commit/eaa3b434938411ec8a3717ea646614561e713f51"><code>eaa3b43</code></a>
  Bump the python-packages group with 5 updates (<a
  href="https://redirect.github.com/pydantic/pydantic-settings/issues/854">#854</a>)</li> <li><a
  href="https://github.com/pydantic/pydantic-settings/commit/9f95615c24c6813c1d7d203576581a79cb6d9e8e"><code>9f95615</code></a>
  Bump the python-packages group with 4 updates (<a
  href="https://redirect.github.com/pydantic/pydantic-settings/issues/850">#850</a>)</li> <li>See
  full diff in <a
  href="https://github.com/pydantic/pydantic-settings/compare/v2.14.0...v2.14.1">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=pydantic-settings&package-manager=uv&previous-version=2.14.0&new-version=2.14.1)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps**: Bump python-multipart from 0.0.26 to 0.0.27 in the uv group across 1 directory
  ([#35](https://github.com/jakub-k-slys/substack-gateway-oss/pull/35),
  [`e95d268`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e95d26862edc7a199bfac0b6411aa0f26ee5732e))

Bumps the uv group with 1 update in the / directory:
  [python-multipart](https://github.com/Kludex/python-multipart).

Updates `python-multipart` from 0.0.26 to 0.0.27 <details> <summary>Release notes</summary>
  <p><em>Sourced from <a
  href="https://github.com/Kludex/python-multipart/releases">python-multipart's
  releases</a>.</em></p> <blockquote> <h2>0.0.27</h2> <h2>What's Changed</h2> <ul> <li>Pass parse
  offsets via constructors by <a href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/268">Kludex/python-multipart#268</a></li>
  <li>Add multipart header limits by <a href="https://github.com/Kludex"><code>@​Kludex</code></a>
  in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/267">Kludex/python-multipart#267</a></li>
  </ul> <p><strong>Full Changelog</strong>: <a
  href="https://github.com/Kludex/python-multipart/compare/0.0.26...0.0.27">https://github.com/Kludex/python-multipart/compare/0.0.26...0.0.27</a></p>
  </blockquote> </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/Kludex/python-multipart/blob/main/CHANGELOG.md">python-multipart's
  changelog</a>.</em></p> <blockquote> <h2>0.0.27 (2026-04-27)</h2> <ul> <li>Add multipart header
  limits <a href="https://redirect.github.com/Kludex/python-multipart/pull/267">#267</a>.</li>
  <li>Pass parse offsets via constructors <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/268">#268</a>.</li> </ul>
  </blockquote> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/Kludex/python-multipart/commit/6d1d6892a6b01b25da6f3e7b097e8e06c57fb250"><code>6d1d689</code></a>
  Version 0.0.27 (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/272">#272</a>)</li> <li><a
  href="https://github.com/Kludex/python-multipart/commit/0b10220b1555af068a2bc8b198022b1ae238200f"><code>0b10220</code></a>
  Run CI on main branch pull requests (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/271">#271</a>)</li> <li><a
  href="https://github.com/Kludex/python-multipart/commit/3e64f5f8caba0e5d391b0c1ad0f1c2edf9e8f911"><code>3e64f5f</code></a>
  Add multipart header limits (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/267">#267</a>)</li> <li><a
  href="https://github.com/Kludex/python-multipart/commit/eb109cc4eb8174f2a7efc1ba894b1bf6425c0b14"><code>eb109cc</code></a>
  Pass parse offsets via constructors (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/268">#268</a>)</li> <li><a
  href="https://github.com/Kludex/python-multipart/commit/78e29abb9a339598975beee093a770ec3033f76d"><code>78e29ab</code></a>
  Bump pytest from 9.0.2 to 9.0.3 (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/266">#266</a>)</li> <li><a
  href="https://github.com/Kludex/python-multipart/commit/b2ddd0982bdf0fe852e4f3baa12122d2827af46c"><code>b2ddd09</code></a>
  fuzz: Enhance fuzzing capabilities with new chunked and boundary tests (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/264">#264</a>)</li> <li>See full
  diff in <a href="https://github.com/Kludex/python-multipart/compare/0.0.26...0.0.27">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=python-multipart&package-manager=uv&previous-version=0.0.26&new-version=0.0.27)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore <dependency name> major version` will close this
  group update PR and stop Dependabot creating any more for the specific dependency's major version
  (unless you unignore this specific dependency's major version or upgrade to it yourself) -
  `@dependabot ignore <dependency name> minor version` will close this group update PR and stop
  Dependabot creating any more for the specific dependency's minor version (unless you unignore this
  specific dependency's minor version or upgrade to it yourself) - `@dependabot ignore <dependency
  name>` will close this group update PR and stop Dependabot creating any more for the specific
  dependency (unless you unignore this specific dependency or upgrade to it yourself) - `@dependabot
  unignore <dependency name>` will remove all of the ignore conditions of the specified dependency -
  `@dependabot unignore <dependency name> <ignore condition>` will remove the ignore condition of
  the specified dependency and ignore conditions You can disable automated security fix PRs for this
  repo from the [Security Alerts
  page](https://github.com/jakub-k-slys/substack-gateway-oss/network/alerts).

</details>

- **deps**: Bump python-multipart in the uv group across 1 directory
  ([`53c8102`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/53c8102416f713d4d47dffdc6f476471bafb2e46))

Bumps the uv group with 1 update in the / directory:
  [python-multipart](https://github.com/Kludex/python-multipart).

Updates `python-multipart` from 0.0.26 to 0.0.27 - [Release
  notes](https://github.com/Kludex/python-multipart/releases) -
  [Changelog](https://github.com/Kludex/python-multipart/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/Kludex/python-multipart/compare/0.0.26...0.0.27)

--- updated-dependencies: - dependency-name: python-multipart dependency-version: 0.0.27

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.15.11 to 0.15.12
  ([`04506f7`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/04506f76712eb111cc27103c6ced7dec9a952f11))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.11 to 0.15.12. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/0.15.11...0.15.12)

--- updated-dependencies: - dependency-name: ruff dependency-version: 0.15.12

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.15.11 to 0.15.12
  ([#32](https://github.com/jakub-k-slys/substack-gateway-oss/pull/32),
  [`4b1e1aa`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/4b1e1aaf3641aedaf364f54793aa6c42cce26601))

[//]: # (dependabot-start) ⚠️ **Dependabot is rebasing this PR** ⚠️

Rebasing might not happen immediately, so don't worry if this takes some time.

Note: if you make any changes to this PR yourself, they will take precedence over the rebase.

---

[//]: # (dependabot-end)

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.11 to 0.15.12. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.15.12</h2> <h2>Release Notes</h2> <p>Released on
  2026-04-24.</p> <h3>Preview features</h3> <ul> <li>Implement <code>#ruff:file-ignore</code>
  file-level suppressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23599">#23599</a>)</li> <li>Implement
  <code>#ruff:ignore</code> logical-line suppressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23404">#23404</a>)</li> <li>Revert preview
  changes to displayed diagnostic severity in LSP (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24789">#24789</a>)</li>
  <li>[<code>airflow</code>] Implement <code>task-branch-as-short-circuit</code>
  (<code>AIR004</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23579">#23579</a>)</li>
  <li>[<code>flake8-bugbear</code>] Fix <code>break</code>/<code>continue</code> handling in
  <code>loop-iterator-mutation</code> (<code>B909</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24440">#24440</a>)</li>
  <li>[<code>pylint</code>] Fix <code>PLC2701</code> for type parameter scopes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24576">#24576</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>pandas-vet</code>] Suggest <code>.array</code> as well in
  <code>PD011</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24805">#24805</a>)</li> </ul> <h3>CLI</h3>
  <ul> <li>Respect default Unix permissions for cache files (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24794">#24794</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>[<code>pylint</code>] Fix <code>PLR0124</code> description not to
  claim self-comparison always returns the same value (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24749">#24749</a>)</li>
  <li>[<code>pyupgrade</code>] Expand docs on reusable <code>TypeVar</code>s and scoping
  (<code>UP046</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24153">#24153</a>)</li> <li>Improve rules
  table accessibility (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24711">#24711</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/dylwil3"><code>@​dylwil3</code></a></li> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> <li><a
  href="https://github.com/woodruffw"><code>@​woodruffw</code></a></li> <li><a
  href="https://github.com/avasis-ai"><code>@​avasis-ai</code></a></li> <li><a
  href="https://github.com/Dev-iL"><code>@​Dev-iL</code></a></li> <li><a
  href="https://github.com/denyszhak"><code>@​denyszhak</code></a></li> <li><a
  href="https://github.com/ShipItAndPray"><code>@​ShipItAndPray</code></a></li> <li><a
  href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li> <li><a
  href="https://github.com/augustelalande"><code>@​augustelalande</code></a></li> <li><a
  href="https://github.com/amyreese"><code>@​amyreese</code></a></li> <li><a
  href="https://github.com/majiayu000"><code>@​majiayu000</code></a></li> </ul> <h2>Install ruff
  0.15.12</h2> <h3>Install prebuilt binaries via shell script</h3> <pre lang="sh"><code>curl --proto
  '=https' --tlsv1.2 -LsSf
  https://releases.astral.sh/github/ruff/releases/download/0.15.12/ruff-installer.sh | sh
  </code></pre> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details> <details>
  <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
  <blockquote> <h2>0.15.12</h2> <p>Released on 2026-04-24.</p> <h3>Preview features</h3> <ul>
  <li>Implement <code>#ruff:file-ignore</code> file-level suppressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23599">#23599</a>)</li> <li>Implement
  <code>#ruff:ignore</code> logical-line suppressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23404">#23404</a>)</li> <li>Revert preview
  changes to displayed diagnostic severity in LSP (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24789">#24789</a>)</li>
  <li>[<code>airflow</code>] Implement <code>task-branch-as-short-circuit</code>
  (<code>AIR004</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23579">#23579</a>)</li>
  <li>[<code>flake8-bugbear</code>] Fix <code>break</code>/<code>continue</code> handling in
  <code>loop-iterator-mutation</code> (<code>B909</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24440">#24440</a>)</li>
  <li>[<code>pylint</code>] Fix <code>PLC2701</code> for type parameter scopes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24576">#24576</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>pandas-vet</code>] Suggest <code>.array</code> as well in
  <code>PD011</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24805">#24805</a>)</li> </ul> <h3>CLI</h3>
  <ul> <li>Respect default Unix permissions for cache files (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24794">#24794</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>[<code>pylint</code>] Fix <code>PLR0124</code> description not to
  claim self-comparison always returns the same value (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24749">#24749</a>)</li>
  <li>[<code>pyupgrade</code>] Expand docs on reusable <code>TypeVar</code>s and scoping
  (<code>UP046</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24153">#24153</a>)</li> <li>Improve rules
  table accessibility (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24711">#24711</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/dylwil3"><code>@​dylwil3</code></a></li> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> <li><a
  href="https://github.com/woodruffw"><code>@​woodruffw</code></a></li> <li><a
  href="https://github.com/avasis-ai"><code>@​avasis-ai</code></a></li> <li><a
  href="https://github.com/Dev-iL"><code>@​Dev-iL</code></a></li> <li><a
  href="https://github.com/denyszhak"><code>@​denyszhak</code></a></li> <li><a
  href="https://github.com/ShipItAndPray"><code>@​ShipItAndPray</code></a></li> <li><a
  href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li> <li><a
  href="https://github.com/augustelalande"><code>@​augustelalande</code></a></li> <li><a
  href="https://github.com/amyreese"><code>@​amyreese</code></a></li> <li><a
  href="https://github.com/majiayu000"><code>@​majiayu000</code></a></li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ruff/commit/66f93cf7ed4d36325f35a452e4afa28268fbcd28"><code>66f93cf</code></a>
  Bump 0.15.12 (<a href="https://redirect.github.com/astral-sh/ruff/issues/24815">#24815</a>)</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/476a4d02e8e3b6c157ac39979d8b698a1b6baa91"><code>476a4d0</code></a>
  [ty] Complete support for more detailed diagnostics on possibly unbound error...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/ed669eab30095d6c51fe6cdef6050fb01276bcb3"><code>ed669ea</code></a>
  Implement <code>#ruff:file-ignore</code> file-level suppressions (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/23599">#23599</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/e73d952e43feb51356ee740c5a973fce81396ff6"><code>e73d952</code></a>
  [ty] Include inferred type in <code>invalid-key</code> concise diagnostic for union/inte...</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/80feb29b31cd98c093316df2e0407b0c70c01b55"><code>80feb29</code></a>
  [ty] report only dead annotation-only locals as unused (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24811">#24811</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/0fbf2bc27336a3d17d39af52cf89b78dcda8c7c8"><code>0fbf2bc</code></a>
  Drop deprecated license classifier (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24808">#24808</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/43b174cc7f2fcb0080bb1d4843cd4bf6b72bbe27"><code>43b174c</code></a>
  [ty] Infer lambda parameter types with <code>Callable</code> type context (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24317">#24317</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/4f449ae4a2377569330a5ab94799d389357b5a3f"><code>4f449ae</code></a>
  [ty] Add error context for intersection types (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24772">#24772</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/5b4e753acb46e96ad408e4904c15308e33efe307"><code>5b4e753</code></a>
  [ty] Add support for goto in literal enum member inlay hint (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24792">#24792</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/e7cc76275a758ce1c636ea1c2d091fd576aac794"><code>e7cc762</code></a>
  [ty] Add error context for TypedDict assignments (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24790">#24790</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.15.11...0.15.12">compare
  view</a></li> </ul> </details> <br />

- **deps-dev**: Bump ruff from 0.15.12 to 0.15.13
  ([`7b7cdbd`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/7b7cdbd321c403b797ef15002c38a1c0d89612af))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.12 to 0.15.13. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/0.15.12...0.15.13)

--- updated-dependencies: - dependency-name: ruff dependency-version: 0.15.13

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.15.12 to 0.15.13
  ([#41](https://github.com/jakub-k-slys/substack-gateway-oss/pull/41),
  [`95c04f1`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/95c04f15f1fc1c2a4c90f23d8ce9183b0c54d544))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.12 to 0.15.13. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.15.13</h2> <h2>Release Notes</h2> <p>Released on
  2026-05-14.</p> <h3>Preview features</h3> <ul> <li>Add a rule to flag lazy imports that are
  eagerly evaluated (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25016">#25016</a>)</li>
  <li>[<code>pylint</code>] Standardize diagnostic message (<code>PLR0914</code>,
  <code>PLR0917</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24996">#24996</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>Fix <code>F811</code> false positive for class methods (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24933">#24933</a>)</li> <li>Fix setting
  selection for multi-folder workspace (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24819">#24819</a>)</li>
  <li>[<code>eradicate</code>] Fix false positive for lines with leading whitespace
  (<code>ERA001</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25122">#25122</a>)</li>
  <li>[<code>flake8-pyi</code>] Fix false positive for f-string debug specifier
  (<code>PYI016</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24098">#24098</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>Always include panic payload in panic diagnostic message (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24873">#24873</a>)</li> <li>Restrict
  <code>PYI034</code> for in-place operations to enclosing class (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24511">#24511</a>)</li> <li>Improve error
  message for parameters that are declared <code>global</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24902">#24902</a>)</li> <li>Update known
  stdlib (<a href="https://redirect.github.com/astral-sh/ruff/pull/25103">#25103</a>)</li> </ul>
  <h3>Performance</h3> <ul> <li>[<code>isort</code>] Avoid constructing <code>glob::Pattern</code>s
  for literal known modules (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25123">#25123</a>)</li> </ul> <h3>CLI</h3>
  <ul> <li>Add TOML examples to <code>--config</code> help text (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25013">#25013</a>)</li> <li>Colorize ruff
  check 'All checks passed' (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25085">#25085</a>)</li> </ul>
  <h3>Configuration</h3> <ul> <li>Increase max allowed value of <code>line-length</code> setting (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24962">#24962</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Add <code>D203</code> to rules that conflict with the formatter
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/25044">#25044</a>)</li> <li>Clarify
  <code>COM819</code> and formatter interaction (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25045">#25045</a>)</li> <li>Clarify that
  <code>NotImplemented</code> is a value, not an exception (<code>F901</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25054">#25054</a>)</li> <li>Update number of
  lint rules supported (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24942">#24942</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Simplify the playground's markdown template (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24924">#24924</a>)</li> </ul>
  <h3>Contributors</h3> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details>
  <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
  <blockquote> <h2>0.15.13</h2> <p>Released on 2026-05-14.</p> <h3>Preview features</h3> <ul>
  <li>Add a rule to flag lazy imports that are eagerly evaluated (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25016">#25016</a>)</li>
  <li>[<code>pylint</code>] Standardize diagnostic message (<code>PLR0914</code>,
  <code>PLR0917</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24996">#24996</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>Fix <code>F811</code> false positive for class methods (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24933">#24933</a>)</li> <li>Fix setting
  selection for multi-folder workspace (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24819">#24819</a>)</li>
  <li>[<code>eradicate</code>] Fix false positive for lines with leading whitespace
  (<code>ERA001</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25122">#25122</a>)</li>
  <li>[<code>flake8-pyi</code>] Fix false positive for f-string debug specifier
  (<code>PYI016</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24098">#24098</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>Always include panic payload in panic diagnostic message (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24873">#24873</a>)</li> <li>Restrict
  <code>PYI034</code> for in-place operations to enclosing class (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24511">#24511</a>)</li> <li>Improve error
  message for parameters that are declared <code>global</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24902">#24902</a>)</li> <li>Update known
  stdlib (<a href="https://redirect.github.com/astral-sh/ruff/pull/25103">#25103</a>)</li> </ul>
  <h3>Performance</h3> <ul> <li>[<code>isort</code>] Avoid constructing <code>glob::Pattern</code>s
  for literal known modules (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25123">#25123</a>)</li> </ul> <h3>CLI</h3>
  <ul> <li>Add TOML examples to <code>--config</code> help text (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25013">#25013</a>)</li> <li>Colorize ruff
  check 'All checks passed' (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25085">#25085</a>)</li> </ul>
  <h3>Configuration</h3> <ul> <li>Increase max allowed value of <code>line-length</code> setting (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24962">#24962</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Add <code>D203</code> to rules that conflict with the formatter
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/25044">#25044</a>)</li> <li>Clarify
  <code>COM819</code> and formatter interaction (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25045">#25045</a>)</li> <li>Clarify that
  <code>NotImplemented</code> is a value, not an exception (<code>F901</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25054">#25054</a>)</li> <li>Update number of
  lint rules supported (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24942">#24942</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Simplify the playground's markdown template (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24924">#24924</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> </ul> <!-- raw HTML
  omitted --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Commits</summary>
  <ul> <li><a
  href="https://github.com/astral-sh/ruff/commit/2afb467ce397e4a89c13a0a814c62cfecb0e9e49"><code>2afb467</code></a>
  Bump 0.15.13 (<a href="https://redirect.github.com/astral-sh/ruff/issues/25157">#25157</a>)</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/300879600fa3af7cde1e675c63de6ad9d0797d1b"><code>3008796</code></a>
  [ty] classify TypeVar semantic tokens as type parameters (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24891">#24891</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/79470e31877acb6074f3bbff2a49e508822ae4e8"><code>79470e3</code></a>
  [<code>isort</code>] Avoid constructing <code>glob::Pattern</code>s for literal known modules (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/25123">#25123</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/2522549901d50f18775999f0fb802b19229417f0"><code>2522549</code></a>
  Remove shellcheck from prek (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/25154">#25154</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/7db7170020f539d6d2bc01dbd0b0c09fab91dc06"><code>7db7170</code></a>
  [ty] Support TypedDict key completions in incomplete, anonymous contexts (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/25">#25</a>...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/bb3dd535f1c5a83e2e56ac93a771fadbeeceebd0"><code>bb3dd53</code></a>
  [ty] Run full iteration analysis on narrowed typevars (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/25143">#25143</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/828cdb7732efcb16a53f4ee5f011cf653b834d1a"><code>828cdb7</code></a>
  [ty] Isolate file-watching test environment (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/25151">#25151</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/89e1d8670ea4d3af60c8143ee552dc750200718d"><code>89e1d86</code></a>
  [ty] Preserve TypedDict keys through dict unpacking (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24523">#24523</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/86f3064d6fffa5697d174f26b840bd6857b381da"><code>86f3064</code></a>
  [ty] Avoid accessing <code>args[0]</code> for <code>static_assert</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/25149">#25149</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/ed819f947dc27e36eac8bb3134153c4668d76a3a"><code>ed819f9</code></a>
  [ty] Treat custom enum <code>__new__</code> values as dynamic (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/25136">#25136</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.15.12...0.15.13">compare
  view</a></li> </ul> </details> <br />

- **deps-dev**: Bump ruff from 0.15.13 to 0.15.14
  ([`6b99edf`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/6b99edff2dd657c7dd8b88b641d201bf626ce9a8))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.13 to 0.15.14. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/commits)

--- updated-dependencies: - dependency-name: ruff dependency-version: 0.15.14

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.15.13 to 0.15.14
  ([#45](https://github.com/jakub-k-slys/substack-gateway-oss/pull/45),
  [`d48fd25`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/d48fd25d238d41f7ecc6323e211d6f400d330e3a))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.13 to 0.15.14. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.15.14</h2> <h2>Release Notes</h2> <p>Released on
  2026-05-21.</p> <h3>Preview features</h3> <ul> <li>[<code>airflow</code>] Implement
  <code>airflow-task-implicit-multiple-outputs</code> (<code>AIR202</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25152">#25152</a>)</li>
  <li>[<code>flake8-use-pathlib</code>] Mark <code>PTH101</code> fix as unsafe when first argument
  is a class attribute annotated as <code>int</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25086">#25086</a>)</li>
  <li>[<code>pylint</code>] Implement <code>too-many-try-statements</code> (<code>W0717</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23970">#23970</a>)</li>
  <li>[<code>ruff</code>] Add <code>incorrect-decorator-order</code> (<code>RUF074</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23461">#23461</a>)</li>
  <li>[<code>ruff</code>] Add <code>fallible-context-manager</code> (<code>RUF075</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/22844">#22844</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>Fix lambda formatting in interpolated string expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25144">#25144</a>)</li> <li>Treat generic
  <code>frozenset</code> annotations as immutable (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25251">#25251</a>)</li>
  <li>[<code>flake8-type-checking</code>] Avoid <code>strict</code> behavior when
  <code>future-annotations</code> are enabled (<code>TC001</code>, <code>TC002</code>,
  <code>TC003</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25035">#25035</a>)</li>
  <li>[<code>pylint</code>] Avoid false positives in <code>else</code> clause (<code>PLR1733</code>)
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/25177">#25177</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>flake8-comprehensions</code>] Skip <code>C417</code> for lambdas with
  positional-only parameters (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25272">#25272</a>)</li>
  <li>[<code>flake8-simplify</code>] Preserve f-string source verbatim in <code>SIM101</code> fix
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/25061">#25061</a>)</li> </ul>
  <h3>Performance</h3> <ul> <li>Avoid unnecessary parser lookahead for operators (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25290">#25290</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Update code example setting Neovim LSP log level (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25284">#25284</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Add full PEP 798 support (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25104">#25104</a>)</li> <li>Add a parser
  recursion limit (<a href="https://redirect.github.com/astral-sh/ruff/pull/24810">#24810</a>)</li>
  <li>Update various <code>ruff_python_stdlib</code> APIs (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25273">#25273</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/ocaballeror"><code>@​ocaballeror</code></a></li> <li><a
  href="https://github.com/lerebear"><code>@​lerebear</code></a></li> <li><a
  href="https://github.com/samuelcolvin"><code>@​samuelcolvin</code></a></li> <li><a
  href="https://github.com/baltasarblanco"><code>@​baltasarblanco</code></a></li> <li><a
  href="https://github.com/aconal-com"><code>@​aconal-com</code></a></li> <li><a
  href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li> <li><a
  href="https://github.com/JelleZijlstra"><code>@​JelleZijlstra</code></a></li> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> <li><a
  href="https://github.com/ntBre"><code>@​ntBre</code></a></li> </ul> <!-- raw HTML omitted -->
  </blockquote> <p>... (truncated)</p> </details> <details> <summary>Changelog</summary>
  <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
  changelog</a>.</em></p> <blockquote> <h2>0.15.14</h2> <p>Released on 2026-05-21.</p> <h3>Preview
  features</h3> <ul> <li>[<code>airflow</code>] Implement
  <code>airflow-task-implicit-multiple-outputs</code> (<code>AIR202</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25152">#25152</a>)</li>
  <li>[<code>flake8-use-pathlib</code>] Mark <code>PTH101</code> fix as unsafe when first argument
  is a class attribute annotated as <code>int</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25086">#25086</a>)</li>
  <li>[<code>pylint</code>] Implement <code>too-many-try-statements</code> (<code>W0717</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23970">#23970</a>)</li>
  <li>[<code>ruff</code>] Add <code>incorrect-decorator-order</code> (<code>RUF074</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23461">#23461</a>)</li>
  <li>[<code>ruff</code>] Add <code>fallible-context-manager</code> (<code>RUF075</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/22844">#22844</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>Fix lambda formatting in interpolated string expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25144">#25144</a>)</li> <li>Treat generic
  <code>frozenset</code> annotations as immutable (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25251">#25251</a>)</li>
  <li>[<code>flake8-type-checking</code>] Avoid <code>strict</code> behavior when
  <code>future-annotations</code> are enabled (<code>TC001</code>, <code>TC002</code>,
  <code>TC003</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25035">#25035</a>)</li>
  <li>[<code>pylint</code>] Avoid false positives in <code>else</code> clause (<code>PLR1733</code>)
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/25177">#25177</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>flake8-comprehensions</code>] Skip <code>C417</code> for lambdas with
  positional-only parameters (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25272">#25272</a>)</li>
  <li>[<code>flake8-simplify</code>] Preserve f-string source verbatim in <code>SIM101</code> fix
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/25061">#25061</a>)</li> </ul>
  <h3>Performance</h3> <ul> <li>Avoid unnecessary parser lookahead for operators (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25290">#25290</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Update code example setting Neovim LSP log level (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25284">#25284</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Add full PEP 798 support (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25104">#25104</a>)</li> <li>Add a parser
  recursion limit (<a href="https://redirect.github.com/astral-sh/ruff/pull/24810">#24810</a>)</li>
  <li>Update various <code>ruff_python_stdlib</code> APIs (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25273">#25273</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/ocaballeror"><code>@​ocaballeror</code></a></li> <li><a
  href="https://github.com/lerebear"><code>@​lerebear</code></a></li> <li><a
  href="https://github.com/samuelcolvin"><code>@​samuelcolvin</code></a></li> <li><a
  href="https://github.com/baltasarblanco"><code>@​baltasarblanco</code></a></li> <li><a
  href="https://github.com/aconal-com"><code>@​aconal-com</code></a></li> <li><a
  href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li> <li><a
  href="https://github.com/JelleZijlstra"><code>@​JelleZijlstra</code></a></li> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> <li><a
  href="https://github.com/ntBre"><code>@​ntBre</code></a></li> <li><a
  href="https://github.com/adityasingh2400"><code>@​adityasingh2400</code></a></li> </ul> <!-- raw
  HTML omitted --> </blockquote> <p>... (truncated)</p> </details> <details>
  <summary>Commits</summary> <ul> <li>See full diff in <a
  href="https://github.com/astral-sh/ruff/commits">compare view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ruff&package-manager=uv&previous-version=0.15.13&new-version=0.15.14)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ty from 0.0.32 to 0.0.33
  ([`3feca4d`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/3feca4d1d593821ca62b5e6020a58011f2162386))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.32 to 0.0.33. - [Release
  notes](https://github.com/astral-sh/ty/releases) -
  [Changelog](https://github.com/astral-sh/ty/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ty/compare/0.0.32...0.0.33)

--- updated-dependencies: - dependency-name: ty dependency-version: 0.0.33

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ty from 0.0.32 to 0.0.33
  ([#31](https://github.com/jakub-k-slys/substack-gateway-oss/pull/31),
  [`c79a923`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/c79a92305ae9f6b2d1b6f4519c697b2f0d06424c))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.32 to 0.0.33. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ty/releases">ty's
  releases</a>.</em></p> <blockquote> <h2>0.0.33</h2> <h2>Release Notes</h2> <p>Released on
  2026-04-28.</p> <h3>Notable changes</h3> <ul> <li> <p>ty now prefers the declared type of an
  annotated assignment in more situations (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24802">#24802</a>). Consider this
  example:</p> <pre lang="py"><code>from some_library import untyped_function <p>threshold: int |
  None = 0 result: str = untyped_function() </code></pre></p> <p>ty previously favored the
  <em>inferred</em> type of the right hand side expression when <code>threshold</code> and
  <code>result</code> were used. This is useful for <code>threshold</code>, as it allows something
  like <code>threshold += 1</code> to work without an error: we know that <code>threshold</code>
  could later become <code>None</code>, but <em>right now</em>, we see that it is an
  <code>int</code>. However, for <code>result</code>, the inferred type is <code>Unknown</code>.
  This is <em>not</em> a useful type and it can lead to false negatives. Starting with this release,
  ty will therefore prefer the declared type <em>if the inferred and declared types are mutually
  assignable</em>. In the above example, <code>threshold</code> will still be inferred as
  <code>int</code> (or rather <code>Literal[1]</code>), but <code>result</code> will now be inferred
  as <code>str</code>. If you previously added <code>cast</code>s to work around this behavior, you
  should be able to remove them after upgrading.</p> </li> </ul> <h3>Bug fixes</h3> <ul> <li>Fix
  reporting of annotation-only locals as unused (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24811">#24811</a>)</li> <li>Fix project and
  workspace selection (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24824">#24824</a>)</li> <li>Fix go-to
  definition for generic classes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24714">#24714</a>)</li> <li>Fix receiver
  coloring for aliased decorators (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24884">#24884</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Add support for go-to definition in literal enum member inlay hints (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24792">#24792</a>)</li> <li>Add support for
  &quot;baking&quot; keyword argument inlay hints into the source code (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24667">#24667</a>)</li> <li>Don't allow
  inlay hint edits when introducing a non global scope symbol (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24797">#24797</a>)</li> <li>Omit semantic
  highlighting for unresolved symbols (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24718">#24718</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Support narrowing with aliased conditional expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24302">#24302</a>)</li> <li>Model
  short-circuiting control flow in Boolean expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24458">#24458</a>)</li> <li>Handle
  <code>finally</code> blocks where all <code>try</code>/<code>except</code> blocks are terminal (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24882">#24882</a>)</li> <li>Detect invalid
  <code>ClassVar</code> vs instance-attribute overrides (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24767">#24767</a>)</li> <li>Emit diagnostic
  for invalid uses of <code>Unpack[...]</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24868">#24868</a>)</li> <li>Infer lambda
  parameter types with <code>Callable</code> type context (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24317">#24317</a>)</li> <li>Support
  <code>**</code> unpacking of <code>TypedDict</code> in dict-literal assignments (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24703">#24703</a>)</li> <li>Support
  <code>Unpack[TypedDict]</code> in <code>**kwargs</code> signatures (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24653">#24653</a>)</li> <li>Treat
  <code>[*xs]</code> as an irrefutable pattern when matching on <code>Sequence</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24787">#24787</a>)</li> <li>Improve generics
  solving for unions in invariant positions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24698">#24698</a>)</li> <li>Improve generics
  solving for unions when matching against protocols (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24837">#24837</a>)</li> </ul>
  <h3>Diagnostics</h3> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details>
  <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ty/blob/main/CHANGELOG.md">ty's changelog</a>.</em></p>
  <blockquote> <h2>0.0.33</h2> <p>Released on 2026-04-28.</p> <h3>Notable changes</h3> <ul> <li>
  <p>ty now prefers the declared type of an annotated assignment in more situations (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24802">#24802</a>). Consider this
  example:</p> <pre lang="py"><code>from some_library import untyped_function <p>threshold: int |
  None = 0 result: str = untyped_function() </code></pre></p> <p>ty previously favored the
  <em>inferred</em> type of the right hand side expression when <code>threshold</code> and
  <code>result</code> were used. This is useful for <code>threshold</code>, as it allows something
  like <code>threshold += 1</code> to work without an error: we know that <code>threshold</code>
  could later become <code>None</code>, but <em>right now</em>, we see that it is an
  <code>int</code>. However, for <code>result</code>, the inferred type is <code>Unknown</code>.
  This is <em>not</em> a useful type and it can lead to false negatives. Starting with this release,
  ty will therefore prefer the declared type <em>if the inferred and declared types are mutually
  assignable</em>. In the above example, <code>threshold</code> will still be inferred as
  <code>int</code> (or rather <code>Literal[1]</code>), but <code>result</code> will now be inferred
  as <code>str</code>. If you previously added <code>cast</code>s to work around this behavior, you
  should be able to remove them after upgrading.</p> </li> </ul> <h3>Bug fixes</h3> <ul> <li>Fix
  reporting of annotation-only locals as unused (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24811">#24811</a>)</li> <li>Fix project and
  workspace selection (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24824">#24824</a>)</li> <li>Fix go-to
  definition for generic classes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24714">#24714</a>)</li> <li>Fix receiver
  coloring for aliased decorators (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24884">#24884</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Add support for go-to definition in literal enum member inlay hints (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24792">#24792</a>)</li> <li>Add support for
  &quot;baking&quot; keyword argument inlay hints into the source code (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24667">#24667</a>)</li> <li>Don't allow
  inlay hint edits when introducing a non global scope symbol (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24797">#24797</a>)</li> <li>Omit semantic
  highlighting for unresolved symbols (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24718">#24718</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Support narrowing with aliased conditional expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24302">#24302</a>)</li> <li>Model
  short-circuiting control flow in Boolean expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24458">#24458</a>)</li> <li>Handle
  <code>finally</code> blocks where all <code>try</code>/<code>except</code> blocks are terminal (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24882">#24882</a>)</li> <li>Detect invalid
  <code>ClassVar</code> vs instance-attribute overrides (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24767">#24767</a>)</li> <li>Emit diagnostic
  for invalid uses of <code>Unpack[...]</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24868">#24868</a>)</li> <li>Infer lambda
  parameter types with <code>Callable</code> type context (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24317">#24317</a>)</li> <li>Support
  <code>**</code> unpacking of <code>TypedDict</code> in dict-literal assignments (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24703">#24703</a>)</li> <li>Support
  <code>Unpack[TypedDict]</code> in <code>**kwargs</code> signatures (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24653">#24653</a>)</li> <li>Treat
  <code>[*xs]</code> as an irrefutable pattern when matching on <code>Sequence</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24787">#24787</a>)</li> <li>Improve generics
  solving for unions in invariant positions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24698">#24698</a>)</li> <li>Improve generics
  solving for unions when matching against protocols (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24837">#24837</a>)</li> </ul>
  <h3>Diagnostics</h3> <ul> <li>Add error context to <code>invalid-return-type</code> diagnostics,
  <code>invalid-yield</code> diagnostics, attribute assignment diagnostics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24770">#24770</a>, <a
  href="https://redirect.github.com/astral-sh/ruff/pull/24771">#24771</a>)</li> </ul> <!-- raw HTML
  omitted --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Commits</summary>
  <ul> <li><a
  href="https://github.com/astral-sh/ty/commit/c512d8425418a2170e92aa7fbbd70952d4e04118"><code>c512d84</code></a>
  Bump version to 0.0.33 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3368">#3368</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/4cd7b334b90eba09042700e7b654044c2d6bcd15"><code>4cd7b33</code></a>
  Upgrade Depot runners from macOS 14 to 15 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3363">#3363</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/c78b8324515bf15a662f61e1d74fd85484d67e8c"><code>c78b832</code></a>
  Update rui314/setup-mold digest to 9c9c13b (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3342">#3342</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/dea338134aef96d741a48886e414f622dbf10426"><code>dea3381</code></a>
  Update actions/cache action to v5.0.5 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3343">#3343</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/d451af477bd5517e132609c3b016799d697f4182"><code>d451af4</code></a>
  update typing-features and faqs (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3335">#3335</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/052d70bc1a7457f50c5acbafe8de7a846f7d5e77"><code>052d70b</code></a>
  Update prek dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3344">#3344</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/66b5e878163ce4ab4810a45a2679a98011932b8b"><code>66b5e87</code></a>
  Update astral-sh/setup-uv action to v8.1.0 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3345">#3345</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/7ec6712a6f02d0255de4c7f0066d5bb23987a9bb"><code>7ec6712</code></a>
  Add a 'Diagnostics improvements' section to the changelogs (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3309">#3309</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/978dfdb38dfb568943f73779d769a965c1d5a397"><code>978dfdb</code></a>
  Add version metadata publishing to the release process (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3292">#3292</a>)</li> <li>See full diff in
  <a href="https://github.com/astral-sh/ty/compare/0.0.32...0.0.33">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ty&package-manager=uv&previous-version=0.0.32&new-version=0.0.33)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ty from 0.0.33 to 0.0.34
  ([`ea62bed`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/ea62bedbfa2a06a0e4325621d50cf31ee03fc5de))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.33 to 0.0.34. - [Release
  notes](https://github.com/astral-sh/ty/releases) -
  [Changelog](https://github.com/astral-sh/ty/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ty/compare/0.0.33...0.0.34)

--- updated-dependencies: - dependency-name: ty dependency-version: 0.0.34

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ty from 0.0.33 to 0.0.34
  ([#34](https://github.com/jakub-k-slys/substack-gateway-oss/pull/34),
  [`4b26685`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/4b26685c4c1e8fe676b82f5ec0ff3a44a852c61d))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.33 to 0.0.34. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ty/releases">ty's
  releases</a>.</em></p> <blockquote> <h2>0.0.34</h2> <h2>Release Notes</h2> <p>Released on
  2026-05-01.</p> <h3>Bug fixes</h3> <ul> <li>Avoid panic in recursive protocol signature
  comparisons (<a href="https://redirect.github.com/astral-sh/ruff/pull/24665">#24665</a>)</li>
  <li>Avoid panics for syntax error targets in invalid unpacking assignments (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24663">#24663</a>)</li> <li>Fix unbounded
  type growth in nested-typevar substitutions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24803">#24803</a>)</li> <li>Prevent string
  annotation tokens from leaking across notebook cells (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24919">#24919</a>)</li> <li>Support
  reference finding in stringified annotations (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24956">#24956</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Add hover support for PEP 695 type aliases (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24926">#24926</a>)</li> <li>Offer string
  literal completion suggestions based on expected type (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24555">#24555</a>)</li> <li>Support Go-to
  Definition, Go-To Declaration, and Find References for TypedDict and NamedTuple initializers (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24897">#24897</a>)</li> <li>Support
  <code>Annotated</code> metadata in semantic tokens (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24890">#24890</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Add support for <code>functools.partial</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24582">#24582</a>)</li> <li>Fix ParamSpec
  defaults and alias variance (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24479">#24479</a>)</li> <li>Fix
  <code>TypeIs</code> assignability with gradual types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24928">#24928</a>)</li> <li>Infer
  <code>dict(**TypedDict)</code> in <code>TypedDict</code> context (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24709">#24709</a>)</li> <li>Support
  <code>infer_variance</code> for legacy <code>TypeVar</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24930">#24930</a>)</li> <li>Support variance
  keywords in <code>ParamSpec</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24927">#24927</a>)</li> <li>Sync vendored
  typeshed stubs (<a href="https://redirect.github.com/astral-sh/ruff/pull/24952">#24952</a>). <a
  href="https://github.com/python/typeshed/compare/c03c2b926422c82ab680d27f3ad2491845000802...e4d32e01bee44241a5e7c33298c261175b9f1bdb">Typeshed
  diff</a></li> <li>Unpack <code>Union</code> of <code>TypedDict</code> in various sites (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24958">#24958</a>)</li> </ul>
  <h3>Diagnostics</h3> <ul> <li>Add missing error context node for protocol to protocol
  assignability (<a href="https://redirect.github.com/astral-sh/ruff/pull/24905">#24905</a>)</li>
  <li>Show a diagnostic for unsupported inferred Python version (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24581">#24581</a>)</li> </ul>
  <h3>Performance</h3> <ul> <li>Lazily build TypeVar accumulations (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24782">#24782</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/sharkdp"><code>@​sharkdp</code></a></li> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/lerebear"><code>@​lerebear</code></a></li> <li><a
  href="https://github.com/MatthewMckee4"><code>@​MatthewMckee4</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/mtshiba"><code>@​mtshiba</code></a></li> <li><a
  href="https://github.com/Minibrams"><code>@​Minibrams</code></a></li> <li><a
  href="https://github.com/denyszhak"><code>@​denyszhak</code></a></li> </ul> <!-- raw HTML omitted
  --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Changelog</summary>
  <p><em>Sourced from <a href="https://github.com/astral-sh/ty/blob/main/CHANGELOG.md">ty's
  changelog</a>.</em></p> <blockquote> <h2>0.0.34</h2> <p>Released on 2026-05-01.</p> <h3>Bug
  fixes</h3> <ul> <li>Avoid panic in recursive protocol signature comparisons (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24665">#24665</a>)</li> <li>Avoid panics for
  syntax error targets in invalid unpacking assignments (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24663">#24663</a>)</li> <li>Fix unbounded
  type growth in nested-typevar substitutions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24803">#24803</a>)</li> <li>Prevent string
  annotation tokens from leaking across notebook cells (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24919">#24919</a>)</li> <li>Support
  reference finding in stringified annotations (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24956">#24956</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Add hover support for PEP 695 type aliases (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24926">#24926</a>)</li> <li>Offer string
  literal completion suggestions based on expected type (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24555">#24555</a>)</li> <li>Support Go-to
  Definition, Go-To Declaration, and Find References for TypedDict and NamedTuple initializers (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24897">#24897</a>)</li> <li>Support
  <code>Annotated</code> metadata in semantic tokens (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24890">#24890</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Add support for <code>functools.partial</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24582">#24582</a>)</li> <li>Fix ParamSpec
  defaults and alias variance (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24479">#24479</a>)</li> <li>Fix
  <code>TypeIs</code> assignability with gradual types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24928">#24928</a>)</li> <li>Infer
  <code>dict(**TypedDict)</code> in <code>TypedDict</code> context (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24709">#24709</a>)</li> <li>Support
  <code>infer_variance</code> for legacy <code>TypeVar</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24930">#24930</a>)</li> <li>Support variance
  keywords in <code>ParamSpec</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24927">#24927</a>)</li> <li>Sync vendored
  typeshed stubs (<a href="https://redirect.github.com/astral-sh/ruff/pull/24952">#24952</a>). <a
  href="https://github.com/python/typeshed/compare/c03c2b926422c82ab680d27f3ad2491845000802...e4d32e01bee44241a5e7c33298c261175b9f1bdb">Typeshed
  diff</a></li> <li>Unpack <code>Union</code> of <code>TypedDict</code> in various sites (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24958">#24958</a>)</li> </ul>
  <h3>Diagnostics</h3> <ul> <li>Add missing error context node for protocol to protocol
  assignability (<a href="https://redirect.github.com/astral-sh/ruff/pull/24905">#24905</a>)</li>
  <li>Show a diagnostic for unsupported inferred Python version (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24581">#24581</a>)</li> </ul>
  <h3>Performance</h3> <ul> <li>Lazily build TypeVar accumulations (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24782">#24782</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/sharkdp"><code>@​sharkdp</code></a></li> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/lerebear"><code>@​lerebear</code></a></li> <li><a
  href="https://github.com/MatthewMckee4"><code>@​MatthewMckee4</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/mtshiba"><code>@​mtshiba</code></a></li> <li><a
  href="https://github.com/Minibrams"><code>@​Minibrams</code></a></li> <li><a
  href="https://github.com/denyszhak"><code>@​denyszhak</code></a></li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ty/commit/d00448eb0204e2dd11943d21e8e08a225914775f"><code>d00448e</code></a>
  Bump version to 0.0.34 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3392">#3392</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/e9e4c909d806d0fc4f7e84192bc15fb01aa3b95c"><code>e9e4c90</code></a>
  docs: Reference correct issue in FAQ regarding strict mode (<a

href="https://redirect.github.com/astral-sh/ty/issues/3385">#3385</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/1b70eae97ede0d2528c3658b85bafe813f718a43"><code>1b70eae</code></a>
  Release: move 'diagnostics' section further down (<a

href="https://redirect.github.com/astral-sh/ty/issues/3373">#3373</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/d439e376ceca70453723cae44b2e61b3f3a6a2f6"><code>d439e37</code></a>
  CHANGELOG: Rename to 'Notable changes' (<a

href="https://redirect.github.com/astral-sh/ty/issues/3372">#3372</a>)</li> <li>See full diff in <a
  href="https://github.com/astral-sh/ty/compare/0.0.33...0.0.34">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ty&package-manager=uv&previous-version=0.0.33&new-version=0.0.34)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ty from 0.0.34 to 0.0.35
  ([`191c198`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/191c1981a727d293b5414df2523bb64a286a9e91))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.34 to 0.0.35. - [Release
  notes](https://github.com/astral-sh/ty/releases) -
  [Changelog](https://github.com/astral-sh/ty/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ty/compare/0.0.34...0.0.35)

--- updated-dependencies: - dependency-name: ty dependency-version: 0.0.35

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ty from 0.0.34 to 0.0.35
  ([#37](https://github.com/jakub-k-slys/substack-gateway-oss/pull/37),
  [`684b1b6`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/684b1b6a81970deab8d3d320fe58e25ac530d16e))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.34 to 0.0.35. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ty/releases">ty's
  releases</a>.</em></p> <blockquote> <h2>0.0.35</h2> <h2>Release Notes</h2> <p>Released on
  2026-05-10.</p> <h3>Bug fixes</h3> <ul> <li>Allow ParamSpec specialization through unioned generic
  classes (<a href="https://redirect.github.com/astral-sh/ruff/pull/24826">#24826</a>)</li> <li>Fix
  cross-file find-references for keyword arguments (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25043">#25043</a>)</li> <li>Fix comparison
  between negative and positive literal integers (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25023">#25023</a>)</li> <li>Reject dataclass
  decorator parameters based on supported Python version (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25029">#25029</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Adjust start of block folding range to preserve visible header for
  character-precise LSP clients. (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24917">#24917</a>)</li> <li>Emit folding
  ranges from the language server for multi-line block headers. (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24978">#24978</a>)</li> <li>Skip global
  search for references if identifier is not externally visible (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25033">#25033</a>)</li> <li>Speed-up
  find-references by using multithreading for cross-file searches (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25042">#25042</a>)</li> </ul> <h3>CLI</h3>
  <ul> <li>Include severity in JUnit diagnostics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25080">#25080</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Check non-generic overload implementations (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24936">#24936</a>)</li> <li>Expand support
  for narrowing within walruses (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24968">#24968</a>)</li> <li>Filter overloads
  based on return type for ParamSpec mapping (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24769">#24769</a>)</li> <li>Improve support
  for recursive types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24773">#24773</a>)</li> <li>Include
  TypedDict type context when inferring mixed constructors (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25039">#25039</a>)</li> <li>Include
  TypedDict type context when inferring string keys (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25037">#25037</a>)</li> <li>Preserve NewType
  and TypeAliasType in implicit aliases (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25072">#25072</a>)</li> <li>Provide type
  cntext for generator expression yields (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25069">#25069</a>)</li> <li>Provide type
  context for boolean operands (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25070">#25070</a>)</li> <li>Selectively
  promote a union of homogeneous fixed-length tuples to a single variadic tuple (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24705">#24705</a>)</li> <li>Support
  narrowing on <code>__class__</code> checks (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24997">#24997</a>)</li> <li>Use more precise
  exception types when catching a union (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25076">#25076</a>)</li> </ul>
  <h3>Diagnostics</h3> <ul> <li>Include error context for overload consistency diagnostics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24950">#24950</a>)</li> </ul>
  <h3>Performance</h3> <ul> <li>Cache results in desperate module resolution (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24977">#24977</a>)</li> <li>Lazily
  initialize builder when transforming a union type (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24929">#24929</a>)</li> <li>Project
  reachability constraints before narrowing (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24982">#24982</a>)</li> <li>Skip parameter
  accumulation for object variadics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24976">#24976</a>)</li> </ul>
  <h3>Contributors</h3> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details>
  <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ty/blob/main/CHANGELOG.md">ty's changelog</a>.</em></p>
  <blockquote> <h2>0.0.35</h2> <p>Released on 2026-05-10.</p> <h3>Bug fixes</h3> <ul> <li>Allow
  ParamSpec specialization through unioned generic classes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24826">#24826</a>)</li> <li>Fix cross-file
  find-references for keyword arguments (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25043">#25043</a>)</li> <li>Fix comparison
  between negative and positive literal integers (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25023">#25023</a>)</li> <li>Reject dataclass
  decorator parameters based on supported Python version (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25029">#25029</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Adjust start of block folding range to preserve visible header for
  character-precise LSP clients. (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24917">#24917</a>)</li> <li>Emit folding
  ranges from the language server for multi-line block headers. (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24978">#24978</a>)</li> <li>Skip global
  search for references if identifier is not externally visible (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25033">#25033</a>)</li> <li>Speed-up
  find-references by using multithreading for cross-file searches (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25042">#25042</a>)</li> </ul> <h3>CLI</h3>
  <ul> <li>Include severity in JUnit diagnostics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25080">#25080</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Check non-generic overload implementations (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24936">#24936</a>)</li> <li>Expand support
  for narrowing within walruses (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24968">#24968</a>)</li> <li>Filter overloads
  based on return type for ParamSpec mapping (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24769">#24769</a>)</li> <li>Improve support
  for recursive types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24773">#24773</a>)</li> <li>Include
  TypedDict type context when inferring mixed constructors (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25039">#25039</a>)</li> <li>Include
  TypedDict type context when inferring string keys (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25037">#25037</a>)</li> <li>Preserve NewType
  and TypeAliasType in implicit aliases (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25072">#25072</a>)</li> <li>Provide type
  cntext for generator expression yields (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25069">#25069</a>)</li> <li>Provide type
  context for boolean operands (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25070">#25070</a>)</li> <li>Selectively
  promote a union of homogeneous fixed-length tuples to a single variadic tuple (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24705">#24705</a>)</li> <li>Support
  narrowing on <code>__class__</code> checks (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24997">#24997</a>)</li> <li>Use more precise
  exception types when catching a union (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25076">#25076</a>)</li> </ul>
  <h3>Diagnostics</h3> <ul> <li>Include error context for overload consistency diagnostics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24950">#24950</a>)</li> </ul>
  <h3>Performance</h3> <ul> <li>Cache results in desperate module resolution (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24977">#24977</a>)</li> <li>Lazily
  initialize builder when transforming a union type (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24929">#24929</a>)</li> <li>Project
  reachability constraints before narrowing (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24982">#24982</a>)</li> <li>Skip parameter
  accumulation for object variadics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24976">#24976</a>)</li> </ul>
  <h3>Contributors</h3> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details>
  <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ty/commit/bc12d1cade50bc9407486057116fa0538bfb31ac"><code>bc12d1c</code></a>
  Bump version to 0.0.35 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3436">#3436</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/fb34d89e4acb379f6d8239d338881a6d1cce6642"><code>fb34d89</code></a>
  Build riscv64 manylinux binary (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3402">#3402</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/05def00f5eb67a599b314e1d550b4ce07ae08727"><code>05def00</code></a>
  Update maturin to v1.13.1 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3417">#3417</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/569c081af4159100bfe7be97624da9ef9910d8c8"><code>569c081</code></a>
  Update prek dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3416">#3416</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/608f8ff6e705b656392a89a1cf4e0b977fb10ab4"><code>608f8ff</code></a>
  Update renovate configuration (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3379">#3379</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/518b61d7c2a2eff95e8826a9bba4a392574258b0"><code>518b61d</code></a>
  Update uraimo/run-on-arch-action action to v3.1.0 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3405">#3405</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/55429594f26e78d277b29aaadc10ca46f9277148"><code>5542959</code></a>
  Update pre-commit hook astral-sh/ruff-pre-commit to v0.15.12 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3404">#3404</a>)</li> <li>See full diff in
  <a href="https://github.com/astral-sh/ty/compare/0.0.34...0.0.35">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ty&package-manager=uv&previous-version=0.0.34&new-version=0.0.35)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ty from 0.0.35 to 0.0.38
  ([`2424d53`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/2424d53d8cd298b2686b8a93ad3809aaefee5d24))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.35 to 0.0.38. - [Release
  notes](https://github.com/astral-sh/ty/releases) -
  [Changelog](https://github.com/astral-sh/ty/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ty/compare/0.0.35...0.0.38)

--- updated-dependencies: - dependency-name: ty dependency-version: 0.0.38

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ty from 0.0.35 to 0.0.38
  ([#43](https://github.com/jakub-k-slys/substack-gateway-oss/pull/43),
  [`c4c3174`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/c4c317432a65e8831f799c9dffc24768058936f6))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.35 to 0.0.38. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ty/releases">ty's
  releases</a>.</em></p> <blockquote> <h2>0.0.38</h2> <h2>Release Notes</h2> <p>Released on
  2026-05-19.</p> <h3>Bug fixes</h3> <ul> <li>Fix panic in enum literal during cycle recovery (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25237">#25237</a>)</li> <li>Fix panic from
  lazy <code>NewType</code> base expansion during cycle recovery (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25234">#25234</a>)</li> <li>Fix class-body
  global lookup before class binding (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25224">#25224</a>)</li> <li>Handle aliased
  dict fallbacks in TypedDict unions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25241">#25241</a>)</li> <li>Ignore
  <code>_generate_next_value_</code> with custom construction hooks (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25210">#25210</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Fix find references for <code>except</code> handlers (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25231">#25231</a>)</li> <li>Preserve
  delimiters when folding expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24999">#24999</a>)</li> <li>Use incremental
  file walk on <code>.gitignore</code> changes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25183">#25183</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Add first-class support for enum complements (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24961">#24961</a>)</li> <li>Allow known
  non-field writes on frozen dataclass subclasses (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25087">#25087</a>)</li> <li>Ignore generic
  specialization in layout compatibility checks (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25178">#25178</a>)</li> <li>Preserve
  short-circuit bindings in all condition consumers (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25160">#25160</a>)</li> <li>Support class
  decorators (<a href="https://redirect.github.com/astral-sh/ruff/pull/25091">#25091</a>)</li>
  <li>Support custom <code>_generate_next_value_</code> methods in enums (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25196">#25196</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/MatthewMckee4"><code>@​MatthewMckee4</code></a></li> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/lerebear"><code>@​lerebear</code></a></li> <li><a
  href="https://github.com/thejchap"><code>@​thejchap</code></a></li> </ul> <h2>Install ty
  0.0.38</h2> <h3>Install prebuilt binaries via shell script</h3> <pre lang="sh"><code>curl --proto
  '=https' --tlsv1.2 -LsSf
  https://releases.astral.sh/github/ty/releases/download/0.0.38/ty-installer.sh | sh </code></pre>
  <h3>Install prebuilt binaries via powershell script</h3> <pre lang="sh"><code>powershell
  -ExecutionPolicy Bypass -c &quot;irm
  https://releases.astral.sh/github/ty/releases/download/0.0.38/ty-installer.ps1 | iex&quot;
  </code></pre> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details> <details>
  <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ty/blob/main/CHANGELOG.md">ty's changelog</a>.</em></p>
  <blockquote> <h2>0.0.38</h2> <p>Released on 2026-05-19.</p> <h3>Bug fixes</h3> <ul> <li>Fix panic
  in enum literal during cycle recovery (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25237">#25237</a>)</li> <li>Fix panic from
  lazy <code>NewType</code> base expansion during cycle recovery (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25234">#25234</a>)</li> <li>Fix class-body
  global lookup before class binding (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25224">#25224</a>)</li> <li>Handle aliased
  dict fallbacks in TypedDict unions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25241">#25241</a>)</li> <li>Ignore
  <code>_generate_next_value_</code> with custom construction hooks (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25210">#25210</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Fix find references for <code>except</code> handlers (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25231">#25231</a>)</li> <li>Preserve
  delimiters when folding expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24999">#24999</a>)</li> <li>Use incremental
  file walk on <code>.gitignore</code> changes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25183">#25183</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Add first-class support for enum complements (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24961">#24961</a>)</li> <li>Allow known
  non-field writes on frozen dataclass subclasses (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25087">#25087</a>)</li> <li>Ignore generic
  specialization in layout compatibility checks (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25178">#25178</a>)</li> <li>Preserve
  short-circuit bindings in all condition consumers (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25160">#25160</a>)</li> <li>Support class
  decorators (<a href="https://redirect.github.com/astral-sh/ruff/pull/25091">#25091</a>)</li>
  <li>Support custom <code>_generate_next_value_</code> methods in enums (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25196">#25196</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/MatthewMckee4"><code>@​MatthewMckee4</code></a></li> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/lerebear"><code>@​lerebear</code></a></li> <li><a
  href="https://github.com/thejchap"><code>@​thejchap</code></a></li> </ul> <h2>0.0.37</h2>
  <p>Released on 2026-05-16.</p> <h3>Bug fixes</h3> <ul> <li>Avoid unsound <code>not in</code>
  narrowing (<a href="https://redirect.github.com/astral-sh/ruff/pull/25161">#25161</a>)</li>
  <li>Fix async iteration over narrowed typevars (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25155">#25155</a>)</li> <li>Fix panic in
  double-inference for single starred positional TypedDict (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25176">#25176</a>)</li> <li>Fix panic in
  disjoint base check (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25187">#25187</a>)</li> <li>Fix panic in
  recursive binary inference (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25189">#25189</a>)</li> <li>Fix panic in
  cyclic <code>__new__</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25185">#25185</a>)</li> <li>Fix panic in
  <code>reveal_protocol</code>, <code>reveal_mro</code>, etc. with keyword arguments (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25179">#25179</a>)</li> <li>Fix panic in
  imported overload definition (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/25168">#25168</a>)</li> </ul> <!-- raw HTML
  omitted --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Commits</summary>
  <ul> <li><a
  href="https://github.com/astral-sh/ty/commit/1d3efc1d68e36a8f982fa73b1f8c2a5ebc50fcde"><code>1d3efc1</code></a>
  Bump version to 0.0.38 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3492">#3492</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/f5100ccde50ff577fa311add5232ae6074ed68f9"><code>f5100cc</code></a>
  scripts/update_schemastore: use -C to allow re-running schema update on exist...</li> <li><a
  href="https://github.com/astral-sh/ty/commit/f18aed6430c781ff3bc4fe41d9b5c2a7161657c4"><code>f18aed6</code></a>
  Bump version to 0.0.37 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3473">#3473</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/a63e55929645f8eeaa6f28117afda8d2ed39d1a4"><code>a63e559</code></a>
  Bump version to 0.0.36 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3463">#3463</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/94370d5b43c48d01720a9e65d8d8d5286b6697b1"><code>94370d5</code></a>
  Update prek dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3449">#3449</a>)</li> <li>See full diff in
  <a href="https://github.com/astral-sh/ty/compare/0.0.35...0.0.38">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ty&package-manager=uv&previous-version=0.0.35&new-version=0.0.38)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

### Continuous Integration

- Update e2e.yaml to remove redundant cron schedule
  ([`e306dd5`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e306dd5e6f6e7b6910f4ae5490c0f6ad1b09f486))

Removed the second cron schedule for the workflow.

### Documentation

- Clarify validation and semver commit rules
  ([`aad27c0`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/aad27c0c857f5cf81bc3b217137bc9c40a04f279))

### Features

- Advertise batch feed features in pro tier
  ([`3d57269`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/3d57269b9760b648ffa0278fe930d90dfb77ea08))

Add api:feeds:batch:{list,get,create,upsert,atom} and the mcp:feeds:batch:{list,get,create,upsert}
  counterparts to PRO_FEATURES so clients querying the gateway's advertised feature set discover the
  batch feed endpoints/tools that gateway_pro already implements.

- Cache following feed profiles
  ([`a1e568f`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/a1e568f2903de08fa0bec16c01a2106d727e8f2f))

- Expose application feature metadata
  ([`09935a0`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/09935a0f5551f1acc39e6732c700eafbd0a981a0))

- Mark partial following feeds in responses
  ([`2fa7f8e`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/2fa7f8ea8a88991000004bd1863e1cefc6b26802))

- Normalize Atom feed ids and links
  ([`e3e60ba`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e3e60ba7a448bcf33c05c2863060035c81fb696c))

### Refactoring

- Move pro feature catalogue into gateway_pro
  ([`4e09276`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/4e092769c51ad1a4e3387649f6a18f67858e894e))

OSS shouldn't enumerate PRO-only capabilities. Move PRO_FEATURES, PRO_OAUTH_FEATURES, and
  build_pro_features into gateway_pro.application_features, leaving gateway_oss.application_features
  with only the OSS catalogue and build_oss_features.

The pro extension now imports build_pro_features from its own package.

- Split oss and pro config settings
  ([`3e01838`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/3e018387b888bd2706cb42503f3624d634db1e1d))


## v1.0.0 (2026-04-24)

### Features

- Release Substack Gateway OSS
  ([`77994b7`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/77994b792ab3d08e2832098b0bdc1ff9515164a4))

BREAKING CHANGE: publish the initial public release of Substack Gateway OSS with REST API and MCP
  server interfaces for Substack integrations.

### Breaking Changes

- Publish the initial public release of Substack Gateway OSS with REST API and MCP server interfaces
  for Substack integrations.


## v0.6.0 (2026-04-24)

### Bug Fixes

- Add uvloop dep
  ([`066da64`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/066da6448fe517c70b133ac84b2a362d3db2a85f))

- App startup
  ([`ebf67e9`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/ebf67e95ce11a7226d172eaee2791017e51e024a))

- Apply formatting updates
  ([`088f4ac`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/088f4ac3c4dd8091df5898652037a77780f3dca6))

- Clear following feed cache in pro behave hooks
  ([`fc31385`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/fc3138552ad31eb2cf989d15ece2aa9fade70bc3))

- Configure e2e client timeout
  ([`3febd62`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/3febd6240588844de8726ed3b50e7c123fb6855f))

- Deployment
  ([`db778c9`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/db778c990236d33e17e9906f12ccbfe0c4fac93c))

- Deployment ([#2](https://github.com/jakub-k-slys/substack-gateway-oss/pull/2),
  [`e3823ef`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e3823efa45dff0932c4e4e9a4f5f707bf0938bb4))

- Linter
  ([`e4dbde2`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e4dbde2915e9fec9f33c78ba56abc46e5b652584))

- Log resolved application metadata at startup
  ([`7b6ad56`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/7b6ad56e4904b0ab9fbcb531219d162bd3e3f5cf))

- Prefer app version override for root metadata
  ([`09d5432`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/09d5432e8275c85c5fcfa7dd07b9d277f0ffb892))

- Preserve original authors for feed post items
  ([`abebda2`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/abebda27fb48840538c90dc0f0a6d806a91b0637))

- Restore real notes sample and align test assertions
  ([`0f76887`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/0f768879671272ffaf7261c6e9c74afff366ecc3))

samples/api/v1/notes was accidentally overwritten with a synthetic stub during the me/notes
  implementation. Restored the original 20-item response with nextCursor from the 22b8dda commit.

Updated me_notes.feature to assert against the real data (20 items, non-null next_cursor) and added
  a 'is not null' step to common.py.

https://claude.ai/code/session_01Q67ac3YRNupaRFNHPxt2Ks

- Satisfy type checks in feed tests
  ([`c23f7d9`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/c23f7d957b5fa0121879ec991088e7d9e97c3eb9))

- Sort import blocks in root.py and extension.py
  ([`37781ed`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/37781ed7e66a192e2b5b4888d584f32ea3f82ec1))

Resolve ruff I001 violations by letting ruff --fix reorder the import blocks into the expected isort
  order.

https://claude.ai/code/session_014PHSG4aNJ8F6gj8GFesYan

- Speed up behave Substack client settings
  ([`0be52d8`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/0be52d88ad21805298df31a2e3da9aa55bd6e313))

- Update commit author
  ([`0a8e4d2`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/0a8e4d22fc4d970aa3a12801c6c1264499bb122f))

- Update commit author
  ([`5587752`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/55877527d795a78b2a7c37b3adda63d548d9d280))

- Update commit author
  ([`909706d`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/909706d16b2600b97cac65c1c061ffd15272b7a2))

- Update commiter
  ([`1fd9314`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/1fd931487134d6fea6715a4526ae3090299dcd45))

- Use application version in root metadata
  ([`65c7e04`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/65c7e044fd86899eddb916beedf30a8a220c0bf8))

- Version
  ([`432907c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/432907c3f9f8a1a7e1c3003c44125e215f8b9401))

- Version
  ([`5edb590`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/5edb590a72596ac2146685068eb495b5f9970c27))

- **drafts**: Extract posts key from list-drafts API response
  ([`8532b62`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/8532b6266065d2cc220b47e43a385534cfd5df98))

Substack GET /api/v1/drafts returns {"posts": [...]} not a bare array. Iterating the dict directly
  yielded key strings, causing a Pydantic validation error. Also updates the BDD fixture to match
  the real shape.

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>

### Chores

- Add pre-commit config
  ([`333c5b6`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/333c5b6014796a64f64b12cd373e037f388f4428))

- Log following feed cache hits and misses
  ([`3040275`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/304027551341c2eddf2e2c5410d310cae989a427))

- Update Substack client default settings
  ([`279806c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/279806c952bb2533fc59a46a93ecadb70817ee7e))

- **deps**: Bump async-lru from 2.2.0 to 2.3.0
  ([`0db8b72`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/0db8b72a36b21e00b1bd8cd563c93e50c09f273b))

Bumps [async-lru](https://github.com/aio-libs/async-lru) from 2.2.0 to 2.3.0. - [Release
  notes](https://github.com/aio-libs/async-lru/releases) -
  [Changelog](https://github.com/aio-libs/async-lru/blob/master/CHANGES.rst) -
  [Commits](https://github.com/aio-libs/async-lru/compare/v2.2.0...v2.3.0)

--- updated-dependencies: - dependency-name: async-lru dependency-version: 2.3.0

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump async-lru from 2.2.0 to 2.3.0
  ([#3](https://github.com/jakub-k-slys/substack-gateway-oss/pull/3),
  [`f33155b`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/f33155b32031e2248221ba53b0e3611daaac1af0))

[//]: # (dependabot-start) ⚠️ **Dependabot is rebasing this PR** ⚠️

Rebasing might not happen immediately, so don't worry if this takes some time.

Note: if you make any changes to this PR yourself, they will take precedence over the rebase.

---

[//]: # (dependabot-end)

Bumps [async-lru](https://github.com/aio-libs/async-lru) from 2.2.0 to 2.3.0. <details>
  <summary>Release notes</summary> <p><em>Sourced from <a
  href="https://github.com/aio-libs/async-lru/releases">async-lru's releases</a>.</em></p>
  <blockquote> <h2>2.3.0</h2> <ul> <li>Added <code>cache_contains()</code> for read-only key
  lookup.</li> <li>Changed cross-loop cache access to auto-reset and rebind to the current event
  loop.</li> <li>Added <code>AlruCacheLoopResetWarning</code> when an auto-reset happens due to
  event loop change.</li> <li>Forwarded <code>cache_close(wait=...)</code> for bound methods.</li>
  </ul> </blockquote> </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/aio-libs/async-lru/blob/master/CHANGES.rst">async-lru's
  changelog</a>.</em></p> <blockquote> <h1>2.3.0 (2026-03-18)</h1> <ul> <li>Added
  <code>cache_contains()</code> for read-only key lookup.</li> <li>Changed cross-loop cache access
  to auto-reset and rebind to the current event loop.</li> <li>Added
  <code>AlruCacheLoopResetWarning</code> when an auto-reset happens due to event loop change.</li>
  <li>Forwarded <code>cache_close(wait=...)</code> for bound methods.</li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/aio-libs/async-lru/commit/cb9e034619167668af09c7be71a37e2d40a96995"><code>cb9e034</code></a>
  Release v2.3.0 (<a href="https://redirect.github.com/aio-libs/async-lru/issues/748">#748</a>)</li>
  <li><a
  href="https://github.com/aio-libs/async-lru/commit/a2aa7b05ce9b773539f1c479341ac1c53f1fe9d0"><code>a2aa7b0</code></a>
  build(deps): bump coverage from 7.13.4 to 7.13.5 (<a
  href="https://redirect.github.com/aio-libs/async-lru/issues/747">#747</a>)</li> <li><a
  href="https://github.com/aio-libs/async-lru/commit/63760a481d44d5a2cc0d1325fc2ca233b664367a"><code>63760a4</code></a>
  feat: add cache_contains() for read-only key lookup (<a

href="https://redirect.github.com/aio-libs/async-lru/issues/746">#746</a>)</li> <li><a
  href="https://github.com/aio-libs/async-lru/commit/e2ddf7af72e2eb7382182dbdde7578142f0124be"><code>e2ddf7a</code></a>
  Forward cache_close(wait=...) for bound methods (<a
  href="https://redirect.github.com/aio-libs/async-lru/issues/745">#745</a>)</li> <li><a
  href="https://github.com/aio-libs/async-lru/commit/33e1a7cec396bcf612f46226253775fd905b40eb"><code>33e1a7c</code></a>
  Emit AlruCacheLoopResetWarning on event loop auto-reset (<a
  href="https://redirect.github.com/aio-libs/async-lru/issues/744">#744</a>)</li> <li><a
  href="https://github.com/aio-libs/async-lru/commit/fff4d49334839987946c74bfc02c05f79427e8b2"><code>fff4d49</code></a>
  feat: Allow <code>alru_cache</code> to automatically clear and rebind to the current eve...</li>
  <li>See full diff in <a
  href="https://github.com/aio-libs/async-lru/compare/v2.2.0...v2.3.0">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=async-lru&package-manager=uv&previous-version=2.2.0&new-version=2.3.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps**: Bump cryptography from 46.0.5 to 46.0.6 in the uv group across 1 directory
  ([#54](https://github.com/jakub-k-slys/substack-gateway-oss/pull/54),
  [`1ee43a0`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/1ee43a06da35f41460412baaeff570b540b4fa6c))

Bumps the uv group with 1 update in the / directory:
  [cryptography](https://github.com/pyca/cryptography).

Updates `cryptography` from 46.0.5 to 46.0.6 <details> <summary>Changelog</summary> <p><em>Sourced
  from <a href="https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst">cryptography's
  changelog</a>.</em></p> <blockquote> <p>46.0.6 - 2026-03-25</p> <pre><code> * **SECURITY ISSUE**:
  Fixed a bug where name constraints were not applied to peer names during verification when the
  leaf certificate contains a wildcard DNS SAN. Ordinary X.509 topologies are not affected by this
  bug, including those used by the Web PKI. Credit to **Oleh Konko (1seal)** for reporting the
  issue. **CVE-2026-34073** <p>.. _v46-0-5:<br /> </code></pre></p> </blockquote> </details>
  <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/pyca/cryptography/commit/91d728897bdad30cd5c79a2b23e207f1f050d587"><code>91d7288</code></a>
  Cherry-pick <a href="https://redirect.github.com/pyca/cryptography/issues/14542">#14542</a> (<a
  href="https://redirect.github.com/pyca/cryptography/issues/14543">#14543</a>)</li> <li>See full
  diff in <a href="https://github.com/pyca/cryptography/compare/46.0.5...46.0.6">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=cryptography&package-manager=uv&previous-version=46.0.5&new-version=46.0.6)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore <dependency name> major version` will close this
  group update PR and stop Dependabot creating any more for the specific dependency's major version
  (unless you unignore this specific dependency's major version or upgrade to it yourself) -
  `@dependabot ignore <dependency name> minor version` will close this group update PR and stop
  Dependabot creating any more for the specific dependency's minor version (unless you unignore this
  specific dependency's minor version or upgrade to it yourself) - `@dependabot ignore <dependency
  name>` will close this group update PR and stop Dependabot creating any more for the specific
  dependency (unless you unignore this specific dependency or upgrade to it yourself) - `@dependabot
  unignore <dependency name>` will remove all of the ignore conditions of the specified dependency -
  `@dependabot unignore <dependency name> <ignore condition>` will remove the ignore condition of
  the specified dependency and ignore conditions You can disable automated security fix PRs for this
  repo from the [Security Alerts
  page](https://github.com/jakub-k-slys/substack-gateway-pro/network/alerts).

</details>

- **deps**: Bump cryptography from 46.0.5 to 46.0.6 in the uv group across 1 directory
  ([#8](https://github.com/jakub-k-slys/substack-gateway-oss/pull/8),
  [`6ac0750`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/6ac0750bdb6c180bf6511c6648d7aeedf866695e))

Bumps the uv group with 1 update in the / directory:
  [cryptography](https://github.com/pyca/cryptography).

Updates `cryptography` from 46.0.5 to 46.0.6 <details> <summary>Changelog</summary> <p><em>Sourced
  from <a href="https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst">cryptography's
  changelog</a>.</em></p> <blockquote> <p>46.0.6 - 2026-03-25</p> <pre><code> * **SECURITY ISSUE**:
  Fixed a bug where name constraints were not applied to peer names during verification when the
  leaf certificate contains a wildcard DNS SAN. Ordinary X.509 topologies are not affected by this
  bug, including those used by the Web PKI. Credit to **Oleh Konko (1seal)** for reporting the
  issue. **CVE-2026-34073** <p>.. _v46-0-5:<br /> </code></pre></p> </blockquote> </details>
  <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/pyca/cryptography/commit/91d728897bdad30cd5c79a2b23e207f1f050d587"><code>91d7288</code></a>
  Cherry-pick <a href="https://redirect.github.com/pyca/cryptography/issues/14542">#14542</a> (<a
  href="https://redirect.github.com/pyca/cryptography/issues/14543">#14543</a>)</li> <li>See full
  diff in <a href="https://github.com/pyca/cryptography/compare/46.0.5...46.0.6">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=cryptography&package-manager=uv&previous-version=46.0.5&new-version=46.0.6)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore <dependency name> major version` will close this
  group update PR and stop Dependabot creating any more for the specific dependency's major version
  (unless you unignore this specific dependency's major version or upgrade to it yourself) -
  `@dependabot ignore <dependency name> minor version` will close this group update PR and stop
  Dependabot creating any more for the specific dependency's minor version (unless you unignore this
  specific dependency's minor version or upgrade to it yourself) - `@dependabot ignore <dependency
  name>` will close this group update PR and stop Dependabot creating any more for the specific
  dependency (unless you unignore this specific dependency or upgrade to it yourself) - `@dependabot
  unignore <dependency name>` will remove all of the ignore conditions of the specified dependency -
  `@dependabot unignore <dependency name> <ignore condition>` will remove the ignore condition of
  the specified dependency and ignore conditions You can disable automated security fix PRs for this
  repo from the [Security Alerts
  page](https://github.com/jakub-k-slys/substack-gateway-oss/network/alerts).

</details>

- **deps**: Bump cryptography from 46.0.6 to 46.0.7 in the uv group across 1 directory
  ([#17](https://github.com/jakub-k-slys/substack-gateway-oss/pull/17),
  [`47792bc`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/47792bcbb0a03198b5593b41c98c957b4632010b))

Bumps the uv group with 1 update in the / directory:
  [cryptography](https://github.com/pyca/cryptography).

Updates `cryptography` from 46.0.6 to 46.0.7 <details> <summary>Changelog</summary> <p><em>Sourced
  from <a href="https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst">cryptography's
  changelog</a>.</em></p> <blockquote> <p>46.0.7 - 2026-04-07</p> <pre><code> * **SECURITY ISSUE**:
  Fixed an issue where non-contiguous buffers could be passed to APIs that accept Python buffers,
  which could lead to buffer overflow. **CVE-2026-39892** * Updated Windows, macOS, and Linux wheels
  to be compiled with OpenSSL 3.5.6. <p>.. _v46-0-6:<br /> </code></pre></p> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/pyca/cryptography/commit/622d672e429a7cff836a23c5903683dbec1901f5"><code>622d672</code></a>
  46.0.7 release (<a
  href="https://redirect.github.com/pyca/cryptography/issues/14602">#14602</a>)</li> <li>See full
  diff in <a href="https://github.com/pyca/cryptography/compare/46.0.6...46.0.7">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=cryptography&package-manager=uv&previous-version=46.0.6&new-version=46.0.7)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore <dependency name> major version` will close this
  group update PR and stop Dependabot creating any more for the specific dependency's major version
  (unless you unignore this specific dependency's major version or upgrade to it yourself) -
  `@dependabot ignore <dependency name> minor version` will close this group update PR and stop
  Dependabot creating any more for the specific dependency's minor version (unless you unignore this
  specific dependency's minor version or upgrade to it yourself) - `@dependabot ignore <dependency
  name>` will close this group update PR and stop Dependabot creating any more for the specific
  dependency (unless you unignore this specific dependency or upgrade to it yourself) - `@dependabot
  unignore <dependency name>` will remove all of the ignore conditions of the specified dependency -
  `@dependabot unignore <dependency name> <ignore condition>` will remove the ignore condition of
  the specified dependency and ignore conditions You can disable automated security fix PRs for this
  repo from the [Security Alerts
  page](https://github.com/jakub-k-slys/substack-gateway-oss/network/alerts).

</details>

- **deps**: Bump cryptography from 46.0.6 to 46.0.7 in the uv group across 1 directory
  ([#61](https://github.com/jakub-k-slys/substack-gateway-oss/pull/61),
  [`338b4a9`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/338b4a95134d89c92f471eb72aa62b12f9703633))

Bumps the uv group with 1 update in the / directory:
  [cryptography](https://github.com/pyca/cryptography).

Updates `cryptography` from 46.0.6 to 46.0.7 <details> <summary>Changelog</summary> <p><em>Sourced
  from <a href="https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst">cryptography's
  changelog</a>.</em></p> <blockquote> <p>46.0.7 - 2026-04-07</p> <pre><code> * **SECURITY ISSUE**:
  Fixed an issue where non-contiguous buffers could be passed to APIs that accept Python buffers,
  which could lead to buffer overflow. **CVE-2026-39892** * Updated Windows, macOS, and Linux wheels
  to be compiled with OpenSSL 3.5.6. <p>.. _v46-0-6:<br /> </code></pre></p> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/pyca/cryptography/commit/622d672e429a7cff836a23c5903683dbec1901f5"><code>622d672</code></a>
  46.0.7 release (<a
  href="https://redirect.github.com/pyca/cryptography/issues/14602">#14602</a>)</li> <li>See full
  diff in <a href="https://github.com/pyca/cryptography/compare/46.0.6...46.0.7">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=cryptography&package-manager=uv&previous-version=46.0.6&new-version=46.0.7)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore <dependency name> major version` will close this
  group update PR and stop Dependabot creating any more for the specific dependency's major version
  (unless you unignore this specific dependency's major version or upgrade to it yourself) -
  `@dependabot ignore <dependency name> minor version` will close this group update PR and stop
  Dependabot creating any more for the specific dependency's minor version (unless you unignore this
  specific dependency's minor version or upgrade to it yourself) - `@dependabot ignore <dependency
  name>` will close this group update PR and stop Dependabot creating any more for the specific
  dependency (unless you unignore this specific dependency or upgrade to it yourself) - `@dependabot
  unignore <dependency name>` will remove all of the ignore conditions of the specified dependency -
  `@dependabot unignore <dependency name> <ignore condition>` will remove the ignore condition of
  the specified dependency and ignore conditions You can disable automated security fix PRs for this
  repo from the [Security Alerts
  page](https://github.com/jakub-k-slys/substack-gateway-pro/network/alerts).

</details>

- **deps**: Bump cryptography in the uv group across 1 directory
  ([`e7b6cb9`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e7b6cb9eede1d38423abbec6671edb9a3708ac88))

Bumps the uv group with 1 update in the / directory:
  [cryptography](https://github.com/pyca/cryptography).

Updates `cryptography` from 46.0.6 to 46.0.7 -
  [Changelog](https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pyca/cryptography/compare/46.0.6...46.0.7)

--- updated-dependencies: - dependency-name: cryptography dependency-version: 46.0.7

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump cryptography in the uv group across 1 directory
  ([`ac3cee9`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/ac3cee9a8595829aaf41ecd575dcfe8db41dadc2))

Bumps the uv group with 1 update in the / directory:
  [cryptography](https://github.com/pyca/cryptography).

Updates `cryptography` from 46.0.6 to 46.0.7 -
  [Changelog](https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pyca/cryptography/compare/46.0.6...46.0.7)

--- updated-dependencies: - dependency-name: cryptography dependency-version: 46.0.7

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump cryptography in the uv group across 1 directory
  ([`1590513`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/15905132588af349718791b804b1dbde05d5b3cf))

Bumps the uv group with 1 update in the / directory:
  [cryptography](https://github.com/pyca/cryptography).

Updates `cryptography` from 46.0.5 to 46.0.6 -
  [Changelog](https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pyca/cryptography/compare/46.0.5...46.0.6)

--- updated-dependencies: - dependency-name: cryptography dependency-version: 46.0.6

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump cryptography in the uv group across 1 directory
  ([`2567729`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/2567729678cc795770b5e0b8737fedabb10bdf46))

Bumps the uv group with 1 update in the / directory:
  [cryptography](https://github.com/pyca/cryptography).

Updates `cryptography` from 46.0.5 to 46.0.6 -
  [Changelog](https://github.com/pyca/cryptography/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pyca/cryptography/compare/46.0.5...46.0.6)

--- updated-dependencies: - dependency-name: cryptography dependency-version: 46.0.6

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump fastapi from 0.135.1 to 0.135.2
  ([`18ec27f`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/18ec27fd7ef45b003c26a9e27867ebfc17557682))

Bumps [fastapi](https://github.com/fastapi/fastapi) from 0.135.1 to 0.135.2. - [Release
  notes](https://github.com/fastapi/fastapi/releases) -
  [Commits](https://github.com/fastapi/fastapi/compare/0.135.1...0.135.2)

--- updated-dependencies: - dependency-name: fastapi dependency-version: 0.135.2

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump fastapi from 0.135.1 to 0.135.2
  ([#7](https://github.com/jakub-k-slys/substack-gateway-oss/pull/7),
  [`d37eeb5`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/d37eeb55864ef7756aa3f26aac97d3b216522db6))

Bumps [fastapi](https://github.com/fastapi/fastapi) from 0.135.1 to 0.135.2. <details>
  <summary>Release notes</summary> <p><em>Sourced from <a
  href="https://github.com/fastapi/fastapi/releases">fastapi's releases</a>.</em></p> <blockquote>
  <h2>0.135.2</h2> <h3>Upgrades</h3> <ul> <li>⬆️ Increase lower bound to <code>pydantic
  &gt;=2.9.0.</code> and fix the test suite. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15139">#15139</a> by <a
  href="https://github.com/svlandeg"><code>@​svlandeg</code></a>.</li> </ul> <h3>Docs</h3> <ul>
  <li>📝 Add missing last release notes dates. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15202">#15202</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>📝 Update docs for
  contributors and team members regarding translation PRs. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15200">#15200</a> by <a
  href="https://github.com/YuriiMotov"><code>@​YuriiMotov</code></a>.</li> <li>💄 Fix code blocks in
  reference docs overflowing table width. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15094">#15094</a> by <a
  href="https://github.com/YuriiMotov"><code>@​YuriiMotov</code></a>.</li> <li>📝 Fix duplicated
  words in docstrings. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15116">#15116</a> by <a
  href="https://github.com/AhsanSheraz"><code>@​AhsanSheraz</code></a>.</li> <li>📝 Add docs for
  <code>pyproject.toml</code> with <code>entrypoint</code>. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15075">#15075</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>📝 Update links in docs to
  no longer use the classes external-link and internal-link. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15061">#15061</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🔨 Add JS and CSS handling
  for automatic <code>target=_blank</code> for links in docs. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15063">#15063</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>💄 Update styles for
  internal and external links in new tab. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15058">#15058</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>📝 Add documentation for
  the FastAPI VS Code extension. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15008">#15008</a> by <a
  href="https://github.com/savannahostrowski"><code>@​savannahostrowski</code></a>.</li> <li>📝 Fix
  doctrings for <code>max_digits</code> and <code>decimal_places</code>. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/14944">#14944</a> by <a
  href="https://github.com/YuriiMotov"><code>@​YuriiMotov</code></a>.</li> <li>📝 Add dates to
  release notes. PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15001">#15001</a> by
  <a href="https://github.com/YuriiMotov"><code>@​YuriiMotov</code></a>.</li> </ul>
  <h3>Translations</h3> <ul> <li>🌐 Update translations for zh (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15177">#15177</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  zh-hant (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15178">#15178</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  zh-hant (add-missing). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15176">#15176</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  zh (add-missing). PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15175">#15175</a>
  by <a href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update
  translations for ja (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15171">#15171</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  ko (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15170">#15170</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  tr (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15172">#15172</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  ko (add-missing). PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15168">#15168</a>
  by <a href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update
  translations for ja (add-missing). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15167">#15167</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  tr (add-missing). PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15169">#15169</a>
  by <a href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update
  translations for fr (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15165">#15165</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  fr (add-missing). PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15163">#15163</a>
  by <a href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update
  translations for uk (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15160">#15160</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  uk (add-missing). PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15158">#15158</a>
  by <a href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update
  translations for pt (add-missing). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15157">#15157</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  pt (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15159">#15159</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  es (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15155">#15155</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  es (add-missing). PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15154">#15154</a>
  by <a href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update
  translations for de (update-outdated). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15156">#15156</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  ru (update-and-add). PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15152">#15152</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>🌐 Update translations for
  de (add-missing). PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15153">#15153</a>
  by <a href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> </ul> <h3>Internal</h3>
  <ul> <li>🔨 Exclude spam comments from statistics in <code>scripts/people.py</code>. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15088">#15088</a> by <a
  href="https://github.com/YuriiMotov"><code>@​YuriiMotov</code></a>.</li> <li>⬆ Bump authlib from
  1.6.7 to 1.6.9. PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15128">#15128</a> by
  <a href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  pyasn1 from 0.6.2 to 0.6.3. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15143">#15143</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump
  ujson from 5.11.0 to 5.12.0. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15150">#15150</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>🔨 Tweak
  translation workflow and translation fixer tool. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15166">#15166</a> by <a
  href="https://github.com/YuriiMotov"><code>@​YuriiMotov</code></a>.</li> </ul> <!-- raw HTML
  omitted --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Commits</summary>
  <ul> <li><a
  href="https://github.com/fastapi/fastapi/commit/25a3697cedc6e7dfb84e93c8ff965801486f00f4"><code>25a3697</code></a>
  🔖 Release version 0.135.2</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/ab125daa4034435777853a2c5a6c47451414f9aa"><code>ab125da</code></a>
  📝 Update release notes</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/122b6d490f844b6f716855d55a3e11237b7fb61f"><code>122b6d4</code></a>
  📝 Add missing last release notes dates (<a
  href="https://redirect.github.com/fastapi/fastapi/issues/15202">#15202</a>)</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/68ac0ab91e9b14c418013790fc0e420a827686b5"><code>68ac0ab</code></a>
  📝 Update release notes</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/ea6e287eb398afe6a82c3ef71780e8451813f674"><code>ea6e287</code></a>
  📝 Update docs for contributors and team members regarding translation PRs (<a
  href="https://redirect.github.com/fastapi/fastapi/issues/1">#1</a>...</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/d0a6f208c5cb5daaa1de5ea5187729e3789d1dce"><code>d0a6f20</code></a>
  📝 Update release notes</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/fd9e192cf4fae399c0d51dd23e2a137052eb6087"><code>fd9e192</code></a>
  💄 Fix code blocks in reference docs overflowing table width (<a
  href="https://redirect.github.com/fastapi/fastapi/issues/15094">#15094</a>)</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/fce9460f865928eb7d0393d8809bbc472e0c21cd"><code>fce9460</code></a>
  📝 Update release notes</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/0227991a01e61bf5cdd93cc00e9e243f52b47a4a"><code>0227991</code></a>
  🔨 Exclude spam comments from statistics in <code>scripts/people.py</code> (<a
  href="https://redirect.github.com/fastapi/fastapi/issues/15088">#15088</a>)</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/cbd64b09a32681d3b0ea097608bc62eb0d1587e0"><code>cbd64b0</code></a>
  📝 Update release notes</li> <li>Additional commits viewable in <a
  href="https://github.com/fastapi/fastapi/compare/0.135.1...0.135.2">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=fastapi&package-manager=uv&previous-version=0.135.1&new-version=0.135.2)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps**: Bump fastapi from 0.135.2 to 0.135.3
  ([`b68b999`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/b68b99908da594e0c9b42948442455083fc133cd))

Bumps [fastapi](https://github.com/fastapi/fastapi) from 0.135.2 to 0.135.3. - [Release
  notes](https://github.com/fastapi/fastapi/releases) -
  [Commits](https://github.com/fastapi/fastapi/compare/0.135.2...0.135.3)

--- updated-dependencies: - dependency-name: fastapi dependency-version: 0.135.3

dependency-type: direct:production

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump fastapi from 0.135.2 to 0.135.3
  ([#16](https://github.com/jakub-k-slys/substack-gateway-oss/pull/16),
  [`93a14a2`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/93a14a2afe0f620a82342251af2da66c6d081c78))

Bumps [fastapi](https://github.com/fastapi/fastapi) from 0.135.2 to 0.135.3. <details>
  <summary>Release notes</summary> <p><em>Sourced from <a
  href="https://github.com/fastapi/fastapi/releases">fastapi's releases</a>.</em></p> <blockquote>
  <h2>0.135.3</h2> <h3>Features</h3> <ul> <li>✨ Add support for <code>@app.vibe()</code>. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15280">#15280</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>. <ul> <li>New docs: <a
  href="https://fastapi.tiangolo.com/advanced/vibe/">Vibe Coding</a>.</li> </ul> </li> </ul>
  <h3>Docs</h3> <ul> <li>✏️ Fix typo for <code>client_secret</code> in OAuth2 form docstrings. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/14946">#14946</a> by <a
  href="https://github.com/bysiber"><code>@​bysiber</code></a>.</li> </ul> <h3>Internal</h3> <ul>
  <li>👥 Update FastAPI People - Experts. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15279">#15279</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>⬆ Bump orjson from 3.11.7
  to 3.11.8. PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15276">#15276</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>⬆ Bump ruff
  from 0.15.0 to 0.15.8. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15277">#15277</a> by <a
  href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>👥 Update
  FastAPI GitHub topic repositories. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15274">#15274</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>⬆ Bump fastmcp from
  2.14.5 to 3.2.0. PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15267">#15267</a> by
  <a href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>👥 Update
  FastAPI People - Contributors and Translators. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15270">#15270</a> by <a
  href="https://github.com/tiangolo"><code>@​tiangolo</code></a>.</li> <li>⬆ Bump requests from
  2.32.5 to 2.33.0. PR <a href="https://redirect.github.com/fastapi/fastapi/pull/15228">#15228</a>
  by <a href="https://github.com/apps/dependabot"><code>@​dependabot[bot]</code></a>.</li> <li>👷 Add
  ty check to <code>lint.sh</code>. PR <a
  href="https://redirect.github.com/fastapi/fastapi/pull/15136">#15136</a> by <a
  href="https://github.com/svlandeg"><code>@​svlandeg</code></a>.</li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/fastapi/fastapi/commit/1f442c454f2f74c7419f83c203e6333955399528"><code>1f442c4</code></a>
  🔖 Release version 0.135.3</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/8f5d1577b471f389f6cdea878d40a1497fda7746"><code>8f5d157</code></a>
  📝 Update release notes</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/428452a710338334ae11043a48b06d52d9b3edba"><code>428452a</code></a>
  📝 Update release notes</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/70580da818722cce68b7a88928d67bd0f64f42c5"><code>70580da</code></a>
  ✨ Add support for <code>@app.vibe()</code> (<a
  href="https://redirect.github.com/fastapi/fastapi/issues/15280">#15280</a>)</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/6ee87478d821171139264cd9cd17cbd2232934ce"><code>6ee8747</code></a>
  📝 Update release notes</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/3e72c09a2abfe9e1b55eede6a297cb1847126e49"><code>3e72c09</code></a>
  👥 Update FastAPI People - Experts (<a
  href="https://redirect.github.com/fastapi/fastapi/issues/15279">#15279</a>)</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/96df35f7a4337d612811483d8ade74f91cce2d61"><code>96df35f</code></a>
  📝 Update release notes</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/6c8112555bd86f21cfee8500140dca094ad26e20"><code>6c81125</code></a>
  ⬆ Bump orjson from 3.11.7 to 3.11.8 (<a
  href="https://redirect.github.com/fastapi/fastapi/issues/15276">#15276</a>)</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/428f82c93616b52aee2fcee03484a855135c07e5"><code>428f82c</code></a>
  📝 Update release notes</li> <li><a
  href="https://github.com/fastapi/fastapi/commit/5599c59b9e7112109f04b63a58034fb95833f514"><code>5599c59</code></a>
  ⬆ Bump ruff from 0.15.0 to 0.15.8 (<a
  href="https://redirect.github.com/fastapi/fastapi/issues/15277">#15277</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/fastapi/fastapi/compare/0.135.2...0.135.3">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=fastapi&package-manager=uv&previous-version=0.135.2&new-version=0.135.3)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps**: Bump fastmcp from 3.0.2 to 3.2.0 in the uv group across 1 directory
  ([#55](https://github.com/jakub-k-slys/substack-gateway-oss/pull/55),
  [`3d94c03`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/3d94c0396828959aa8692268f25f1ab96ef8311d))

Bumps the uv group with 1 update in the / directory:
  [fastmcp](https://github.com/PrefectHQ/fastmcp).

Updates `fastmcp` from 3.0.2 to 3.2.0 <details> <summary>Release notes</summary> <p><em>Sourced from
  <a href="https://github.com/PrefectHQ/fastmcp/releases">fastmcp's releases</a>.</em></p>
  <blockquote> <h2>v3.2.0: Show Don't Tool</h2> <p>FastMCP 3.2 is the Apps release. The 3.0
  architecture gave you providers and transforms; 3.1 shipped Code Mode for tool discovery. 3.2 puts
  a face on it: your tools can now return interactive UIs — charts, dashboards, forms, maps —
  rendered right inside the conversation.</p> <h2>FastMCPApp</h2> <p><code>FastMCPApp</code> is a
  new provider class for building interactive applications inside MCP. It separates the tools the
  LLM sees (<code>@app.ui()</code>) from the backend tools the UI calls (<code>@app.tool()</code>),
  manages visibility automatically, and gives tool references stable identifiers that survive
  namespace transforms and server composition — without requiring host cooperation.</p> <pre
  lang="python"><code>from fastmcp import FastMCP, FastMCPApp from prefab_ui.actions.mcp import
  CallTool from prefab_ui.components import Column, Form, Input, Button, ForEach, Text <p>app =
  FastMCPApp(&quot;Contacts&quot;)</p> <p><a
  href="https://github.com/app"><code>@​app</code></a>.tool() def save_contact(name: str, email:
  str) -&gt; list[dict]: db.append({&quot;name&quot;: name, &quot;email&quot;: email}) return
  list(db)</p> <p><a href="https://github.com/app"><code>@​app</code></a>.ui() def contact_manager()
  -&gt; PrefabApp: with PrefabApp(state={&quot;contacts&quot;: list(db)}) as view: with
  Column(gap=4): ForEach(&quot;contacts&quot;, lambda c: Text(c.name)) with
  Form(on_submit=CallTool(&quot;save_contact&quot;)): Input(name=&quot;name&quot;, required=True)
  Input(name=&quot;email&quot;, required=True) Button(&quot;Save&quot;) return view</p> <p>mcp =
  FastMCP(&quot;Server&quot;, providers=[app]) </code></pre></p> <p>The UI is built with <a
  href="https://prefab.prefect.io">Prefab</a>, a Python component library that compiles to
  interactive UIs. You write Python; the user sees charts, tables, forms, and dashboards. FastMCP
  handles the MCP Apps protocol machinery — renderer resources, CSP configuration, structured
  content serialization — so you don't have to.</p> <p>For simpler cases where you just want to
  visualize data without server interaction, set <code>app=True</code> on any tool and return Prefab
  components directly:</p> <pre lang="python"><code>@mcp.tool(app=True) def revenue_chart(year: int)
  -&gt; PrefabApp: with PrefabApp() as app: BarChart(data=revenue_data,
  series=[ChartSeries(data_key=&quot;revenue&quot;)]) return app </code></pre> <h2>Built-in
  Providers</h2> <p>Five ready-made providers you add with a single <code>add_provider()</code>
  call:</p> <ul> <li><strong>FileUpload</strong> — drag-and-drop file upload with session-scoped
  storage</li> </ul> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details>
  <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/PrefectHQ/fastmcp/blob/main/docs/changelog.mdx">fastmcp's
  changelog</a>.</em></p> <blockquote> <hr /> <h2>title: &quot;Changelog&quot; icon:
  &quot;list-check&quot;

rss: true

tag: NEW</h2> <!-- raw HTML omitted --> <p><strong><a
  href="https://github.com/PrefectHQ/fastmcp/releases/tag/v3.1.1">v3.1.1: 'Tis But a
  Patch</a></strong></p> <p>Pins <code>pydantic-monty</code> below 0.0.8 to fix a breaking change in
  Monty that affects code mode. Monty 0.0.8 removed the <code>external_functions</code> constructor
  parameter, causing <code>MontySandboxProvider</code> to fail. This patch caps the version so
  existing installs work correctly.</p> <h3>Fixes 🐞</h3> <ul> <li>Pin pydantic-monty below 0.0.8 to
  fix code mode by <a href="https://github.com/jlowin"><code>@​jlowin</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3497">#3497</a></li> </ul>
  <p><strong>Full Changelog</strong>: <a
  href="https://github.com/PrefectHQ/fastmcp/compare/v3.1.0...v3.1.1">v3.1.0...v3.1.1</a></p> <!--
  raw HTML omitted --> <!-- raw HTML omitted --> <p><strong><a
  href="https://github.com/PrefectHQ/fastmcp/releases/tag/v3.1.0">v3.1.0: Code to
  Joy</a></strong></p> <p>FastMCP 3.1 is the Code Mode release. The 3.0 architecture introduced
  providers and transforms as the extensibility layer — 3.1 puts that architecture to work, shipping
  the most requested capability since launch: servers that can find and execute code on behalf of
  agents, without requiring clients to know what tools exist.</p> <h3>New Features 🎉</h3> <ul>
  <li>feat: Search transforms for tool discovery by <a
  href="https://github.com/jlowin"><code>@​jlowin</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3154">#3154</a></li> <li>Add experimental
  CodeMode transform by <a href="https://github.com/aaazzam"><code>@​aaazzam</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3297">#3297</a></li> <li>Add Prefab Apps
  integration for MCP tool UIs by <a href="https://github.com/jlowin"><code>@​jlowin</code></a> in
  <a href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3316">#3316</a></li> </ul>
  <h3>Enhancements 🔧</h3> <ul> <li>Lazy-load heavy imports to reduce import time by <a
  href="https://github.com/jlowin"><code>@​jlowin</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3295">#3295</a></li> <li>Add http_client
  parameter to all token verifiers for connection pooling by <a
  href="https://github.com/jlowin"><code>@​jlowin</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3300">#3300</a></li> <li>Add in-memory
  caching for token introspection results by <a
  href="https://github.com/jlowin"><code>@​jlowin</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3298">#3298</a></li> <li>Add SessionStart
  hook to install gh CLI in cloud sessions by <a
  href="https://github.com/jlowin"><code>@​jlowin</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3308">#3308</a></li> <li>Fix ty 0.0.19
  type errors by <a href="https://github.com/jlowin"><code>@​jlowin</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3310">#3310</a></li> <li>Code Mode: Add
  resource limits to MontySandboxProvider by <a
  href="https://github.com/jlowin"><code>@​jlowin</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3326">#3326</a></li> <li>Accept
  transforms as FastMCP init kwarg by <a href="https://github.com/jlowin"><code>@​jlowin</code></a>
  in <a href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3324">#3324</a></li> <li>Split
  large test files to comply with loq line limit by <a
  href="https://github.com/jlowin"><code>@​jlowin</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3328">#3328</a></li> <li>Add -m/--module
  flag to <code>fastmcp run</code> and <code>dev inspector</code> by <a
  href="https://github.com/dgenio"><code>@​dgenio</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3331">#3331</a></li> <li>Add
  search_result_serializer hook and serialize_tools_for_output_markdown by <a
  href="https://github.com/MagnusS0"><code>@​MagnusS0</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3337">#3337</a></li> <li>Add MultiAuth
  for composing multiple token verification sources by <a
  href="https://github.com/jlowin"><code>@​jlowin</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3335">#3335</a></li> <li>Adds PropelAuth
  as an AuthProvider by <a
  href="https://github.com/andrew-propelauth"><code>@​andrew-propelauth</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3358">#3358</a></li> <li>Replace vendored
  DI with uncalled-for by <a href="https://github.com/chrisguidry"><code>@​chrisguidry</code></a> in
  <a href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3301">#3301</a></li> <li>Decompose
  CodeMode into composable discovery tools by <a
  href="https://github.com/jlowin"><code>@​jlowin</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3354">#3354</a></li> <li>feat(contrib):
  auto-sync MCPMixin decorators with from_function signatures by <a
  href="https://github.com/AnkeshThakur"><code>@​AnkeshThakur</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3323">#3323</a></li> <li>Add Google GenAI
  Sampling Handler by <a href="https://github.com/strawgate"><code>@​strawgate</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/2977">#2977</a></li> <li>Add ListTools,
  search limit, and catalog size annotation to CodeMode by <a
  href="https://github.com/jlowin"><code>@​jlowin</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3359">#3359</a></li> <li>Allow
  configuring FastMCP transport setting in the same way as other configuration by <a
  href="https://github.com/jvdmr"><code>@​jvdmr</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/1796">#1796</a></li> <li>Add
  include_unversioned option to VersionFilter by <a
  href="https://github.com/yangbaechu"><code>@​yangbaechu</code></a> in <a
  href="https://redirect.github.com/PrefectHQ/fastmcp/pull/3349">#3349</a></li> </ul> <!-- raw HTML
  omitted --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Commits</summary>
  <ul> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/665514e19a78543709be85b4261153bbe98e882f"><code>665514e</code></a>
  Add forward_resource flag to OAuthProxy (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3711">#3711</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/f189d1f7fbfd55c9f68c750a3a293e31c7586e8b"><code>f189d1f</code></a>
  Bump pydantic-monty to 0.0.9 (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3707">#3707</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/6faa2d61f82eab670694965606fd7b14bedddc7f"><code>6faa2d6</code></a>
  Remove hardcoded prefab-ui version from pinning warnings (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3708">#3708</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/dd8816c6ccc733048fe6208bfc8f80ded505f993"><code>dd8816c</code></a>
  chore: Update SDK documentation (<a

href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3701">#3701</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/d27495960af23969f11d6e1e44e2018529c1c37e"><code>d274959</code></a>
  docs: note that custom routes are unauthenticated (<a

href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3706">#3706</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/4a54be2d5f1ac8925a461e67cf993e0278729d4d"><code>4a54be2</code></a>
  Add examples gallery page (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3705">#3705</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/961dd5045611e9c1bd6b7c4f5ac3aa14f0a30ce7"><code>961dd50</code></a>
  Add interactive map example with geocoding (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3702">#3702</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/f01d0c581c7a821a9701d6dde4d9beb95e32d479"><code>f01d0c5</code></a>
  Add quiz example app, fix dev server empty string args (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3700">#3700</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/85b7efd74601a72c74ac68e23599de6c032bb9c4"><code>85b7efd</code></a>
  chore: Update SDK documentation (<a

href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3694">#3694</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/27abe3c3f0cc2ce1925cc3cbc7968d5637ebc82b"><code>27abe3c</code></a>
  Add sales dashboard and live system monitor examples, bump prefab-ui to 0.17 ...</li>
  <li>Additional commits viewable in <a
  href="https://github.com/PrefectHQ/fastmcp/compare/v3.0.2...v3.2.0">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=fastmcp&package-manager=uv&previous-version=3.0.2&new-version=3.2.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore <dependency name> major version` will close this
  group update PR and stop Dependabot creating any more for the specific dependency's major version
  (unless you unignore this specific dependency's major version or upgrade to it yourself) -
  `@dependabot ignore <dependency name> minor version` will close this group update PR and stop
  Dependabot creating any more for the specific dependency's minor version (unless you unignore this
  specific dependency's minor version or upgrade to it yourself) - `@dependabot ignore <dependency
  name>` will close this group update PR and stop Dependabot creating any more for the specific
  dependency (unless you unignore this specific dependency or upgrade to it yourself) - `@dependabot
  unignore <dependency name>` will remove all of the ignore conditions of the specified dependency -
  `@dependabot unignore <dependency name> <ignore condition>` will remove the ignore condition of
  the specified dependency and ignore conditions You can disable automated security fix PRs for this
  repo from the [Security Alerts
  page](https://github.com/jakub-k-slys/substack-gateway-pro/network/alerts).

</details>

- **deps**: Bump fastmcp from 3.1.1 to 3.2.0 in the uv group across 1 directory
  ([#9](https://github.com/jakub-k-slys/substack-gateway-oss/pull/9),
  [`813ec1f`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/813ec1fc1f1272e854253aef3680af22cca87347))

Bumps the uv group with 1 update in the / directory:
  [fastmcp](https://github.com/PrefectHQ/fastmcp).

Updates `fastmcp` from 3.1.1 to 3.2.0 <details> <summary>Release notes</summary> <p><em>Sourced from
  <a href="https://github.com/PrefectHQ/fastmcp/releases">fastmcp's releases</a>.</em></p>
  <blockquote> <h2>v3.2.0: Show Don't Tool</h2> <p>FastMCP 3.2 is the Apps release. The 3.0
  architecture gave you providers and transforms; 3.1 shipped Code Mode for tool discovery. 3.2 puts
  a face on it: your tools can now return interactive UIs — charts, dashboards, forms, maps —
  rendered right inside the conversation.</p> <h2>FastMCPApp</h2> <p><code>FastMCPApp</code> is a
  new provider class for building interactive applications inside MCP. It separates the tools the
  LLM sees (<code>@app.ui()</code>) from the backend tools the UI calls (<code>@app.tool()</code>),
  manages visibility automatically, and gives tool references stable identifiers that survive
  namespace transforms and server composition — without requiring host cooperation.</p> <pre
  lang="python"><code>from fastmcp import FastMCP, FastMCPApp from prefab_ui.actions.mcp import
  CallTool from prefab_ui.components import Column, Form, Input, Button, ForEach, Text <p>app =
  FastMCPApp(&quot;Contacts&quot;)</p> <p><a
  href="https://github.com/app"><code>@​app</code></a>.tool() def save_contact(name: str, email:
  str) -&gt; list[dict]: db.append({&quot;name&quot;: name, &quot;email&quot;: email}) return
  list(db)</p> <p><a href="https://github.com/app"><code>@​app</code></a>.ui() def contact_manager()
  -&gt; PrefabApp: with PrefabApp(state={&quot;contacts&quot;: list(db)}) as view: with
  Column(gap=4): ForEach(&quot;contacts&quot;, lambda c: Text(c.name)) with
  Form(on_submit=CallTool(&quot;save_contact&quot;)): Input(name=&quot;name&quot;, required=True)
  Input(name=&quot;email&quot;, required=True) Button(&quot;Save&quot;) return view</p> <p>mcp =
  FastMCP(&quot;Server&quot;, providers=[app]) </code></pre></p> <p>The UI is built with <a
  href="https://prefab.prefect.io">Prefab</a>, a Python component library that compiles to
  interactive UIs. You write Python; the user sees charts, tables, forms, and dashboards. FastMCP
  handles the MCP Apps protocol machinery — renderer resources, CSP configuration, structured
  content serialization — so you don't have to.</p> <p>For simpler cases where you just want to
  visualize data without server interaction, set <code>app=True</code> on any tool and return Prefab
  components directly:</p> <pre lang="python"><code>@mcp.tool(app=True) def revenue_chart(year: int)
  -&gt; PrefabApp: with PrefabApp() as app: BarChart(data=revenue_data,
  series=[ChartSeries(data_key=&quot;revenue&quot;)]) return app </code></pre> <h2>Built-in
  Providers</h2> <p>Five ready-made providers you add with a single <code>add_provider()</code>
  call:</p> <ul> <li><strong>FileUpload</strong> — drag-and-drop file upload with session-scoped
  storage</li> </ul> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details>
  <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/665514e19a78543709be85b4261153bbe98e882f"><code>665514e</code></a>
  Add forward_resource flag to OAuthProxy (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3711">#3711</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/f189d1f7fbfd55c9f68c750a3a293e31c7586e8b"><code>f189d1f</code></a>
  Bump pydantic-monty to 0.0.9 (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3707">#3707</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/6faa2d61f82eab670694965606fd7b14bedddc7f"><code>6faa2d6</code></a>
  Remove hardcoded prefab-ui version from pinning warnings (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3708">#3708</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/dd8816c6ccc733048fe6208bfc8f80ded505f993"><code>dd8816c</code></a>
  chore: Update SDK documentation (<a

href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3701">#3701</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/d27495960af23969f11d6e1e44e2018529c1c37e"><code>d274959</code></a>
  docs: note that custom routes are unauthenticated (<a

href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3706">#3706</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/4a54be2d5f1ac8925a461e67cf993e0278729d4d"><code>4a54be2</code></a>
  Add examples gallery page (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3705">#3705</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/961dd5045611e9c1bd6b7c4f5ac3aa14f0a30ce7"><code>961dd50</code></a>
  Add interactive map example with geocoding (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3702">#3702</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/f01d0c581c7a821a9701d6dde4d9beb95e32d479"><code>f01d0c5</code></a>
  Add quiz example app, fix dev server empty string args (<a
  href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3700">#3700</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/85b7efd74601a72c74ac68e23599de6c032bb9c4"><code>85b7efd</code></a>
  chore: Update SDK documentation (<a

href="https://redirect.github.com/PrefectHQ/fastmcp/issues/3694">#3694</a>)</li> <li><a
  href="https://github.com/PrefectHQ/fastmcp/commit/27abe3c3f0cc2ce1925cc3cbc7968d5637ebc82b"><code>27abe3c</code></a>
  Add sales dashboard and live system monitor examples, bump prefab-ui to 0.17 ...</li>
  <li>Additional commits viewable in <a
  href="https://github.com/PrefectHQ/fastmcp/compare/v3.1.1...v3.2.0">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=fastmcp&package-manager=uv&previous-version=3.1.1&new-version=3.2.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore <dependency name> major version` will close this
  group update PR and stop Dependabot creating any more for the specific dependency's major version
  (unless you unignore this specific dependency's major version or upgrade to it yourself) -
  `@dependabot ignore <dependency name> minor version` will close this group update PR and stop
  Dependabot creating any more for the specific dependency's minor version (unless you unignore this
  specific dependency's minor version or upgrade to it yourself) - `@dependabot ignore <dependency
  name>` will close this group update PR and stop Dependabot creating any more for the specific
  dependency (unless you unignore this specific dependency or upgrade to it yourself) - `@dependabot
  unignore <dependency name>` will remove all of the ignore conditions of the specified dependency -
  `@dependabot unignore <dependency name> <ignore condition>` will remove the ignore condition of
  the specified dependency and ignore conditions You can disable automated security fix PRs for this
  repo from the [Security Alerts
  page](https://github.com/jakub-k-slys/substack-gateway-oss/network/alerts).

</details>

- **deps**: Bump fastmcp in the uv group across 1 directory
  ([`b20e9fc`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/b20e9fc1a6f89e2aa29552bc4b0970ffeb2afc1d))

Bumps the uv group with 1 update in the / directory:
  [fastmcp](https://github.com/PrefectHQ/fastmcp).

Updates `fastmcp` from 3.1.1 to 3.2.0 - [Release
  notes](https://github.com/PrefectHQ/fastmcp/releases) -
  [Changelog](https://github.com/PrefectHQ/fastmcp/blob/main/docs/changelog.mdx) -
  [Commits](https://github.com/PrefectHQ/fastmcp/compare/v3.1.1...v3.2.0)

--- updated-dependencies: - dependency-name: fastmcp dependency-version: 3.2.0

dependency-type: direct:production

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump fastmcp in the uv group across 1 directory
  ([`07e6ea4`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/07e6ea4985d8206ba2bc6ad834209309300cb3c3))

Bumps the uv group with 1 update in the / directory:
  [fastmcp](https://github.com/PrefectHQ/fastmcp).

Updates `fastmcp` from 3.0.2 to 3.2.0 - [Release
  notes](https://github.com/PrefectHQ/fastmcp/releases) -
  [Changelog](https://github.com/PrefectHQ/fastmcp/blob/main/docs/changelog.mdx) -
  [Commits](https://github.com/PrefectHQ/fastmcp/compare/v3.0.2...v3.2.0)

--- updated-dependencies: - dependency-name: fastmcp dependency-version: 3.2.0

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump python-multipart from 0.0.22 to 0.0.26 in the uv group across 1 directory
  ([#67](https://github.com/jakub-k-slys/substack-gateway-oss/pull/67),
  [`f72cf5c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/f72cf5cfceae9adfab81c0e081f22789dc929121))

Bumps the uv group with 1 update in the / directory:
  [python-multipart](https://github.com/Kludex/python-multipart).

Updates `python-multipart` from 0.0.22 to 0.0.26 <details> <summary>Release notes</summary>
  <p><em>Sourced from <a
  href="https://github.com/Kludex/python-multipart/releases">python-multipart's
  releases</a>.</em></p> <blockquote> <h2>Version 0.0.26</h2> <h2>What's Changed</h2> <ul> <li>Skip
  preamble before first multipart boundary by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/262">Kludex/python-multipart#262</a></li>
  <li>Silently discard epilogue data after the closing boundary by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/259">Kludex/python-multipart#259</a></li>
  </ul> <p><strong>Full Changelog</strong>: <a
  href="https://github.com/Kludex/python-multipart/compare/0.0.25...0.0.26">https://github.com/Kludex/python-multipart/compare/0.0.25...0.0.26</a></p>
  <h2>Version 0.0.25</h2> <h2>What's Changed</h2> <ul> <li>Apply Apache-2.0 properly by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/247">Kludex/python-multipart#247</a></li>
  <li>Handle multipart headers case-insensitively by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/252">Kludex/python-multipart#252</a></li>
  <li>Emit <code>field_end</code> for trailing bare field names on finalize by <a
  href="https://github.com/bysiber"><code>@​bysiber</code></a> in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/230">Kludex/python-multipart#230</a></li>
  <li>Add <code>UPLOAD_DELETE_TMP</code> to <code>FormParser</code> config by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/254">Kludex/python-multipart#254</a></li>
  <li>Remove custom FormParser classes by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/257">Kludex/python-multipart#257</a></li>
  <li>Handle CTE values case-insensitively by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/258">Kludex/python-multipart#258</a></li>
  <li>Add MIME content type info to File by <a
  href="https://github.com/jhnstrk"><code>@​jhnstrk</code></a> in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/143">Kludex/python-multipart#143</a></li>
  </ul> <p><strong>Full Changelog</strong>: <a
  href="https://github.com/Kludex/python-multipart/compare/0.0.24...0.0.25">https://github.com/Kludex/python-multipart/compare/0.0.24...0.0.25</a></p>
  <h2>Version 0.0.24</h2> <h2>What's Changed</h2> <ul> <li>Validate <code>chunk_size</code> in
  <code>parse_form()</code> by <a href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/244">Kludex/python-multipart#244</a></li>
  </ul> <p><strong>Full Changelog</strong>: <a
  href="https://github.com/Kludex/python-multipart/compare/0.0.23...0.0.24">https://github.com/Kludex/python-multipart/compare/0.0.23...0.0.24</a></p>
  <h2>Version 0.0.23</h2> <h2>What's Changed</h2> <ul> <li>Remove unused
  <code>trust_x_headers</code> parameter and <code>X-File-Name</code> fallback by <a
  href="https://github.com/jhnstrk"><code>@​jhnstrk</code></a> in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/196">Kludex/python-multipart#196</a></li>
  <li>Return processed length from <code>QuerystringParser._internal_write</code> by <a
  href="https://github.com/bysiber"><code>@​bysiber</code></a> in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/229">Kludex/python-multipart#229</a></li>
  <li>Cleanup metadata dunders from <code>__init__.py</code> by <a
  href="https://github.com/Chesars"><code>@​Chesars</code></a> in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/227">Kludex/python-multipart#227</a></li>
  </ul> <h2>New Contributors</h2> <ul> <li><a
  href="https://github.com/Chesars"><code>@​Chesars</code></a> made their first contribution in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/227">Kludex/python-multipart#227</a></li>
  <li><a href="https://github.com/bysiber"><code>@​bysiber</code></a> made their first contribution
  in <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/229">Kludex/python-multipart#229</a></li>
  </ul> <p><strong>Full Changelog</strong>: <a
  href="https://github.com/Kludex/python-multipart/compare/0.0.22...0.0.23">https://github.com/Kludex/python-multipart/compare/0.0.22...0.0.23</a></p>
  </blockquote> </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/Kludex/python-multipart/blob/master/CHANGELOG.md">python-multipart's
  changelog</a>.</em></p> <blockquote> <h2>0.0.26 (2026-04-10)</h2> <ul> <li>Skip preamble before
  the first multipart boundary more efficiently <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/262">#262</a>.</li> <li>Silently
  discard epilogue data after the closing multipart boundary <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/259">#259</a>.</li> </ul>
  <h2>0.0.25 (2026-04-10)</h2> <ul> <li>Add MIME content type info to <code>File</code> <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/143">#143</a>.</li> <li>Handle CTE
  values case-insensitively <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/258">#258</a>.</li> <li>Remove
  custom <code>FormParser</code> classes <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/257">#257</a>.</li> <li>Add
  <code>UPLOAD_DELETE_TMP</code> to <code>FormParser</code> config <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/254">#254</a>.</li> <li>Emit
  <code>field_end</code> for trailing bare field names on finalize <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/230">#230</a>.</li> <li>Handle
  multipart headers case-insensitively <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/252">#252</a>.</li> <li>Apply
  Apache-2.0 properly <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/247">#247</a>.</li> </ul>
  <h2>0.0.24 (2026-04-05)</h2> <ul> <li>Validate <code>chunk_size</code> in
  <code>parse_form()</code> <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/244">#244</a>.</li> </ul>
  <h2>0.0.23 (2026-04-05)</h2> <ul> <li>Remove unused <code>trust_x_headers</code> parameter and
  <code>X-File-Name</code> fallback <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/196">#196</a>.</li> <li>Return
  processed length from <code>QuerystringParser._internal_write</code> <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/229">#229</a>.</li> <li>Cleanup
  metadata dunders from <code>__init__.py</code> <a
  href="https://redirect.github.com/Kludex/python-multipart/pull/227">#227</a>.</li> </ul>
  </blockquote> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/Kludex/python-multipart/commit/28f47859b4a40c2e11e02dc514b2e9743ceedd2e"><code>28f4785</code></a>
  Version 0.0.26 (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/263">#263</a>)</li> <li><a
  href="https://github.com/Kludex/python-multipart/commit/d4452a78bbde94995dd3c0d1b4aff3610a5c472f"><code>d4452a7</code></a>
  Silently discard epilogue data after the closing boundary (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/259">#259</a>)</li> <li><a
  href="https://github.com/Kludex/python-multipart/commit/6a7b76dd2653d99d8e5981d7ff09a4a047750b37"><code>6a7b76d</code></a>
  Skip preamble before first multipart boundary (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/262">#262</a>)</li> <li><a
  href="https://github.com/Kludex/python-multipart/commit/4addb60350fc843f77a1502f14247db91930b3bf"><code>4addb60</code></a>
  Version 0.0.25 (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/261">#261</a>)</li> <li><a
  href="https://github.com/Kludex/python-multipart/commit/d3a4698e0dc16cbd85f98076b2ebf9b696cd3604"><code>d3a4698</code></a>
  Add MIME content type info to File (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/143">#143</a>)</li> <li><a
  href="https://github.com/Kludex/python-multipart/commit/9a1ecbd074801fcd3911266f3f4442181d10ab92"><code>9a1ecbd</code></a>
  Handle CTE values case-insensitively (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/258">#258</a>)</li> <li><a
  href="https://github.com/Kludex/python-multipart/commit/ef2a0b94f95676ea6a7b77d2252b09f5797cb8ed"><code>ef2a0b9</code></a>
  Remove custom FormParser classes (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/257">#257</a>)</li> <li><a
  href="https://github.com/Kludex/python-multipart/commit/3a757d7cf209e654eb17cf7b7af868eed469f680"><code>3a757d7</code></a>
  Ignore local Claude state (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/255">#255</a>)</li> <li><a
  href="https://github.com/Kludex/python-multipart/commit/55e739617db7c40e2cd04c5ad8c7acf2ed0a1d19"><code>55e7396</code></a>
  fuzz: Add cifuzz (<a

href="https://redirect.github.com/Kludex/python-multipart/issues/186">#186</a>)</li> <li><a
  href="https://github.com/Kludex/python-multipart/commit/d6d1d111e7de9ce3d3f8623fe5f5e4201c0a5fd1"><code>d6d1d11</code></a>
  Bump the github-actions group with 2 updates (<a
  href="https://redirect.github.com/Kludex/python-multipart/issues/249">#249</a>)</li>
  <li>Additional commits viewable in <a
  href="https://github.com/Kludex/python-multipart/compare/0.0.22...0.0.26">compare view</a></li>
  </ul> </details> <br />

- **deps**: Bump python-multipart in the uv group across 1 directory
  ([`ab28115`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/ab281153f7952ca6ac515280cb17370ec8351d93))

Bumps the uv group with 1 update in the / directory:
  [python-multipart](https://github.com/Kludex/python-multipart).

Updates `python-multipart` from 0.0.22 to 0.0.26 - [Release
  notes](https://github.com/Kludex/python-multipart/releases) -
  [Changelog](https://github.com/Kludex/python-multipart/blob/master/CHANGELOG.md) -
  [Commits](https://github.com/Kludex/python-multipart/compare/0.0.22...0.0.26)

--- updated-dependencies: - dependency-name: python-multipart dependency-version: 0.0.26

dependency-type: indirect

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the uv group across 1 directory with 2 updates
  ([`60d76ae`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/60d76ae15ce44c5cb6d74786572abff93e3911a1))

Bumps the uv group with 2 updates in the / directory: [authlib](https://github.com/authlib/authlib)
  and [python-dotenv](https://github.com/theskumar/python-dotenv).

Updates `authlib` from 1.6.9 to 1.6.11 - [Release
  notes](https://github.com/authlib/authlib/releases) -
  [Changelog](https://github.com/authlib/authlib/blob/v1.6.11/docs/changelog.rst) -
  [Commits](https://github.com/authlib/authlib/compare/v1.6.9...v1.6.11)

Updates `python-dotenv` from 1.2.1 to 1.2.2 - [Release
  notes](https://github.com/theskumar/python-dotenv/releases) -
  [Changelog](https://github.com/theskumar/python-dotenv/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/theskumar/python-dotenv/compare/v1.2.1...v1.2.2)

--- updated-dependencies: - dependency-name: authlib dependency-version: 1.6.11

dependency-type: indirect

dependency-group: uv

- dependency-name: python-dotenv dependency-version: 1.2.2

dependency-group: uv ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump the uv group across 1 directory with 2 updates
  ([#72](https://github.com/jakub-k-slys/substack-gateway-oss/pull/72),
  [`e3cd336`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e3cd336093765418c6dbd74778d1eaadc7eb0c0a))

Bumps the uv group with 2 updates in the / directory: [authlib](https://github.com/authlib/authlib)
  and [python-dotenv](https://github.com/theskumar/python-dotenv).

Updates `authlib` from 1.6.9 to 1.6.11 <details> <summary>Release notes</summary> <p><em>Sourced
  from <a href="https://github.com/authlib/authlib/releases">authlib's releases</a>.</em></p>
  <blockquote> <h2>v1.6.11</h2> <p><strong>Full Changelog</strong>: <a
  href="https://github.com/authlib/authlib/compare/v1.6.10...v1.6.11">https://github.com/authlib/authlib/compare/v1.6.10...v1.6.11</a></p>
  <ul> <li>Fix CSRF issue with starlette client</li> </ul> <h2>v1.6.10</h2> <p><strong>Full
  Changelog</strong>: <a
  href="https://github.com/authlib/authlib/compare/v1.6.9...v1.6.10">https://github.com/authlib/authlib/compare/v1.6.9...v1.6.10</a></p>
  <ul> <li>Fix redirecting to unvalidated <code>redirect_uri</code> on
  <code>UnsupportedResponseTypeError</code>.</li> </ul> </blockquote> </details> <details>
  <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/authlib/authlib/blob/v1.6.11/docs/changelog.rst">authlib's
  changelog</a>.</em></p> <blockquote> <h2>Version 1.6.11</h2> <p><strong>Released on Apr 16,
  2026</strong></p> <ul> <li>Fix CSRF vulnerability in the Starlette OAuth client when a
  <code>cache</code> is configured.</li> </ul> <h2>Version 1.6.10</h2> <p><strong>Released on Apr
  13, 2026</strong></p> <ul> <li>Fix redirecting to unvalidated <code>redirect_uri</code> on
  <code>UnsupportedResponseTypeError</code>.</li> </ul> </blockquote> </details> <details>
  <summary>Commits</summary> <ul> <li><a
  href="https://github.com/authlib/authlib/commit/0dc0e5b4dc84f155319518a3732113af6fa47525"><code>0dc0e5b</code></a>
  chore: bump to 1.6.11</li> <li><a
  href="https://github.com/authlib/authlib/commit/aa7b8e46e00d0622658666476782042ac00153a5"><code>aa7b8e4</code></a>
  Merge commit from fork</li> <li><a
  href="https://github.com/authlib/authlib/commit/401a7709c3fe43bce1b2105d16a475b688faa788"><code>401a770</code></a>
  fix: CSRF issue with starlette client</li> <li><a
  href="https://github.com/authlib/authlib/commit/ef09aebbba4439dedb22bd15777d1b3458b6f0ab"><code>ef09aeb</code></a>
  chore: release 1.6.10</li> <li><a
  href="https://github.com/authlib/authlib/commit/3be08468201a7766a93012ce149ea12822cab096"><code>3be0846</code></a>
  fix: redirecting to unvalidated redirect_uri on UnsupportedResponseTypeError</li> <li>See full
  diff in <a href="https://github.com/authlib/authlib/compare/v1.6.9...v1.6.11">compare
  view</a></li> </ul> </details> <br />

Updates `python-dotenv` from 1.2.1 to 1.2.2 <details> <summary>Release notes</summary>
  <p><em>Sourced from <a href="https://github.com/theskumar/python-dotenv/releases">python-dotenv's
  releases</a>.</em></p> <blockquote> <h2>v1.2.2</h2> <h3>Added</h3> <ul> <li>Support for Python
  3.14, including the free-threaded (3.14t) build. (#)</li> </ul> <h3>Changed</h3> <ul> <li>The
  <code>dotenv run</code> command now forwards flags directly to the specified command by <a
  href="https://github.com/bbc2"><code>@​bbc2</code></a> in <a
  href="https://redirect.github.com/theskumar/python-dotenv/pull/607">theskumar/python-dotenv#607</a></li>
  <li>Improved documentation clarity regarding override behavior and the reference page.</li>
  <li>Updated PyPy support to version 3.11.</li> <li>Documentation for FIFO file support.</li>
  <li>Support for Python 3.9.</li> </ul> <h3>Fixed</h3> <ul> <li>Improved <code>set_key</code> and
  <code>unset_key</code> behavior when interacting with symlinks by <a
  href="https://github.com/bbc2"><code>@​bbc2</code></a> in <a
  href="https://github.com/theskumar/python-dotenv/commit/790c5c02991100aa1bf41ee5330aca75edc51311">#790c5</a></li>
  <li>Corrected the license specifier and added missing Python 3.14 classifiers in package metadata
  by <a href="https://github.com/JYOuyang"><code>@​JYOuyang</code></a> in <a
  href="https://redirect.github.com/theskumar/python-dotenv/pull/590">theskumar/python-dotenv#590</a></li>
  </ul> <h3>Breaking Changes</h3> <ul> <li> <p><code>dotenv.set_key</code> and
  <code>dotenv.unset_key</code> used to follow symlinks in some situations. This is no longer the
  case. For that behavior to be restored in all cases, <code>follow_symlinks=True</code> should be
  used.</p> </li> <li> <p>In the CLI, <code>set</code> and <code>unset</code> used to follow
  symlinks in some situations. This is no longer the case.</p> </li> <li>
  <p><code>dotenv.set_key</code>, <code>dotenv.unset_key</code> and the CLI commands
  <code>set</code> and <code>unset</code> used to reset the file mode of the modified .env file to
  <code>0o600</code> in some situations. This is no longer the case: The original mode of the file
  is now preserved. Is the file needed to be created or wasn't a regular file, mode
  <code>0o600</code> is used.</p> </li> </ul> <h3>Misc</h3> <ul> <li>skip 000 permission tests for
  root user by <a href="https://github.com/burnout-projects"><code>@​burnout-projects</code></a> in
  <a
  href="https://redirect.github.com/theskumar/python-dotenv/pull/561">theskumar/python-dotenv#561</a></li>
  <li>Bump actions/checkout from 5 to 6 in the github-actions group by <a
  href="https://github.com/dependabot"><code>@​dependabot</code></a>[bot] in <a
  href="https://redirect.github.com/theskumar/python-dotenv/pull/593">theskumar/python-dotenv#593</a></li>
  <li>Add Windows testing to CI by <a href="https://github.com/bbc2"><code>@​bbc2</code></a> in <a
  href="https://redirect.github.com/theskumar/python-dotenv/pull/604">theskumar/python-dotenv#604</a></li>
  <li>Improve workflow efficiency with best practices by <a
  href="https://github.com/theskumar"><code>@​theskumar</code></a> in <a
  href="https://redirect.github.com/theskumar/python-dotenv/pull/609">theskumar/python-dotenv#609</a></li>
  <li>Remove the use of <code>sh</code> in tests by <a
  href="https://github.com/bbc2"><code>@​bbc2</code></a> in <a
  href="https://redirect.github.com/theskumar/python-dotenv/pull/612">theskumar/python-dotenv#612</a></li>
  </ul> <h2>New Contributors</h2> <ul> <li><a
  href="https://github.com/JYOuyang"><code>@​JYOuyang</code></a> made their first contribution in <a
  href="https://redirect.github.com/theskumar/python-dotenv/pull/590">theskumar/python-dotenv#590</a></li>
  <li><a href="https://github.com/burnout-projects"><code>@​burnout-projects</code></a> made their
  first contribution in <a
  href="https://redirect.github.com/theskumar/python-dotenv/pull/561">theskumar/python-dotenv#561</a></li>
  <li><a href="https://github.com/cpackham-atlnz"><code>@​cpackham-atlnz</code></a> made their first
  contribution in <a
  href="https://redirect.github.com/theskumar/python-dotenv/pull/597">theskumar/python-dotenv#597</a></li>
  </ul> <p><strong>Full Changelog</strong>: <a
  href="https://github.com/theskumar/python-dotenv/compare/v1.2.1...v1.2.2">https://github.com/theskumar/python-dotenv/compare/v1.2.1...v1.2.2</a></p>
  </blockquote> </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/theskumar/python-dotenv/blob/main/CHANGELOG.md">python-dotenv's
  changelog</a>.</em></p> <blockquote> <h2>[1.2.2] - 2026-03-01</h2> <h3>Added</h3> <ul> <li>Support
  for Python 3.14, including the free-threaded (3.14t) build. (<a
  href="https://redirect.github.com/theskumar/python-dotenv/issues/588">#588</a>)</li> </ul>
  <h3>Changed</h3> <ul> <li>The <code>dotenv run</code> command now forwards flags directly to the
  specified command by [<a href="https://github.com/bbc2"><code>@​bbc2</code></a>] in <a
  href="https://redirect.github.com/theskumar/python-dotenv/issues/607">#607</a></li> <li>Improved
  documentation clarity regarding override behavior and the reference page.</li> <li>Updated PyPy
  support to version 3.11.</li> <li>Documentation for FIFO file support.</li> <li>Dropped Support
  for Python 3.9.</li> </ul> <h3>Fixed</h3> <ul> <li>Improved <code>set_key</code> and
  <code>unset_key</code> behavior when interacting with symlinks by [<a
  href="https://github.com/bbc2"><code>@​bbc2</code></a>] in [790c5c0]</li> <li>Corrected the
  license specifier and added missing Python 3.14 classifiers in package metadata by [<a
  href="https://github.com/JYOuyang"><code>@​JYOuyang</code></a>] in <a
  href="https://redirect.github.com/theskumar/python-dotenv/issues/590">#590</a></li> </ul>
  <h3>Breaking Changes</h3> <ul> <li> <p><code>dotenv.set_key</code> and
  <code>dotenv.unset_key</code> used to follow symlinks in some situations. This is no longer the
  case. For that behavior to be restored in all cases, <code>follow_symlinks=True</code> should be
  used.</p> </li> <li> <p>In the CLI, <code>set</code> and <code>unset</code> used to follow
  symlinks in some situations. This is no longer the case.</p> </li> <li>
  <p><code>dotenv.set_key</code>, <code>dotenv.unset_key</code> and the CLI commands
  <code>set</code> and <code>unset</code> used to reset the file mode of the modified .env file to
  <code>0o600</code> in some situations. This is no longer the case: The original mode of the file
  is now preserved. Is the file needed to be created or wasn't a regular file, mode
  <code>0o600</code> is used.</p> </li> </ul> </blockquote> </details> <details>
  <summary>Commits</summary> <ul> <li><a
  href="https://github.com/theskumar/python-dotenv/commit/36004e0e34be7665ff2b11a8a4005144f76f176d"><code>36004e0</code></a>
  Bump version: 1.2.1 → 1.2.2</li> <li><a
  href="https://github.com/theskumar/python-dotenv/commit/eb202520e5933c9daf42501e1e42fdb0144002c8"><code>eb20252</code></a>
  docs: update changelog for v1.2.2</li> <li><a
  href="https://github.com/theskumar/python-dotenv/commit/790c5c02991100aa1bf41ee5330aca75edc51311"><code>790c5c0</code></a>
  Merge commit from fork</li> <li><a
  href="https://github.com/theskumar/python-dotenv/commit/43340da220fb4ca4f95357bbe21a3c7f8f1278b1"><code>43340da</code></a>
  Remove the use of <code>sh</code> in tests (<a
  href="https://redirect.github.com/theskumar/python-dotenv/issues/612">#612</a>)</li> <li><a
  href="https://github.com/theskumar/python-dotenv/commit/09d7cee32459e7abdcb5c9d8122a552589c06a9c"><code>09d7cee</code></a>
  docs: clarify override behavior and document FIFO support (<a

href="https://redirect.github.com/theskumar/python-dotenv/issues/610">#610</a>)</li> <li><a
  href="https://github.com/theskumar/python-dotenv/commit/c8de2887c00198c22842c5ae5e92d1747467363c"><code>c8de288</code></a>
  ci: improve workflow efficiency with best practices (<a

href="https://redirect.github.com/theskumar/python-dotenv/issues/609">#609</a>)</li> <li><a
  href="https://github.com/theskumar/python-dotenv/commit/7bd9e3dbfedc0983ad7d56d5570013035242bdf4"><code>7bd9e3d</code></a>
  Add Windows testing to CI (<a
  href="https://redirect.github.com/theskumar/python-dotenv/issues/604">#604</a>)</li> <li><a
  href="https://github.com/theskumar/python-dotenv/commit/1baaf04f336072e0ee324d5df9563ec767f14f81"><code>1baaf04</code></a>
  Drop Python 3.9 support and update to PyPy 3.11 (<a
  href="https://redirect.github.com/theskumar/python-dotenv/issues/608">#608</a>)</li> <li><a
  href="https://github.com/theskumar/python-dotenv/commit/4a22cf8993804aeede0c20b75bb1a29d3a99e9dc"><code>4a22cf8</code></a>
  ci: enable testing on Python 3.14t (free-threaded) (<a

href="https://redirect.github.com/theskumar/python-dotenv/issues/588">#588</a>)</li> <li><a
  href="https://github.com/theskumar/python-dotenv/commit/e2e8e776b42e382ae38b44d3982dd649e7507dd4"><code>e2e8e77</code></a>
  Fix license specifier (<a
  href="https://redirect.github.com/theskumar/python-dotenv/issues/597">#597</a>)</li>
  <li>Additional commits viewable in <a
  href="https://github.com/theskumar/python-dotenv/compare/v1.2.1...v1.2.2">compare view</a></li>
  </ul> </details> <br />

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore <dependency name> major version` will close this
  group update PR and stop Dependabot creating any more for the specific dependency's major version
  (unless you unignore this specific dependency's major version or upgrade to it yourself) -
  `@dependabot ignore <dependency name> minor version` will close this group update PR and stop
  Dependabot creating any more for the specific dependency's minor version (unless you unignore this
  specific dependency's minor version or upgrade to it yourself) - `@dependabot ignore <dependency
  name>` will close this group update PR and stop Dependabot creating any more for the specific
  dependency (unless you unignore this specific dependency or upgrade to it yourself) - `@dependabot
  unignore <dependency name>` will remove all of the ignore conditions of the specified dependency -
  `@dependabot unignore <dependency name> <ignore condition>` will remove the ignore condition of
  the specified dependency and ignore conditions You can disable automated security fix PRs for this
  repo from the [Security Alerts
  page](https://github.com/jakub-k-slys/substack-gateway-pro/network/alerts).

</details>

- **deps**: Bump uvicorn from 0.41.0 to 0.42.0
  ([`2ed5bd0`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/2ed5bd02b5d75d839eda6c89c6a719743be532a3))

Bumps [uvicorn](https://github.com/Kludex/uvicorn) from 0.41.0 to 0.42.0. - [Release
  notes](https://github.com/Kludex/uvicorn/releases) -
  [Changelog](https://github.com/Kludex/uvicorn/blob/main/docs/release-notes.md) -
  [Commits](https://github.com/Kludex/uvicorn/compare/0.41.0...0.42.0)

--- updated-dependencies: - dependency-name: uvicorn dependency-version: 0.42.0

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump uvicorn from 0.41.0 to 0.42.0
  ([#51](https://github.com/jakub-k-slys/substack-gateway-oss/pull/51),
  [`06aaad6`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/06aaad60990469bc7461ec503f22843a145c8ff0))

Bumps [uvicorn](https://github.com/Kludex/uvicorn) from 0.41.0 to 0.42.0. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/Kludex/uvicorn/releases">uvicorn's
  releases</a>.</em></p> <blockquote> <h2>Version 0.42.0</h2> <h2>Changed</h2> <ul> <li>Use
  <code>bytearray</code> for request body accumulation to avoid O(n^2) allocation on fragmented
  bodies (<a href="https://redirect.github.com/Kludex/uvicorn/issues/2845">#2845</a>)</li> </ul>
  <h2>Fixed</h2> <ul> <li>Escape brackets and backslash in httptools <code>HEADER_RE</code> regex
  (<a href="https://redirect.github.com/Kludex/uvicorn/issues/2824">#2824</a>)</li> <li>Fix multiple
  issues in websockets sans-io implementation (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2825">#2825</a>)</li> </ul> <hr /> <h2>New
  Contributors</h2> <ul> <li><a href="https://github.com/bysiber"><code>@​bysiber</code></a> made
  their first contribution in <a
  href="https://redirect.github.com/Kludex/uvicorn/pull/2825">Kludex/uvicorn#2825</a></li> </ul> <hr
  /> <p><strong>Full Changelog</strong>: <a
  href="https://github.com/Kludex/uvicorn/compare/0.41.0...0.42.0">https://github.com/Kludex/uvicorn/compare/0.41.0...0.42.0</a></p>
  </blockquote> </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/Kludex/uvicorn/blob/main/docs/release-notes.md">uvicorn's
  changelog</a>.</em></p> <blockquote> <h2>0.42.0 (March 16, 2026)</h2> <h3>Changed</h3> <ul>
  <li>Use <code>bytearray</code> for request body accumulation to avoid O(n^2) allocation on
  fragmented bodies (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2845">#2845</a>)</li> </ul> <h3>Fixed</h3>
  <ul> <li>Escape brackets and backslash in httptools <code>HEADER_RE</code> regex (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2824">#2824</a>)</li> <li>Fix multiple
  issues in websockets sans-io implementation (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2825">#2825</a>)</li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/Kludex/uvicorn/commit/02bed6f8c38e74f684bb0e572977a9bfdc1f6fea"><code>02bed6f</code></a>
  Version 0.42.0 (<a href="https://redirect.github.com/Kludex/uvicorn/issues/2852">#2852</a>)</li>
  <li><a
  href="https://github.com/Kludex/uvicorn/commit/d8f25013161d8206e129e39bf48432d3a85e1744"><code>d8f2501</code></a>
  chore: pre-create Config objects in benchmarks to measure protocol hot paths ...</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/9dbb7836bb0fdb446d083ecd8dc5a2a95bb96b98"><code>9dbb783</code></a>
  Add WebSocket protocol benchmarks for wsproto and websockets-sansio (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2849">#2849</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/b3c69da8c1a36e1834e614abe38243671e156077"><code>b3c69da</code></a>
  Use bytearray for request body accumulation (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2845">#2845</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/3f3ebee20f46504a3f7279dd72f9c24ce9070b11"><code>3f3ebee</code></a>
  Disable <code>pytest-xdist</code> for CodSpeed benchmark runs (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2847">#2847</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/d072de754f825bee4710363dd49d41efd5285dcc"><code>d072de7</code></a>
  Add fragmented body benchmark for chunked body accumulation (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2846">#2846</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/e300c2c75d71bea6f8d1799ca6f182f1e5583aaa"><code>e300c2c</code></a>
  Add CodSpeed benchmark suite for HTTP protocol hot paths (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2844">#2844</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/1fa697651bacf10d72f74de104ead814ce6fcdc0"><code>1fa6976</code></a>
  Escape brackets and backslash in httptools HEADER_RE regex (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2824">#2824</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/59ec1de7a4f07afbd139812f033f3af8b784de74"><code>59ec1de</code></a>
  Fix multiple issues in websockets sansio implementation (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2825">#2825</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/2fc0efcdd958abd3adbe6ea19682408d6b2e1b18"><code>2fc0efc</code></a>
  Clarify Windows asyncio event loop selection in docs (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2843">#2843</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/Kludex/uvicorn/compare/0.41.0...0.42.0">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=uvicorn&package-manager=uv&previous-version=0.41.0&new-version=0.42.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps**: Bump uvicorn from 0.42.0 to 0.44.0
  ([`0c4310f`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/0c4310f6ae3fc6278faa3c38818119ec8c82d526))

Bumps [uvicorn](https://github.com/Kludex/uvicorn) from 0.42.0 to 0.44.0. - [Release
  notes](https://github.com/Kludex/uvicorn/releases) -
  [Changelog](https://github.com/Kludex/uvicorn/blob/main/docs/release-notes.md) -
  [Commits](https://github.com/Kludex/uvicorn/compare/0.42.0...0.44.0)

--- updated-dependencies: - dependency-name: uvicorn dependency-version: 0.44.0

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump uvicorn from 0.42.0 to 0.44.0
  ([#66](https://github.com/jakub-k-slys/substack-gateway-oss/pull/66),
  [`d7123ce`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/d7123ced99b392bf47b02711b244e0501d39fb8b))

Bumps [uvicorn](https://github.com/Kludex/uvicorn) from 0.42.0 to 0.44.0. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/Kludex/uvicorn/releases">uvicorn's
  releases</a>.</em></p> <blockquote> <h2>Version 0.44.0</h2> <h2>What's Changed</h2> <ul>
  <li>Implement websocket keepalive pings for websockets-sansio by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/uvicorn/pull/2888">Kludex/uvicorn#2888</a></li> </ul>
  <p><strong>Full Changelog</strong>: <a
  href="https://github.com/Kludex/uvicorn/compare/0.43.0...0.44.0">https://github.com/Kludex/uvicorn/compare/0.43.0...0.44.0</a></p>
  <h2>Version 0.43.0</h2> <h2>Changed</h2> <ul> <li>Emit <code>http.disconnect</code> ASGI
  <code>receive()</code> event on server shutting down for streaming responses (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2829">#2829</a>)</li> <li>Use native
  <code>context</code> parameter for <code>create_task</code> on Python 3.11+ (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2859">#2859</a>)</li> <li>Drop cast in
  ASGI types (<a href="https://redirect.github.com/Kludex/uvicorn/issues/2875">#2875</a>)</li> </ul>
  <hr /> <p><strong>Full Changelog</strong>: <a
  href="https://github.com/Kludex/uvicorn/compare/0.42.0...0.43.0">https://github.com/Kludex/uvicorn/compare/0.42.0...0.43.0</a></p>
  </blockquote> </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/Kludex/uvicorn/blob/main/docs/release-notes.md">uvicorn's
  changelog</a>.</em></p> <blockquote> <h2>0.44.0 (April 6, 2026)</h2> <h3>Added</h3> <ul>
  <li>Implement websocket keepalive pings for websockets-sansio (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2888">#2888</a>)</li> </ul> <h2>0.43.0
  (April 3, 2026)</h2> <p>You can quit Uvicorn now. We heard you, <a
  href="https://github.com/pamelafox"><code>@​pamelafox</code></a> - all 47 of your Ctrl+C's (thanks
  for flagging it, and thanks to <a href="https://github.com/tiangolo"><code>@​tiangolo</code></a>
  for the fix 🙏). <a href="https://x.com/pamelafox/status/2039097686155227623">See the
  tweet</a>.</p> <h3>Changed</h3> <ul> <li>Emit <code>http.disconnect</code> ASGI
  <code>receive()</code> event on server shutting down for streaming responses (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2829">#2829</a>)</li> <li>Use native
  <code>context</code> parameter for <code>create_task</code> on Python 3.11+ (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2859">#2859</a>)</li> <li>Drop cast in
  ASGI types (<a href="https://redirect.github.com/Kludex/uvicorn/issues/2875">#2875</a>)</li> </ul>
  </blockquote> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/Kludex/uvicorn/commit/edb54c43c0321c0b41eee1473f3f4cf145e8927f"><code>edb54c4</code></a>
  Version 0.44.0 (<a href="https://redirect.github.com/Kludex/uvicorn/issues/2890">#2890</a>)</li>
  <li><a
  href="https://github.com/Kludex/uvicorn/commit/029be08867fe899cde6fd31a3ba75fffca7bd9ae"><code>029be08</code></a>
  Implement websocket keepalive pings for websockets-sansio (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2888">#2888</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/8d397c73191b49c6d5280098d7c09dbe474e00bf"><code>8d397c7</code></a>
  Version 0.43.0 (<a href="https://redirect.github.com/Kludex/uvicorn/issues/2885">#2885</a>)</li>
  <li><a
  href="https://github.com/Kludex/uvicorn/commit/587042d68ff6c813ec0d8cfafaa820ebe7229d23"><code>587042d</code></a>
  🐛 Emit <code>http.disconnect</code> ASGI <code>receive()</code> event on server shutting down for
  s...</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/c9a75fb67b2e969253a41ef4ad447e013eee879e"><code>c9a75fb</code></a>
  chore(deps): bump the github-actions group with 3 updates (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2878">#2878</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/84fd578224e36766efb056585cb6cc5171270089"><code>84fd578</code></a>
  chore(deps): bump pygments from 2.19.2 to 2.20.0 (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2877">#2877</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/cd52d34b55d898180a65cfc01a6a88aac54c65c3"><code>cd52d34</code></a>
  Use native <code>context</code> parameter for <code>create_task</code> on Python 3.11+ (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2859">#2859</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/5211880320b2e99a532eb121808039404da234ab"><code>5211880</code></a>
  Drop cast in ASGI types (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2875">#2875</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/1cb8e747e2817ee46a4c0d44139e46b3b1f8fab6"><code>1cb8e74</code></a>
  Add websocket 500 fallback header test (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2874">#2874</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/28efbb24bd590f1f943cbc2bf84f197268a8c6d8"><code>28efbb2</code></a>
  chore(deps-dev): bump cryptography from 46.0.5 to 46.0.6 (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2873">#2873</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/Kludex/uvicorn/compare/0.42.0...0.44.0">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=uvicorn&package-manager=uv&previous-version=0.42.0&new-version=0.44.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps**: Bump uvicorn from 0.44.0 to 0.46.0
  ([`5dd4603`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/5dd46033cbec494e293d9dd842470bf5c7d5da07))

Bumps [uvicorn](https://github.com/Kludex/uvicorn) from 0.44.0 to 0.46.0. - [Release
  notes](https://github.com/Kludex/uvicorn/releases) -
  [Changelog](https://github.com/Kludex/uvicorn/blob/main/docs/release-notes.md) -
  [Commits](https://github.com/Kludex/uvicorn/compare/0.44.0...0.46.0)

--- updated-dependencies: - dependency-name: uvicorn dependency-version: 0.46.0

dependency-type: direct:production

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps**: Bump uvicorn from 0.44.0 to 0.46.0
  ([#73](https://github.com/jakub-k-slys/substack-gateway-oss/pull/73),
  [`86d8929`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/86d8929c2024974d1fb44d7a425931a5dad99939))

Bumps [uvicorn](https://github.com/Kludex/uvicorn) from 0.44.0 to 0.46.0. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/Kludex/uvicorn/releases">uvicorn's
  releases</a>.</em></p> <blockquote> <h2>Version 0.46.0</h2> <h2>What's Changed</h2> <ul>
  <li>Support <code>ws_max_size</code> in <code>wsproto</code> implementation by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/uvicorn/pull/2915">Kludex/uvicorn#2915</a></li>
  <li>Support <code>ws_ping_interval</code> and <code>ws_ping_timeout</code> in <code>wsproto</code>
  implementation by <a href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/uvicorn/pull/2916">Kludex/uvicorn#2916</a></li> <li>Use
  <code>bytearray</code> for incoming WebSocket message buffer in websockets-sansio by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/uvicorn/pull/2917">Kludex/uvicorn#2917</a></li> </ul>
  <p><strong>Full Changelog</strong>: <a
  href="https://github.com/Kludex/uvicorn/compare/0.45.0...0.46.0">https://github.com/Kludex/uvicorn/compare/0.45.0...0.46.0</a></p>
  <h2>Version 0.45.0</h2> <h2>What's Changed</h2> <ul> <li>Preserve forwarded client ports in proxy
  headers middleware by <a href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/uvicorn/pull/2903">Kludex/uvicorn#2903</a></li>
  <li>Accept <code>os.PathLike</code> for <code>log_config</code> by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/uvicorn/pull/2905">Kludex/uvicorn#2905</a></li>
  <li>Accept <code>log_level</code> strings case-insensitively by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/uvicorn/pull/2907">Kludex/uvicorn#2907</a></li> <li>Raise
  helpful <code>ImportError</code> when PyYAML is missing for YAML log config by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/uvicorn/pull/2906">Kludex/uvicorn#2906</a></li>
  <li>Revert empty context for ASGI runs by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/uvicorn/pull/2911">Kludex/uvicorn#2911</a></li> <li>Add
  <code>--reset-contextvars</code> flag to isolate ASGI request context by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/uvicorn/pull/2912">Kludex/uvicorn#2912</a></li>
  <li>Revert &quot;Emit <code>http.disconnect</code> on server shutdown for streaming
  responses&quot; (<a href="https://redirect.github.com/Kludex/uvicorn/issues/2829">#2829</a>) by <a
  href="https://github.com/Kludex"><code>@​Kludex</code></a> in <a
  href="https://redirect.github.com/Kludex/uvicorn/pull/2913">Kludex/uvicorn#2913</a></li> </ul>
  <h2>New Contributors</h2> <ul> <li><a
  href="https://github.com/Krishnachaitanyakc"><code>@​Krishnachaitanyakc</code></a> made their
  first contribution in <a
  href="https://redirect.github.com/Kludex/uvicorn/pull/2870">Kludex/uvicorn#2870</a></li> </ul>
  <p><strong>Full Changelog</strong>: <a
  href="https://github.com/Kludex/uvicorn/compare/0.44.0...0.45.0">https://github.com/Kludex/uvicorn/compare/0.44.0...0.45.0</a></p>
  </blockquote> </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/Kludex/uvicorn/blob/main/docs/release-notes.md">uvicorn's
  changelog</a>.</em></p> <blockquote> <h2>0.46.0 (April 23, 2026)</h2> <h3>Added</h3> <ul>
  <li>Support <code>ws_max_size</code> in <code>wsproto</code> implementation (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2915">#2915</a>)</li> <li>Support
  <code>ws_ping_interval</code> and <code>ws_ping_timeout</code> in <code>wsproto</code>
  implementation (<a href="https://redirect.github.com/Kludex/uvicorn/issues/2916">#2916</a>)</li>
  </ul> <h3>Changed</h3> <ul> <li>Use <code>bytearray</code> for incoming WebSocket message buffer
  in <code>websockets-sansio</code> (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2917">#2917</a>)</li> </ul> <h2>0.45.0
  (April 21, 2026)</h2> <h3>Added</h3> <ul> <li>Add <code>--reset-contextvars</code> flag to isolate
  ASGI request context (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2912">#2912</a>)</li> <li>Accept
  <code>os.PathLike</code> for <code>log_config</code> (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2905">#2905</a>)</li> <li>Accept
  <code>log_level</code> strings case-insensitively (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2907">#2907</a>)</li> </ul>
  <h3>Changed</h3> <ul> <li>Revert &quot;Emit <code>http.disconnect</code> on server shutdown for
  streaming responses&quot; (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2913">#2913</a>)</li> <li>Revert
  &quot;Explicitly start ASGI run with empty context&quot; (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2911">#2911</a>)</li> </ul> <h3>Fixed</h3>
  <ul> <li>Preserve forwarded client ports in proxy headers middleware (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2903">#2903</a>)</li> <li>Raise helpful
  <code>ImportError</code> when PyYAML is missing for YAML log config (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2906">#2906</a>)</li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/Kludex/uvicorn/commit/b224045f5900b7f766743bcb16ba9fc3adea2606"><code>b224045</code></a>
  Version 0.46.0 (<a href="https://redirect.github.com/Kludex/uvicorn/issues/2918">#2918</a>)</li>
  <li><a
  href="https://github.com/Kludex/uvicorn/commit/7375b5bf66d962186d663e85615d4b4d956bf880"><code>7375b5b</code></a>
  Use <code>bytearray</code> for incoming WebSocket message buffer in websockets-sansio (#...</li>
  <li><a
  href="https://github.com/Kludex/uvicorn/commit/d438fb16fe2d23c7bbc2ca7094645cff1f116458"><code>d438fb1</code></a>
  Support <code>ws_ping_interval</code> and <code>ws_ping_timeout</code> in <code>wsproto</code>
  implementation ...</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/3e6b96446653d0156434bce529a14c80764c9eda"><code>3e6b964</code></a>
  Support <code>ws_max_size</code> in <code>wsproto</code> implementation (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2915">#2915</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/2c423bd82be169459ea254a61476de34767e0326"><code>2c423bd</code></a>
  Version 0.45.0 (<a href="https://redirect.github.com/Kludex/uvicorn/issues/2914">#2914</a>)</li>
  <li><a
  href="https://github.com/Kludex/uvicorn/commit/7f027f8e25e47668a9c2ce8b5c21b35054c48d02"><code>7f027f8</code></a>
  Revert &quot;Emit <code>http.disconnect</code> on server shutdown for streaming responses&quot;
  (#...</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/73a80c3cc87de269ed016e584a25e585ae6f2b44"><code>73a80c3</code></a>
  Add <code>--reset-contextvars</code> flag to isolate ASGI request context (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2912">#2912</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/45c0b568d38e9bf4f2f036bc2d79eb98b0e72f72"><code>45c0b56</code></a>
  Revert empty context for ASGI runs (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2911">#2911</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/850d92656de0cb5859ee5f6ba252e19ad3d38989"><code>850d926</code></a>
  Raise helpful <code>ImportError</code> when PyYAML is missing for YAML log config (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2906">#2906</a>)</li> <li><a
  href="https://github.com/Kludex/uvicorn/commit/fdcacb4b83bc686ea1ba9e50ffe5b8cfe49b3e00"><code>fdcacb4</code></a>
  Accept <code>log_level</code> strings case-insensitively (<a
  href="https://redirect.github.com/Kludex/uvicorn/issues/2907">#2907</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/Kludex/uvicorn/compare/0.44.0...0.46.0">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=uvicorn&package-manager=uv&previous-version=0.44.0&new-version=0.46.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump pytest from 9.0.2 to 9.0.3
  ([`88c5c41`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/88c5c41889df7f24e26be93cdb84b656d1b4e168))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 9.0.2 to 9.0.3. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/9.0.2...9.0.3)

--- updated-dependencies: - dependency-name: pytest dependency-version: 9.0.3

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump pytest from 9.0.2 to 9.0.3
  ([`974963a`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/974963a8fa22fcaef61e46ce486c50581aff4d7c))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 9.0.2 to 9.0.3. - [Release
  notes](https://github.com/pytest-dev/pytest/releases) -
  [Changelog](https://github.com/pytest-dev/pytest/blob/main/CHANGELOG.rst) -
  [Commits](https://github.com/pytest-dev/pytest/compare/9.0.2...9.0.3)

--- updated-dependencies: - dependency-name: pytest dependency-version: 9.0.3

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump pytest from 9.0.2 to 9.0.3
  ([#15](https://github.com/jakub-k-slys/substack-gateway-oss/pull/15),
  [`78ae0c1`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/78ae0c122a94a0f1114c6cb934d3cd71918640ea))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 9.0.2 to 9.0.3. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a
  href="https://github.com/pytest-dev/pytest/releases">pytest's releases</a>.</em></p> <blockquote>
  <h2>9.0.3</h2> <h1>pytest 9.0.3 (2026-04-07)</h1> <h2>Bug fixes</h2> <ul> <li> <p><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/12444">#12444</a>: Fixed
  <code>pytest.approx</code> which now correctly takes into account
  <code>~collections.abc.Mapping</code> keys order to compare them.</p> </li> <li> <p><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13634">#13634</a>: Blocking a
  <code>conftest.py</code> file using the <code>-p no:</code> option is now explicitly
  disallowed.</p> <p>Previously this resulted in an internal assertion failure during plugin
  loading.</p> <p>Pytest now raises a clear <code>UsageError</code> explaining that conftest files
  are not plugins and cannot be disabled via <code>-p</code>.</p> </li> <li> <p><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13734">#13734</a>: Fixed crash when a
  test raises an exceptiongroup with <code>__tracebackhide__ = True</code>.</p> </li> <li> <p><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14195">#14195</a>: Fixed an issue where
  non-string messages passed to <!-- raw HTML omitted -->unittest.TestCase.subTest()<!-- raw HTML
  omitted --> were not printed.</p> </li> <li> <p><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14343">#14343</a>: Fixed use of
  insecure temporary directory (CVE-2025-71176).</p> </li> </ul> <h2>Improved documentation</h2>
  <ul> <li><a href="https://redirect.github.com/pytest-dev/pytest/issues/13388">#13388</a>:
  Clarified documentation for <code>-p</code> vs <code>PYTEST_PLUGINS</code> plugin loading and
  fixed an incorrect <code>-p</code> example.</li> <li><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13731">#13731</a>: Clarified that
  capture fixtures (e.g. <code>capsys</code> and <code>capfd</code>) take precedence over the
  <code>-s</code> / <code>--capture=no</code> command-line options in <code>Accessing captured
  output from a test function &lt;accessing-captured-output&gt;</code>.</li> <li><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14088">#14088</a>: Clarified that the
  default <code>pytest_collection</code> hook sets <code>session.items</code> before it calls
  <code>pytest_collection_finish</code>, not after.</li> <li><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14255">#14255</a>: TOML integer log
  levels must be quoted: Updating reference documentation.</li> </ul> <h2>Contributor-facing
  changes</h2> <ul> <li> <p><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/12689">#12689</a>: The test reports are
  now published to Codecov from GitHub Actions. The test statistics is visible <a
  href="https://app.codecov.io/gh/pytest-dev/pytest/tests">on the web interface</a>.</p> <p>-- by
  <code>aleguy02</code></p> </li> </ul> </blockquote> </details> <details>
  <summary>Commits</summary> <ul> <li><a
  href="https://github.com/pytest-dev/pytest/commit/a7d58d7a21b78581e636bbbdea13c66ad1657c1e"><code>a7d58d7</code></a>
  Prepare release version 9.0.3</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/089d98199c253d8f89a040243bc4f2aa6cd5ab22"><code>089d981</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/14366">#14366</a>
  from bluetech/revert-14193-backport</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/8127eaf4ab7f6b2fdd0dc1b38343ec97aeef05ac"><code>8127eaf</code></a>
  Revert &quot;Fix: assertrepr_compare respects dict insertion order (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14050">#14050</a>) (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14193">#14193</a>)&quot;</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/99a7e6029e7a6e8d53e5df114b1346e035370241"><code>99a7e60</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/14363">#14363</a>
  from pytest-dev/patchback/backports/9.0.x/95d8423bd...</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/ddee02a578da30dd43aedc39c1c1f1aaadfcee95"><code>ddee02a</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/14343">#14343</a>
  from bluetech/cve-2025-71176-simple</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/74eac6916fee34726cb194f16c516e96fbd29619"><code>74eac69</code></a>
  doc: Update training info (<a

href="https://redirect.github.com/pytest-dev/pytest/issues/14298">#14298</a>) (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14301">#14301</a>)</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/f92dee777cfdb77d1c43633d02766ddf1f07c869"><code>f92dee7</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/14267">#14267</a>
  from pytest-dev/patchback/backports/9.0.x/d6fa26c62...</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/7ee58acc8777c31ac6cf388d01addf5a414a7439"><code>7ee58ac</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/12378">#12378</a>
  from Pierre-Sassoulas/fix-implicit-str-concat-and-d...</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/37da870d37e3a2f5177cae075c7b9ae279432bf8"><code>37da870</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/14259">#14259</a>
  from mitre88/patch-4 (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14268">#14268</a>)</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/c34bfa3b7acb65b594707c714f1d8461b0304eed"><code>c34bfa3</code></a>
  Add explanation for string context diffs (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14257">#14257</a>) (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14266">#14266</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/pytest-dev/pytest/compare/9.0.2...9.0.3">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=pytest&package-manager=uv&previous-version=9.0.2&new-version=9.0.3)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump pytest from 9.0.2 to 9.0.3
  ([#65](https://github.com/jakub-k-slys/substack-gateway-oss/pull/65),
  [`ed6c7b8`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/ed6c7b875f59c84796a644f29d2cfbca68aef5fc))

Bumps [pytest](https://github.com/pytest-dev/pytest) from 9.0.2 to 9.0.3. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a
  href="https://github.com/pytest-dev/pytest/releases">pytest's releases</a>.</em></p> <blockquote>
  <h2>9.0.3</h2> <h1>pytest 9.0.3 (2026-04-07)</h1> <h2>Bug fixes</h2> <ul> <li> <p><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/12444">#12444</a>: Fixed
  <code>pytest.approx</code> which now correctly takes into account
  <code>~collections.abc.Mapping</code> keys order to compare them.</p> </li> <li> <p><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13634">#13634</a>: Blocking a
  <code>conftest.py</code> file using the <code>-p no:</code> option is now explicitly
  disallowed.</p> <p>Previously this resulted in an internal assertion failure during plugin
  loading.</p> <p>Pytest now raises a clear <code>UsageError</code> explaining that conftest files
  are not plugins and cannot be disabled via <code>-p</code>.</p> </li> <li> <p><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13734">#13734</a>: Fixed crash when a
  test raises an exceptiongroup with <code>__tracebackhide__ = True</code>.</p> </li> <li> <p><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14195">#14195</a>: Fixed an issue where
  non-string messages passed to <!-- raw HTML omitted -->unittest.TestCase.subTest()<!-- raw HTML
  omitted --> were not printed.</p> </li> <li> <p><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14343">#14343</a>: Fixed use of
  insecure temporary directory (CVE-2025-71176).</p> </li> </ul> <h2>Improved documentation</h2>
  <ul> <li><a href="https://redirect.github.com/pytest-dev/pytest/issues/13388">#13388</a>:
  Clarified documentation for <code>-p</code> vs <code>PYTEST_PLUGINS</code> plugin loading and
  fixed an incorrect <code>-p</code> example.</li> <li><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/13731">#13731</a>: Clarified that
  capture fixtures (e.g. <code>capsys</code> and <code>capfd</code>) take precedence over the
  <code>-s</code> / <code>--capture=no</code> command-line options in <code>Accessing captured
  output from a test function &lt;accessing-captured-output&gt;</code>.</li> <li><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14088">#14088</a>: Clarified that the
  default <code>pytest_collection</code> hook sets <code>session.items</code> before it calls
  <code>pytest_collection_finish</code>, not after.</li> <li><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14255">#14255</a>: TOML integer log
  levels must be quoted: Updating reference documentation.</li> </ul> <h2>Contributor-facing
  changes</h2> <ul> <li> <p><a
  href="https://redirect.github.com/pytest-dev/pytest/issues/12689">#12689</a>: The test reports are
  now published to Codecov from GitHub Actions. The test statistics is visible <a
  href="https://app.codecov.io/gh/pytest-dev/pytest/tests">on the web interface</a>.</p> <p>-- by
  <code>aleguy02</code></p> </li> </ul> </blockquote> </details> <details>
  <summary>Commits</summary> <ul> <li><a
  href="https://github.com/pytest-dev/pytest/commit/a7d58d7a21b78581e636bbbdea13c66ad1657c1e"><code>a7d58d7</code></a>
  Prepare release version 9.0.3</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/089d98199c253d8f89a040243bc4f2aa6cd5ab22"><code>089d981</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/14366">#14366</a>
  from bluetech/revert-14193-backport</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/8127eaf4ab7f6b2fdd0dc1b38343ec97aeef05ac"><code>8127eaf</code></a>
  Revert &quot;Fix: assertrepr_compare respects dict insertion order (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14050">#14050</a>) (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14193">#14193</a>)&quot;</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/99a7e6029e7a6e8d53e5df114b1346e035370241"><code>99a7e60</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/14363">#14363</a>
  from pytest-dev/patchback/backports/9.0.x/95d8423bd...</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/ddee02a578da30dd43aedc39c1c1f1aaadfcee95"><code>ddee02a</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/14343">#14343</a>
  from bluetech/cve-2025-71176-simple</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/74eac6916fee34726cb194f16c516e96fbd29619"><code>74eac69</code></a>
  doc: Update training info (<a

href="https://redirect.github.com/pytest-dev/pytest/issues/14298">#14298</a>) (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14301">#14301</a>)</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/f92dee777cfdb77d1c43633d02766ddf1f07c869"><code>f92dee7</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/14267">#14267</a>
  from pytest-dev/patchback/backports/9.0.x/d6fa26c62...</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/7ee58acc8777c31ac6cf388d01addf5a414a7439"><code>7ee58ac</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/12378">#12378</a>
  from Pierre-Sassoulas/fix-implicit-str-concat-and-d...</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/37da870d37e3a2f5177cae075c7b9ae279432bf8"><code>37da870</code></a>
  Merge pull request <a href="https://redirect.github.com/pytest-dev/pytest/issues/14259">#14259</a>
  from mitre88/patch-4 (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14268">#14268</a>)</li> <li><a
  href="https://github.com/pytest-dev/pytest/commit/c34bfa3b7acb65b594707c714f1d8461b0304eed"><code>c34bfa3</code></a>
  Add explanation for string context diffs (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14257">#14257</a>) (<a
  href="https://redirect.github.com/pytest-dev/pytest/issues/14266">#14266</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/pytest-dev/pytest/compare/9.0.2...9.0.3">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=pytest&package-manager=uv&previous-version=9.0.2&new-version=9.0.3)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump respx from 0.22.0 to 0.23.0
  ([`a439c8c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/a439c8c3707622ebab239894bb07be87eb94c7c3))

Bumps [respx](https://github.com/lundberg/respx) from 0.22.0 to 0.23.0. - [Release
  notes](https://github.com/lundberg/respx/releases) -
  [Changelog](https://github.com/lundberg/respx/blob/master/CHANGELOG.md) -
  [Commits](https://github.com/lundberg/respx/compare/0.22.0...0.23.0)

--- updated-dependencies: - dependency-name: respx dependency-version: 0.23.0

dependency-type: direct:development

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump respx from 0.22.0 to 0.23.0
  ([#12](https://github.com/jakub-k-slys/substack-gateway-oss/pull/12),
  [`d395427`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/d395427c2ca22a9ec55351addf7678b7aeb53116))

Bumps [respx](https://github.com/lundberg/respx) from 0.22.0 to 0.23.0. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/lundberg/respx/releases">respx's
  releases</a>.</em></p> <blockquote> <h2>Version 0.23.0</h2> <h2>0.23.0 (7th April 2026)</h2>
  <h3>Fixed</h3> <ul> <li>Fix <code>data</code> pattern with list value (<a
  href="https://redirect.github.com/lundberg/respx/issues/264">#264</a>)</li> <li>Fix and enhance
  incorrect documentations about iterable side effects (<a
  href="https://redirect.github.com/lundberg/respx/issues/287">#287</a>)</li> <li>Fix documentation
  typo, thanks <a href="https://github.com/markhobson"><code>@​markhobson</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/298">#298</a>)</li> <li>Fix support for
  multiple slashes <code>//</code> in URL path by not using <code>urljoin</code> when prepending
  path, thanks <a href="https://github.com/lewiscollard"><code>@​lewiscollard</code></a> and <a
  href="https://github.com/Skeen"><code>@​Skeen</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/302">#302</a>)</li> <li>Type Route.respond
  json as <code>Any</code> to align with HTTPX, thanks <a
  href="https://github.com/JacobHayes"><code>@​JacobHayes</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/284">#284</a>)</li> <li>Properly handle
  <code>ANY</code> in <code>MuitiItems</code> patterns (<a
  href="https://redirect.github.com/lundberg/respx/issues/289">#289</a>)</li> </ul> <h3>CI</h3> <ul>
  <li>Fix test warnings (<a
  href="https://redirect.github.com/lundberg/respx/issues/267">#267</a>)</li> <li>Add Python 3.14 to
  test matrix, thanks <a
  href="https://github.com/carlosdorneles-mb"><code>@​carlosdorneles-mb</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/300">#300</a>)</li> <li>Update nix flake,
  mypy target and workflows (<a
  href="https://redirect.github.com/lundberg/respx/issues/306">#306</a>, <a
  href="https://redirect.github.com/lundberg/respx/issues/282">#282</a>)</li> </ul> </blockquote>
  </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/lundberg/respx/blob/master/CHANGELOG.md">respx's changelog</a>.</em></p>
  <blockquote> <h2>[0.23.0] - 2026-04-07</h2> <h3>Fixed</h3> <ul> <li>Fix <code>data</code> pattern
  with list value (<a href="https://redirect.github.com/lundberg/respx/issues/264">#264</a>)</li>
  <li>Fix and enhance incorrect documentations about iterable side effects (<a
  href="https://redirect.github.com/lundberg/respx/issues/287">#287</a>)</li> <li>Fix documentation
  typo, thanks <a href="https://github.com/markhobson"><code>@​markhobson</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/298">#298</a>)</li> <li>Fix support for
  multiple slashes <code>//</code> in URL path by not using <code>urljoin</code> when prepending
  path, thanks <a href="https://github.com/lewiscollard"><code>@​lewiscollard</code></a> and <a
  href="https://github.com/Skeen"><code>@​Skeen</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/302">#302</a>)</li> <li>Type Route.respond
  json as <code>Any</code> to align with HTTPX, thanks <a
  href="https://github.com/JacobHayes"><code>@​JacobHayes</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/284">#284</a>)</li> <li>Properly handle
  <code>ANY</code> in <code>MuitiItems</code> patterns (<a
  href="https://redirect.github.com/lundberg/respx/issues/289">#289</a>)</li> </ul> <h3>CI</h3> <ul>
  <li>Fix test warnings (<a
  href="https://redirect.github.com/lundberg/respx/issues/267">#267</a>)</li> <li>Add Python 3.14 to
  test matrix, thanks <a
  href="https://github.com/carlosdorneles-mb"><code>@​carlosdorneles-mb</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/300">#300</a>)</li> <li>Update nix flake,
  mypy target and workflows (<a
  href="https://redirect.github.com/lundberg/respx/issues/306">#306</a>, <a
  href="https://redirect.github.com/lundberg/respx/issues/282">#282</a>)</li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/lundberg/respx/commit/62aaeabf2d55c9dcafa74ec086885850194e0dda"><code>62aaeab</code></a>
  Release <code>0.23.0</code></li> <li><a
  href="https://github.com/lundberg/respx/commit/d8edf3db92c4e6830301a4f4e51fe56b743e0ed9"><code>d8edf3d</code></a>
  Adjust badges</li> <li><a
  href="https://github.com/lundberg/respx/commit/b3a193d3a443472c9f0241599f02d89f4a3f33f9"><code>b3a193d</code></a>
  Add downloads badge to docs</li> <li><a
  href="https://github.com/lundberg/respx/commit/9961e9b79641635f3c891d8ded5c7e5aa3d8f049"><code>9961e9b</code></a>
  Handle multiple routes using <code>MuitiItems</code> pattern with <code>ANY</code> (<a
  href="https://redirect.github.com/lundberg/respx/issues/289">#289</a>)</li> <li><a
  href="https://github.com/lundberg/respx/commit/e51c2a6ffad066c78dedb0fc0e2fa27257f686f2"><code>e51c2a6</code></a>
  Update Route.respond json type hint to Any to match HTTPX (<a
  href="https://redirect.github.com/lundberg/respx/issues/284">#284</a>)</li> <li><a
  href="https://github.com/lundberg/respx/commit/a499260e28520ad6f19b06539f3321aa67f3f3b3"><code>a499260</code></a>
  Bump less-action/reusables from 8 to 10 (<a
  href="https://redirect.github.com/lundberg/respx/issues/282">#282</a>)</li> <li><a
  href="https://github.com/lundberg/respx/commit/7b44b512c8e44db460bbafaddb382444660c55f4"><code>7b44b51</code></a>
  Update nix flake and mypy target (<a
  href="https://redirect.github.com/lundberg/respx/issues/306">#306</a>)</li> <li><a
  href="https://github.com/lundberg/respx/commit/bf30cb3cdb8999879f8d921f03236ed25f52fdbf"><code>bf30cb3</code></a>
  Add Python 3.14 to test matrix (<a
  href="https://redirect.github.com/lundberg/respx/issues/300">#300</a>)</li> <li><a
  href="https://github.com/lundberg/respx/commit/c39612aabc7edc5038353973e7709dacb9d7cc8b"><code>c39612a</code></a>
  Don't use urljoin for prepending a forward slash to paths. (<a
  href="https://redirect.github.com/lundberg/respx/issues/302">#302</a>)</li> <li><a
  href="https://github.com/lundberg/respx/commit/0dbd8c8c5d4040309c6060809a60be93ae5fcba6"><code>0dbd8c8</code></a>
  Correct RESPX typo (<a href="https://redirect.github.com/lundberg/respx/issues/298">#298</a>)</li>
  <li>Additional commits viewable in <a
  href="https://github.com/lundberg/respx/compare/0.22.0...0.23.0">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=respx&package-manager=uv&previous-version=0.22.0&new-version=0.23.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump respx from 0.22.0 to 0.23.1
  ([`4c75dfe`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/4c75dfe156c9342eda83d6264ea65f9c403fe69e))

Bumps [respx](https://github.com/lundberg/respx) from 0.22.0 to 0.23.1. - [Release
  notes](https://github.com/lundberg/respx/releases) -
  [Changelog](https://github.com/lundberg/respx/blob/master/CHANGELOG.md) -
  [Commits](https://github.com/lundberg/respx/compare/0.22.0...0.23.1)

--- updated-dependencies: - dependency-name: respx dependency-version: 0.23.1

dependency-type: direct:development

update-type: version-update:semver-minor ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump respx from 0.22.0 to 0.23.1
  ([#64](https://github.com/jakub-k-slys/substack-gateway-oss/pull/64),
  [`791f07f`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/791f07f4ebd6b6619c5847e3db63795b7820be9a))

Bumps [respx](https://github.com/lundberg/respx) from 0.22.0 to 0.23.1. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/lundberg/respx/releases">respx's
  releases</a>.</em></p> <blockquote> <h2>Version 0.23.1</h2> <h2>0.23.1 (8th April 2026)</h2>
  <h3>Fixed</h3> <ul> <li>Fix regression causing <code>params</code> pattern to stop working under
  some conditions, by doing a strict detection of <code>ANY</code> in multi items patterns (<a
  href="https://redirect.github.com/lundberg/respx/issues/313">#313</a>)</li> </ul> <h3>CI</h3> <ul>
  <li>Update workflows actions (<a
  href="https://redirect.github.com/lundberg/respx/issues/310">#310</a>)</li> </ul> <h2>Version
  0.23.0</h2> <h2>0.23.0 (7th April 2026)</h2> <h3>Fixed</h3> <ul> <li>Fix <code>data</code> pattern
  with list value (<a href="https://redirect.github.com/lundberg/respx/issues/264">#264</a>)</li>
  <li>Fix and enhance incorrect documentations about iterable side effects (<a
  href="https://redirect.github.com/lundberg/respx/issues/287">#287</a>)</li> <li>Fix documentation
  typo, thanks <a href="https://github.com/markhobson"><code>@​markhobson</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/298">#298</a>)</li> <li>Fix support for
  multiple slashes <code>//</code> in URL path by not using <code>urljoin</code> when prepending
  path, thanks <a href="https://github.com/lewiscollard"><code>@​lewiscollard</code></a> and <a
  href="https://github.com/Skeen"><code>@​Skeen</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/302">#302</a>)</li> <li>Type Route.respond
  json as <code>Any</code> to align with HTTPX, thanks <a
  href="https://github.com/JacobHayes"><code>@​JacobHayes</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/284">#284</a>)</li> <li>Properly handle
  <code>ANY</code> in <code>MuitiItems</code> patterns (<a
  href="https://redirect.github.com/lundberg/respx/issues/289">#289</a>)</li> </ul> <h3>CI</h3> <ul>
  <li>Fix test warnings (<a
  href="https://redirect.github.com/lundberg/respx/issues/267">#267</a>)</li> <li>Add Python 3.14 to
  test matrix, thanks <a
  href="https://github.com/carlosdorneles-mb"><code>@​carlosdorneles-mb</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/300">#300</a>)</li> <li>Update nix flake,
  mypy target and workflows (<a
  href="https://redirect.github.com/lundberg/respx/issues/306">#306</a>, <a
  href="https://redirect.github.com/lundberg/respx/issues/282">#282</a>)</li> </ul> </blockquote>
  </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/lundberg/respx/blob/master/CHANGELOG.md">respx's changelog</a>.</em></p>
  <blockquote> <h2>[0.23.1] - 2026-04-08</h2> <h3>Fixed</h3> <ul> <li>Fix regression causing
  <code>params</code> pattern to stop working under some conditions, by doing a strict detection of
  <code>ANY</code> in multi items patterns (<a
  href="https://redirect.github.com/lundberg/respx/issues/313">#313</a>)</li> </ul> <h3>CI</h3> <ul>
  <li>Update workflows actions (<a
  href="https://redirect.github.com/lundberg/respx/issues/310">#310</a>)</li> </ul> <h2>[0.23.0] -
  2026-04-07</h2> <h3>Fixed</h3> <ul> <li>Fix <code>data</code> pattern with list value (<a
  href="https://redirect.github.com/lundberg/respx/issues/264">#264</a>)</li> <li>Fix and enhance
  incorrect documentations about iterable side effects (<a
  href="https://redirect.github.com/lundberg/respx/issues/287">#287</a>)</li> <li>Fix documentation
  typo, thanks <a href="https://github.com/markhobson"><code>@​markhobson</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/298">#298</a>)</li> <li>Fix support for
  multiple slashes <code>//</code> in URL path by not using <code>urljoin</code> when prepending
  path, thanks <a href="https://github.com/lewiscollard"><code>@​lewiscollard</code></a> and <a
  href="https://github.com/Skeen"><code>@​Skeen</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/302">#302</a>)</li> <li>Type Route.respond
  json as <code>Any</code> to align with HTTPX, thanks <a
  href="https://github.com/JacobHayes"><code>@​JacobHayes</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/284">#284</a>)</li> <li>Properly handle
  <code>ANY</code> in <code>MuitiItems</code> patterns (<a
  href="https://redirect.github.com/lundberg/respx/issues/289">#289</a>)</li> </ul> <h3>CI</h3> <ul>
  <li>Fix test warnings (<a
  href="https://redirect.github.com/lundberg/respx/issues/267">#267</a>)</li> <li>Add Python 3.14 to
  test matrix, thanks <a
  href="https://github.com/carlosdorneles-mb"><code>@​carlosdorneles-mb</code></a> (<a
  href="https://redirect.github.com/lundberg/respx/issues/300">#300</a>)</li> <li>Update nix flake,
  mypy target and workflows (<a
  href="https://redirect.github.com/lundberg/respx/issues/306">#306</a>, <a
  href="https://redirect.github.com/lundberg/respx/issues/282">#282</a>)</li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/lundberg/respx/commit/fc8b43bc74a69d07a6bdccf61522069b12bb8fad"><code>fc8b43b</code></a>
  Release <code>0.23.1</code></li> <li><a
  href="https://github.com/lundberg/respx/commit/1da5d2ff487122de3648efd4ad8d33ae9a1a5393"><code>1da5d2f</code></a>
  Strict detection of <code>ANY</code> in multi items patterns (<a
  href="https://redirect.github.com/lundberg/respx/issues/313">#313</a>)</li> <li><a
  href="https://github.com/lundberg/respx/commit/6f1bf70576eb7a024272c82cd84fb523d50fe9e9"><code>6f1bf70</code></a>
  Bump checkout and python actions (<a
  href="https://redirect.github.com/lundberg/respx/issues/310">#310</a>)</li> <li><a
  href="https://github.com/lundberg/respx/commit/62aaeabf2d55c9dcafa74ec086885850194e0dda"><code>62aaeab</code></a>
  Release <code>0.23.0</code></li> <li><a
  href="https://github.com/lundberg/respx/commit/d8edf3db92c4e6830301a4f4e51fe56b743e0ed9"><code>d8edf3d</code></a>
  Adjust badges</li> <li><a
  href="https://github.com/lundberg/respx/commit/b3a193d3a443472c9f0241599f02d89f4a3f33f9"><code>b3a193d</code></a>
  Add downloads badge to docs</li> <li><a
  href="https://github.com/lundberg/respx/commit/9961e9b79641635f3c891d8ded5c7e5aa3d8f049"><code>9961e9b</code></a>
  Handle multiple routes using <code>MuitiItems</code> pattern with <code>ANY</code> (<a
  href="https://redirect.github.com/lundberg/respx/issues/289">#289</a>)</li> <li><a
  href="https://github.com/lundberg/respx/commit/e51c2a6ffad066c78dedb0fc0e2fa27257f686f2"><code>e51c2a6</code></a>
  Update Route.respond json type hint to Any to match HTTPX (<a
  href="https://redirect.github.com/lundberg/respx/issues/284">#284</a>)</li> <li><a
  href="https://github.com/lundberg/respx/commit/a499260e28520ad6f19b06539f3321aa67f3f3b3"><code>a499260</code></a>
  Bump less-action/reusables from 8 to 10 (<a
  href="https://redirect.github.com/lundberg/respx/issues/282">#282</a>)</li> <li><a
  href="https://github.com/lundberg/respx/commit/7b44b512c8e44db460bbafaddb382444660c55f4"><code>7b44b51</code></a>
  Update nix flake and mypy target (<a
  href="https://redirect.github.com/lundberg/respx/issues/306">#306</a>)</li> <li>Additional commits
  viewable in <a href="https://github.com/lundberg/respx/compare/0.22.0...0.23.1">compare
  view</a></li> </ul> </details> <br />

- **deps-dev**: Bump ruff from 0.15.4 to 0.15.7
  ([`4e9a23c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/4e9a23c857b3bab071ff1c7f1d0484c6aa2e9bc9))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.4 to 0.15.7. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/0.15.4...0.15.7)

--- updated-dependencies: - dependency-name: ruff dependency-version: 0.15.7

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.15.4 to 0.15.7
  ([#50](https://github.com/jakub-k-slys/substack-gateway-oss/pull/50),
  [`b03bd1c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/b03bd1cbd978f54098a090afb710c6479ab04f9e))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.4 to 0.15.7. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.15.7</h2> <h2>Release Notes</h2> <p>Released on
  2026-03-19.</p> <h3>Preview features</h3> <ul> <li>Display output severity in preview (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23845">#23845</a>)</li> <li>Don't show
  <code>noqa</code> hover for non-Python documents (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24040">#24040</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>pycodestyle</code>] Recognize <code>pyrefly:</code> as a pragma
  comment (<code>E501</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24019">#24019</a>)</li> </ul>
  <h3>Server</h3> <ul> <li>Don't return code actions for non-Python documents (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23905">#23905</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Add company AI policy to contributing guide (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24021">#24021</a>)</li> <li>Document editor
  features for Markdown code formatting (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23924">#23924</a>)</li>
  <li>[<code>pylint</code>] Improve phrasing (<code>PLC0208</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24033">#24033</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Use PEP 639 license information (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/19661">#19661</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/tmimmanuel"><code>@​tmimmanuel</code></a></li> <li><a
  href="https://github.com/DimitriPapadopoulos"><code>@​DimitriPapadopoulos</code></a></li> <li><a
  href="https://github.com/amyreese"><code>@​amyreese</code></a></li> <li><a
  href="https://github.com/statxc"><code>@​statxc</code></a></li> <li><a
  href="https://github.com/dylwil3"><code>@​dylwil3</code></a></li> <li><a
  href="https://github.com/hunterhogan"><code>@​hunterhogan</code></a></li> <li><a
  href="https://github.com/renovate"><code>@​renovate</code></a></li> </ul> <h2>Install ruff
  0.15.7</h2> <h3>Install prebuilt binaries via shell script</h3> <pre lang="sh"><code>curl --proto
  '=https' --tlsv1.2 -LsSf
  https://releases.astral.sh/github/ruff/releases/download/0.15.7/ruff-installer.sh | sh
  </code></pre> <h3>Install prebuilt binaries via powershell script</h3> <pre
  lang="sh"><code>powershell -ExecutionPolicy Bypass -c &quot;irm
  https://releases.astral.sh/github/ruff/releases/download/0.15.7/ruff-installer.ps1 | iex&quot;
  &lt;/tr&gt;&lt;/table&gt; </code></pre> </blockquote> <p>... (truncated)</p> </details> <details>
  <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
  <blockquote> <h2>0.15.7</h2> <p>Released on 2026-03-19.</p> <h3>Preview features</h3> <ul>
  <li>Display output severity in preview (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23845">#23845</a>)</li> <li>Don't show
  <code>noqa</code> hover for non-Python documents (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24040">#24040</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>pycodestyle</code>] Recognize <code>pyrefly:</code> as a pragma
  comment (<code>E501</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24019">#24019</a>)</li> </ul>
  <h3>Server</h3> <ul> <li>Don't return code actions for non-Python documents (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23905">#23905</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Add company AI policy to contributing guide (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24021">#24021</a>)</li> <li>Document editor
  features for Markdown code formatting (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23924">#23924</a>)</li>
  <li>[<code>pylint</code>] Improve phrasing (<code>PLC0208</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24033">#24033</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Use PEP 639 license information (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/19661">#19661</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/tmimmanuel"><code>@​tmimmanuel</code></a></li> <li><a
  href="https://github.com/DimitriPapadopoulos"><code>@​DimitriPapadopoulos</code></a></li> <li><a
  href="https://github.com/amyreese"><code>@​amyreese</code></a></li> <li><a
  href="https://github.com/statxc"><code>@​statxc</code></a></li> <li><a
  href="https://github.com/dylwil3"><code>@​dylwil3</code></a></li> <li><a
  href="https://github.com/hunterhogan"><code>@​hunterhogan</code></a></li> <li><a
  href="https://github.com/renovate"><code>@​renovate</code></a></li> </ul> <h2>0.15.6</h2>
  <p>Released on 2026-03-12.</p> <h3>Preview features</h3> <ul> <li>Add support for
  <code>lazy</code> import parsing (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23755">#23755</a>)</li> <li>Add support for
  star-unpacking of comprehensions (PEP 798) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23788">#23788</a>)</li> <li>Reject semantic
  syntax errors for lazy imports (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23757">#23757</a>)</li> <li>Drop a few rules
  from the preview default set (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23879">#23879</a>)</li>
  <li>[<code>airflow</code>] Flag <code>Variable.get()</code> calls outside of task execution
  context (<code>AIR003</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23584">#23584</a>)</li>
  <li>[<code>airflow</code>] Flag runtime-varying values in DAG/task constructor arguments
  (<code>AIR304</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23631">#23631</a>)</li>
  <li>[<code>flake8-bugbear</code>] Implement <code>delattr-with-constant</code> (<code>B043</code>)
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/23737">#23737</a>)</li> </ul> <!-- raw
  HTML omitted --> </blockquote> <p>... (truncated)</p> </details> <details>
  <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ruff/commit/0ef39de46c006994fb1e90f7bd4ba09c0b2c1f79"><code>0ef39de</code></a>
  Bump 0.15.7 (<a href="https://redirect.github.com/astral-sh/ruff/issues/24049">#24049</a>)</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/beb543b5c666be9fd3f13c88df818f202b63e9d0"><code>beb543b</code></a>
  [ty] ecosystem-analyzer: Fail on newly panicking projects (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24043">#24043</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/378fe730929ccd67a7f2426b3012093da814b31d"><code>378fe73</code></a>
  Don't show noqa hover for non-Python documents (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24040">#24040</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/b5665bd18eecab4d3b5ab1256b36904cd99a4c57"><code>b5665bd</code></a>
  [<code>pylint</code>] Improve phrasing (<code>PLC0208</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24033">#24033</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/6e20f2219020e61eeae29458013d2d3684f75a79"><code>6e20f22</code></a>
  test: migrate <code>show_settings</code> and <code>version</code> tests to use
  <code>CliTest</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/23702">#23702</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/f99b284c1fe1399a82da7f6669467488017d44a7"><code>f99b284</code></a>
  Drain file watcher events during test setup (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24030">#24030</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/744c996c35016a8c0e05aa2823f4f822ac7b842c"><code>744c996</code></a>
  [ty] Filter out unsatisfiable inference attempts during generic call narrowin...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/16160958bdafb6106b6fffc72ffe2e4db0c0ac33"><code>1616095</code></a>
  [ty] Avoid inferring intersection types for call arguments (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/23933">#23933</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/7f275f431bf8c60d59601b74d441e9f4bef89f35"><code>7f275f4</code></a>
  [ty] Pin mypy_primer in <code>setup_primer_project.py</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24020">#24020</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/7255e362e4b171a641222279cd28d2ca88a74fdc"><code>7255e36</code></a>
  [<code>pycodestyle</code>] Recognize <code>pyrefly:</code> as a pragma comment (<code>E501</code>)
  (<a href="https://redirect.github.com/astral-sh/ruff/issues/24019">#24019</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.15.4...0.15.7">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ruff&package-manager=uv&previous-version=0.15.4&new-version=0.15.7)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ruff from 0.15.6 to 0.15.7
  ([`628cdad`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/628cdad32b2c058acbd150dde8ec6d68149b898e))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.6 to 0.15.7. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/0.15.6...0.15.7)

--- updated-dependencies: - dependency-name: ruff dependency-version: 0.15.7

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.15.6 to 0.15.7
  ([#4](https://github.com/jakub-k-slys/substack-gateway-oss/pull/4),
  [`5c50070`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/5c50070e94e963fb3ed50e5a9cfbb58a2bab826b))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.6 to 0.15.7. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.15.7</h2> <h2>Release Notes</h2> <p>Released on
  2026-03-19.</p> <h3>Preview features</h3> <ul> <li>Display output severity in preview (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23845">#23845</a>)</li> <li>Don't show
  <code>noqa</code> hover for non-Python documents (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24040">#24040</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>pycodestyle</code>] Recognize <code>pyrefly:</code> as a pragma
  comment (<code>E501</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24019">#24019</a>)</li> </ul>
  <h3>Server</h3> <ul> <li>Don't return code actions for non-Python documents (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23905">#23905</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Add company AI policy to contributing guide (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24021">#24021</a>)</li> <li>Document editor
  features for Markdown code formatting (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23924">#23924</a>)</li>
  <li>[<code>pylint</code>] Improve phrasing (<code>PLC0208</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24033">#24033</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Use PEP 639 license information (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/19661">#19661</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/tmimmanuel"><code>@​tmimmanuel</code></a></li> <li><a
  href="https://github.com/DimitriPapadopoulos"><code>@​DimitriPapadopoulos</code></a></li> <li><a
  href="https://github.com/amyreese"><code>@​amyreese</code></a></li> <li><a
  href="https://github.com/statxc"><code>@​statxc</code></a></li> <li><a
  href="https://github.com/dylwil3"><code>@​dylwil3</code></a></li> <li><a
  href="https://github.com/hunterhogan"><code>@​hunterhogan</code></a></li> <li><a
  href="https://github.com/renovate"><code>@​renovate</code></a></li> </ul> <h2>Install ruff
  0.15.7</h2> <h3>Install prebuilt binaries via shell script</h3> <pre lang="sh"><code>curl --proto
  '=https' --tlsv1.2 -LsSf
  https://releases.astral.sh/github/ruff/releases/download/0.15.7/ruff-installer.sh | sh
  </code></pre> <h3>Install prebuilt binaries via powershell script</h3> <pre
  lang="sh"><code>powershell -ExecutionPolicy Bypass -c &quot;irm
  https://releases.astral.sh/github/ruff/releases/download/0.15.7/ruff-installer.ps1 | iex&quot;
  &lt;/tr&gt;&lt;/table&gt; </code></pre> </blockquote> <p>... (truncated)</p> </details> <details>
  <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
  <blockquote> <h2>0.15.7</h2> <p>Released on 2026-03-19.</p> <h3>Preview features</h3> <ul>
  <li>Display output severity in preview (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23845">#23845</a>)</li> <li>Don't show
  <code>noqa</code> hover for non-Python documents (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24040">#24040</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>pycodestyle</code>] Recognize <code>pyrefly:</code> as a pragma
  comment (<code>E501</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24019">#24019</a>)</li> </ul>
  <h3>Server</h3> <ul> <li>Don't return code actions for non-Python documents (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23905">#23905</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Add company AI policy to contributing guide (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24021">#24021</a>)</li> <li>Document editor
  features for Markdown code formatting (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23924">#23924</a>)</li>
  <li>[<code>pylint</code>] Improve phrasing (<code>PLC0208</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24033">#24033</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Use PEP 639 license information (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/19661">#19661</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/tmimmanuel"><code>@​tmimmanuel</code></a></li> <li><a
  href="https://github.com/DimitriPapadopoulos"><code>@​DimitriPapadopoulos</code></a></li> <li><a
  href="https://github.com/amyreese"><code>@​amyreese</code></a></li> <li><a
  href="https://github.com/statxc"><code>@​statxc</code></a></li> <li><a
  href="https://github.com/dylwil3"><code>@​dylwil3</code></a></li> <li><a
  href="https://github.com/hunterhogan"><code>@​hunterhogan</code></a></li> <li><a
  href="https://github.com/renovate"><code>@​renovate</code></a></li> </ul> </blockquote> </details>
  <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ruff/commit/0ef39de46c006994fb1e90f7bd4ba09c0b2c1f79"><code>0ef39de</code></a>
  Bump 0.15.7 (<a href="https://redirect.github.com/astral-sh/ruff/issues/24049">#24049</a>)</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/beb543b5c666be9fd3f13c88df818f202b63e9d0"><code>beb543b</code></a>
  [ty] ecosystem-analyzer: Fail on newly panicking projects (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24043">#24043</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/378fe730929ccd67a7f2426b3012093da814b31d"><code>378fe73</code></a>
  Don't show noqa hover for non-Python documents (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24040">#24040</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/b5665bd18eecab4d3b5ab1256b36904cd99a4c57"><code>b5665bd</code></a>
  [<code>pylint</code>] Improve phrasing (<code>PLC0208</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24033">#24033</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/6e20f2219020e61eeae29458013d2d3684f75a79"><code>6e20f22</code></a>
  test: migrate <code>show_settings</code> and <code>version</code> tests to use
  <code>CliTest</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/23702">#23702</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/f99b284c1fe1399a82da7f6669467488017d44a7"><code>f99b284</code></a>
  Drain file watcher events during test setup (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24030">#24030</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/744c996c35016a8c0e05aa2823f4f822ac7b842c"><code>744c996</code></a>
  [ty] Filter out unsatisfiable inference attempts during generic call narrowin...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/16160958bdafb6106b6fffc72ffe2e4db0c0ac33"><code>1616095</code></a>
  [ty] Avoid inferring intersection types for call arguments (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/23933">#23933</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/7f275f431bf8c60d59601b74d441e9f4bef89f35"><code>7f275f4</code></a>
  [ty] Pin mypy_primer in <code>setup_primer_project.py</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24020">#24020</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/7255e362e4b171a641222279cd28d2ca88a74fdc"><code>7255e36</code></a>
  [<code>pycodestyle</code>] Recognize <code>pyrefly:</code> as a pragma comment (<code>E501</code>)
  (<a href="https://redirect.github.com/astral-sh/ruff/issues/24019">#24019</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.15.6...0.15.7">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ruff&package-manager=uv&previous-version=0.15.6&new-version=0.15.7)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ruff from 0.15.7 to 0.15.8
  ([`3dcabf9`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/3dcabf99f4c17f8b0ea531358440ae948ca7c27b))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.7 to 0.15.8. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/0.15.7...0.15.8)

--- updated-dependencies: - dependency-name: ruff dependency-version: 0.15.8

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.15.7 to 0.15.8
  ([`e808f4d`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e808f4d951000f5185fa034f228469734f487497))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.7 to 0.15.8. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/0.15.7...0.15.8)

--- updated-dependencies: - dependency-name: ruff dependency-version: 0.15.8

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.15.7 to 0.15.8
  ([#10](https://github.com/jakub-k-slys/substack-gateway-oss/pull/10),
  [`7fff610`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/7fff6101898de03659a699b2809cc7442b13f71c))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.7 to 0.15.8. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.15.8</h2> <h2>Release Notes</h2> <p>Released on
  2026-03-26.</p> <h3>Preview features</h3> <ul> <li>[<code>ruff</code>] New rule
  <code>unnecessary-if</code> (<code>RUF050</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24114">#24114</a>)</li>
  <li>[<code>ruff</code>] New rule <code>useless-finally</code> (<code>RUF072</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24165">#24165</a>)</li>
  <li>[<code>ruff</code>] New rule <code>f-string-percent-format</code> (<code>RUF073</code>): warn
  when using <code>%</code> operator on an f-string (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24162">#24162</a>)</li>
  <li>[<code>pyflakes</code>] Recognize <code>frozendict</code> as a builtin for Python 3.15+ (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24100">#24100</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>[<code>flake8-async</code>] Use fully-qualified <code>anyio.lowlevel</code>
  import in autofix (<code>ASYNC115</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24166">#24166</a>)</li>
  <li>[<code>flake8-bandit</code>] Check tuple arguments for partial paths in <code>S607</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24080">#24080</a>)</li>
  <li>[<code>pyflakes</code>] Skip <code>undefined-name</code> (<code>F821</code>) for conditionally
  deleted variables (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24088">#24088</a>)</li>
  <li><code>E501</code>/<code>W505</code>/formatter: Exclude nested pragma comments from line width
  calculation (<a href="https://redirect.github.com/astral-sh/ruff/pull/24071">#24071</a>)</li>
  <li>Fix <code>%foo?</code> parsing in IPython assignment expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24152">#24152</a>)</li> <li><code>analyze
  graph</code>: resolve string imports that reference attributes, not just modules (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24058">#24058</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>eradicate</code>] ignore <code>ty: ignore</code> comments in
  <code>ERA001</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24192">#24192</a>)</li>
  <li>[<code>flake8-bandit</code>] Treat <code>sys.executable</code> as trusted input in
  <code>S603</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24106">#24106</a>)</li>
  <li>[<code>flake8-self</code>] Recognize <code>Self</code> annotation and <code>self</code>
  assignment in <code>SLF001</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24144">#24144</a>)</li>
  <li>[<code>pyflakes</code>] <code>F507</code>: Fix false negative for non-tuple RHS in
  <code>%</code>-formatting (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24142">#24142</a>)</li>
  <li>[<code>refurb</code>] Parenthesize generator arguments in <code>FURB142</code> fixer (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24200">#24200</a>)</li> </ul>
  <h3>Performance</h3> <ul> <li>Speed up diagnostic rendering (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24146">#24146</a>)</li> </ul>
  <h3>Server</h3> <ul> <li>Warn when Markdown files are skipped due to preview being disabled (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24150">#24150</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Clarify <code>extend-ignore</code> and <code>extend-select</code>
  settings documentation (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24064">#24064</a>)</li> <li>Mention AI
  policy in PR template (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24198">#24198</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Use trusted publishing for NPM packages (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24171">#24171</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a href="https://github.com/bitloi"><code>@​bitloi</code></a></li>
  <li><a href="https://github.com/Sim-hu"><code>@​Sim-hu</code></a></li> </ul> <!-- raw HTML omitted
  --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Changelog</summary>
  <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
  changelog</a>.</em></p> <blockquote> <h2>0.15.8</h2> <p>Released on 2026-03-26.</p> <h3>Preview
  features</h3> <ul> <li>[<code>ruff</code>] New rule <code>unnecessary-if</code>
  (<code>RUF050</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24114">#24114</a>)</li>
  <li>[<code>ruff</code>] New rule <code>useless-finally</code> (<code>RUF072</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24165">#24165</a>)</li>
  <li>[<code>ruff</code>] New rule <code>f-string-percent-format</code> (<code>RUF073</code>): warn
  when using <code>%</code> operator on an f-string (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24162">#24162</a>)</li>
  <li>[<code>pyflakes</code>] Recognize <code>frozendict</code> as a builtin for Python 3.15+ (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24100">#24100</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>[<code>flake8-async</code>] Use fully-qualified <code>anyio.lowlevel</code>
  import in autofix (<code>ASYNC115</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24166">#24166</a>)</li>
  <li>[<code>flake8-bandit</code>] Check tuple arguments for partial paths in <code>S607</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24080">#24080</a>)</li>
  <li>[<code>pyflakes</code>] Skip <code>undefined-name</code> (<code>F821</code>) for conditionally
  deleted variables (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24088">#24088</a>)</li>
  <li><code>E501</code>/<code>W505</code>/formatter: Exclude nested pragma comments from line width
  calculation (<a href="https://redirect.github.com/astral-sh/ruff/pull/24071">#24071</a>)</li>
  <li>Fix <code>%foo?</code> parsing in IPython assignment expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24152">#24152</a>)</li> <li><code>analyze
  graph</code>: resolve string imports that reference attributes, not just modules (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24058">#24058</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>eradicate</code>] ignore <code>ty: ignore</code> comments in
  <code>ERA001</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24192">#24192</a>)</li>
  <li>[<code>flake8-bandit</code>] Treat <code>sys.executable</code> as trusted input in
  <code>S603</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24106">#24106</a>)</li>
  <li>[<code>flake8-self</code>] Recognize <code>Self</code> annotation and <code>self</code>
  assignment in <code>SLF001</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24144">#24144</a>)</li>
  <li>[<code>pyflakes</code>] <code>F507</code>: Fix false negative for non-tuple RHS in
  <code>%</code>-formatting (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24142">#24142</a>)</li>
  <li>[<code>refurb</code>] Parenthesize generator arguments in <code>FURB142</code> fixer (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24200">#24200</a>)</li> </ul>
  <h3>Performance</h3> <ul> <li>Speed up diagnostic rendering (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24146">#24146</a>)</li> </ul>
  <h3>Server</h3> <ul> <li>Warn when Markdown files are skipped due to preview being disabled (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24150">#24150</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Clarify <code>extend-ignore</code> and <code>extend-select</code>
  settings documentation (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24064">#24064</a>)</li> <li>Mention AI
  policy in PR template (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24198">#24198</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Use trusted publishing for NPM packages (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24171">#24171</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a href="https://github.com/bitloi"><code>@​bitloi</code></a></li>
  <li><a href="https://github.com/Sim-hu"><code>@​Sim-hu</code></a></li> <li><a
  href="https://github.com/mvanhorn"><code>@​mvanhorn</code></a></li> </ul> <!-- raw HTML omitted
  --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Commits</summary> <ul>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/c2a8815842f9dc5d24ec19385eae0f1a7188b0d9"><code>c2a8815</code></a>
  Release 0.15.8 (<a href="https://redirect.github.com/astral-sh/ruff/issues/24217">#24217</a>)</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/d444d52e2b9cc8bc9a078c2bd4ff6ff993290209"><code>d444d52</code></a>
  [ty] Infer lambda expressions with <code>Callable</code> type context (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/22633">#22633</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/9622285ed0081fc688149f6efca87f127d9b18dd"><code>9622285</code></a>
  [ty] Autocomplete arguments if in arguments node (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24167">#24167</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/d81266252aaf0820346d55edbed79c4f25ba13d2"><code>d812662</code></a>
  Use the <code>release</code> environment in <code>publish-docs</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24214">#24214</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/eda2355832f7a9c58aef6febd3e061dc9c87509a"><code>eda2355</code></a>
  [ty] Show <code>Final</code> source in final assignment diagnostic (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24194">#24194</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/929eb5238c82bfadad4549ff526f02efc0163dd0"><code>929eb52</code></a>
  [ty] Enforce Final attribute assignment rules for annotated and augmented wri...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/34998be22ec3a77d398bbd55234ef8740f768329"><code>34998be</code></a>
  [ty] Fix typo in comment (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24211">#24211</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/560aca0b2828ee2ff1b4bcc5c5ef1ef4ced229d2"><code>560aca0</code></a>
  [ty] Minor simplifications to some benchmark code (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24209">#24209</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/683bae512d03d3727a7bcdbc5a0170dafa049583"><code>683bae5</code></a>
  [ty] Track non-terminal-call constraints in global scope (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/23245">#23245</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/4704c2a4ff3dde2fd29324346720e9516b4fe387"><code>4704c2a</code></a>
  [ty] Remove unnecessary intermediate collection in `StaticClassLiteral::field...</li>
  <li>Additional commits viewable in <a
  href="https://github.com/astral-sh/ruff/compare/0.15.7...0.15.8">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ruff&package-manager=uv&previous-version=0.15.7&new-version=0.15.8)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ruff from 0.15.7 to 0.15.8
  ([#56](https://github.com/jakub-k-slys/substack-gateway-oss/pull/56),
  [`84b73cf`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/84b73cf44725afa2d7da93d09ca30ff036f1aefe))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.7 to 0.15.8. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.15.8</h2> <h2>Release Notes</h2> <p>Released on
  2026-03-26.</p> <h3>Preview features</h3> <ul> <li>[<code>ruff</code>] New rule
  <code>unnecessary-if</code> (<code>RUF050</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24114">#24114</a>)</li>
  <li>[<code>ruff</code>] New rule <code>useless-finally</code> (<code>RUF072</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24165">#24165</a>)</li>
  <li>[<code>ruff</code>] New rule <code>f-string-percent-format</code> (<code>RUF073</code>): warn
  when using <code>%</code> operator on an f-string (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24162">#24162</a>)</li>
  <li>[<code>pyflakes</code>] Recognize <code>frozendict</code> as a builtin for Python 3.15+ (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24100">#24100</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>[<code>flake8-async</code>] Use fully-qualified <code>anyio.lowlevel</code>
  import in autofix (<code>ASYNC115</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24166">#24166</a>)</li>
  <li>[<code>flake8-bandit</code>] Check tuple arguments for partial paths in <code>S607</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24080">#24080</a>)</li>
  <li>[<code>pyflakes</code>] Skip <code>undefined-name</code> (<code>F821</code>) for conditionally
  deleted variables (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24088">#24088</a>)</li>
  <li><code>E501</code>/<code>W505</code>/formatter: Exclude nested pragma comments from line width
  calculation (<a href="https://redirect.github.com/astral-sh/ruff/pull/24071">#24071</a>)</li>
  <li>Fix <code>%foo?</code> parsing in IPython assignment expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24152">#24152</a>)</li> <li><code>analyze
  graph</code>: resolve string imports that reference attributes, not just modules (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24058">#24058</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>eradicate</code>] ignore <code>ty: ignore</code> comments in
  <code>ERA001</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24192">#24192</a>)</li>
  <li>[<code>flake8-bandit</code>] Treat <code>sys.executable</code> as trusted input in
  <code>S603</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24106">#24106</a>)</li>
  <li>[<code>flake8-self</code>] Recognize <code>Self</code> annotation and <code>self</code>
  assignment in <code>SLF001</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24144">#24144</a>)</li>
  <li>[<code>pyflakes</code>] <code>F507</code>: Fix false negative for non-tuple RHS in
  <code>%</code>-formatting (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24142">#24142</a>)</li>
  <li>[<code>refurb</code>] Parenthesize generator arguments in <code>FURB142</code> fixer (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24200">#24200</a>)</li> </ul>
  <h3>Performance</h3> <ul> <li>Speed up diagnostic rendering (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24146">#24146</a>)</li> </ul>
  <h3>Server</h3> <ul> <li>Warn when Markdown files are skipped due to preview being disabled (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24150">#24150</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Clarify <code>extend-ignore</code> and <code>extend-select</code>
  settings documentation (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24064">#24064</a>)</li> <li>Mention AI
  policy in PR template (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24198">#24198</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Use trusted publishing for NPM packages (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24171">#24171</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a href="https://github.com/bitloi"><code>@​bitloi</code></a></li>
  <li><a href="https://github.com/Sim-hu"><code>@​Sim-hu</code></a></li> </ul> <!-- raw HTML omitted
  --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Changelog</summary>
  <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
  changelog</a>.</em></p> <blockquote> <h2>0.15.8</h2> <p>Released on 2026-03-26.</p> <h3>Preview
  features</h3> <ul> <li>[<code>ruff</code>] New rule <code>unnecessary-if</code>
  (<code>RUF050</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24114">#24114</a>)</li>
  <li>[<code>ruff</code>] New rule <code>useless-finally</code> (<code>RUF072</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24165">#24165</a>)</li>
  <li>[<code>ruff</code>] New rule <code>f-string-percent-format</code> (<code>RUF073</code>): warn
  when using <code>%</code> operator on an f-string (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24162">#24162</a>)</li>
  <li>[<code>pyflakes</code>] Recognize <code>frozendict</code> as a builtin for Python 3.15+ (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24100">#24100</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>[<code>flake8-async</code>] Use fully-qualified <code>anyio.lowlevel</code>
  import in autofix (<code>ASYNC115</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24166">#24166</a>)</li>
  <li>[<code>flake8-bandit</code>] Check tuple arguments for partial paths in <code>S607</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24080">#24080</a>)</li>
  <li>[<code>pyflakes</code>] Skip <code>undefined-name</code> (<code>F821</code>) for conditionally
  deleted variables (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24088">#24088</a>)</li>
  <li><code>E501</code>/<code>W505</code>/formatter: Exclude nested pragma comments from line width
  calculation (<a href="https://redirect.github.com/astral-sh/ruff/pull/24071">#24071</a>)</li>
  <li>Fix <code>%foo?</code> parsing in IPython assignment expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24152">#24152</a>)</li> <li><code>analyze
  graph</code>: resolve string imports that reference attributes, not just modules (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24058">#24058</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>eradicate</code>] ignore <code>ty: ignore</code> comments in
  <code>ERA001</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24192">#24192</a>)</li>
  <li>[<code>flake8-bandit</code>] Treat <code>sys.executable</code> as trusted input in
  <code>S603</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24106">#24106</a>)</li>
  <li>[<code>flake8-self</code>] Recognize <code>Self</code> annotation and <code>self</code>
  assignment in <code>SLF001</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24144">#24144</a>)</li>
  <li>[<code>pyflakes</code>] <code>F507</code>: Fix false negative for non-tuple RHS in
  <code>%</code>-formatting (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24142">#24142</a>)</li>
  <li>[<code>refurb</code>] Parenthesize generator arguments in <code>FURB142</code> fixer (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24200">#24200</a>)</li> </ul>
  <h3>Performance</h3> <ul> <li>Speed up diagnostic rendering (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24146">#24146</a>)</li> </ul>
  <h3>Server</h3> <ul> <li>Warn when Markdown files are skipped due to preview being disabled (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24150">#24150</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Clarify <code>extend-ignore</code> and <code>extend-select</code>
  settings documentation (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24064">#24064</a>)</li> <li>Mention AI
  policy in PR template (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24198">#24198</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Use trusted publishing for NPM packages (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24171">#24171</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a href="https://github.com/bitloi"><code>@​bitloi</code></a></li>
  <li><a href="https://github.com/Sim-hu"><code>@​Sim-hu</code></a></li> <li><a
  href="https://github.com/mvanhorn"><code>@​mvanhorn</code></a></li> </ul> <!-- raw HTML omitted
  --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Commits</summary> <ul>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/c2a8815842f9dc5d24ec19385eae0f1a7188b0d9"><code>c2a8815</code></a>
  Release 0.15.8 (<a href="https://redirect.github.com/astral-sh/ruff/issues/24217">#24217</a>)</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/d444d52e2b9cc8bc9a078c2bd4ff6ff993290209"><code>d444d52</code></a>
  [ty] Infer lambda expressions with <code>Callable</code> type context (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/22633">#22633</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/9622285ed0081fc688149f6efca87f127d9b18dd"><code>9622285</code></a>
  [ty] Autocomplete arguments if in arguments node (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24167">#24167</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/d81266252aaf0820346d55edbed79c4f25ba13d2"><code>d812662</code></a>
  Use the <code>release</code> environment in <code>publish-docs</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24214">#24214</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/eda2355832f7a9c58aef6febd3e061dc9c87509a"><code>eda2355</code></a>
  [ty] Show <code>Final</code> source in final assignment diagnostic (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24194">#24194</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/929eb5238c82bfadad4549ff526f02efc0163dd0"><code>929eb52</code></a>
  [ty] Enforce Final attribute assignment rules for annotated and augmented wri...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/34998be22ec3a77d398bbd55234ef8740f768329"><code>34998be</code></a>
  [ty] Fix typo in comment (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24211">#24211</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/560aca0b2828ee2ff1b4bcc5c5ef1ef4ced229d2"><code>560aca0</code></a>
  [ty] Minor simplifications to some benchmark code (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24209">#24209</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/683bae512d03d3727a7bcdbc5a0170dafa049583"><code>683bae5</code></a>
  [ty] Track non-terminal-call constraints in global scope (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/23245">#23245</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/4704c2a4ff3dde2fd29324346720e9516b4fe387"><code>4704c2a</code></a>
  [ty] Remove unnecessary intermediate collection in `StaticClassLiteral::field...</li>
  <li>Additional commits viewable in <a
  href="https://github.com/astral-sh/ruff/compare/0.15.7...0.15.8">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ruff&package-manager=uv&previous-version=0.15.7&new-version=0.15.8)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ruff from 0.15.8 to 0.15.9
  ([`0d37dbd`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/0d37dbd72eba8628cd5bb5cf8c8e79ce7ca98fa1))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.8 to 0.15.9. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/0.15.8...0.15.9)

--- updated-dependencies: - dependency-name: ruff dependency-version: 0.15.9

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.15.8 to 0.15.9
  ([`03f2c08`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/03f2c080c25cd5ebdb797c114c6d2645c9d6bf50))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.8 to 0.15.9. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/0.15.8...0.15.9)

--- updated-dependencies: - dependency-name: ruff dependency-version: 0.15.9

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.15.8 to 0.15.9
  ([#13](https://github.com/jakub-k-slys/substack-gateway-oss/pull/13),
  [`c358c1a`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/c358c1a38d071dd00befc9301303e17d459cefb6))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.8 to 0.15.9. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.15.9</h2> <h2>Release Notes</h2> <p>Released on
  2026-04-02.</p> <h3>Preview features</h3> <ul> <li>[<code>pyflakes</code>] Flag annotated variable
  redeclarations as <code>F811</code> in preview mode (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24244">#24244</a>)</li>
  <li>[<code>ruff</code>] Allow dunder-named assignments in non-strict mode for <code>RUF067</code>
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24089">#24089</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>[<code>flake8-errmsg</code>] Avoid shadowing existing <code>msg</code> in fix
  for <code>EM101</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24363">#24363</a>)</li>
  <li>[<code>flake8-simplify</code>] Ignore pre-initialization references in <code>SIM113</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24235">#24235</a>)</li>
  <li>[<code>pycodestyle</code>] Fix <code>W391</code> fixes for consecutive empty notebook cells
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24236">#24236</a>)</li>
  <li>[<code>pyupgrade</code>] Fix <code>UP008</code> nested class matching (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24273">#24273</a>)</li>
  <li>[<code>pyupgrade</code>] Ignore strings with string-only escapes (<code>UP012</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16058">#16058</a>)</li>
  <li>[<code>ruff</code>] <code>RUF072</code>: skip formfeeds on dedent (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24308">#24308</a>)</li>
  <li>[<code>ruff</code>] Avoid re-using symbol in <code>RUF024</code> fix (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24316">#24316</a>)</li>
  <li>[<code>ruff</code>] Parenthesize expression in <code>RUF050</code> fix (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24234">#24234</a>)</li> <li>Disallow starred
  expressions as values of starred expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24280">#24280</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>flake8-simplify</code>] Suppress <code>SIM105</code> for
  <code>except*</code> before Python 3.12 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23869">#23869</a>)</li>
  <li>[<code>pyflakes</code>] Extend <code>F507</code> to flag <code>%</code>-format strings with
  zero placeholders (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24215">#24215</a>)</li>
  <li>[<code>pyupgrade</code>] <code>UP018</code> should detect more unnecessarily wrapped literals
  (UP018) (<a href="https://redirect.github.com/astral-sh/ruff/pull/24093">#24093</a>)</li>
  <li>[<code>pyupgrade</code>] Fix <code>UP008</code> callable scope handling to support lambdas (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24274">#24274</a>)</li>
  <li>[<code>ruff</code>] <code>RUF010</code>: Mark fix as unsafe when it deletes a comment (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24270">#24270</a>)</li> </ul>
  <h3>Formatter</h3> <ul> <li>Add <code>nested-string-quote-style</code> formatting option (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24312">#24312</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>[<code>flake8-bugbear</code>] Clarify RUF071 fix safety for
  non-path string comparisons (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24149">#24149</a>)</li>
  <li>[<code>flake8-type-checking</code>] Clarify import cycle wording for
  <code>TC001</code>/<code>TC002</code>/<code>TC003</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24322">#24322</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Avoid rendering fix lines with trailing whitespace after <code>|</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24343">#24343</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/tranhoangtu-it"><code>@​tranhoangtu-it</code></a></li> <li><a
  href="https://github.com/dylwil3"><code>@​dylwil3</code></a></li> <li><a
  href="https://github.com/zsol"><code>@​zsol</code></a></li> </ul> <!-- raw HTML omitted -->
  </blockquote> <p>... (truncated)</p> </details> <details> <summary>Changelog</summary>
  <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
  changelog</a>.</em></p> <blockquote> <h2>0.15.9</h2> <p>Released on 2026-04-02.</p> <h3>Preview
  features</h3> <ul> <li>[<code>pyflakes</code>] Flag annotated variable redeclarations as
  <code>F811</code> in preview mode (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24244">#24244</a>)</li>
  <li>[<code>ruff</code>] Allow dunder-named assignments in non-strict mode for <code>RUF067</code>
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24089">#24089</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>[<code>flake8-errmsg</code>] Avoid shadowing existing <code>msg</code> in fix
  for <code>EM101</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24363">#24363</a>)</li>
  <li>[<code>flake8-simplify</code>] Ignore pre-initialization references in <code>SIM113</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24235">#24235</a>)</li>
  <li>[<code>pycodestyle</code>] Fix <code>W391</code> fixes for consecutive empty notebook cells
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24236">#24236</a>)</li>
  <li>[<code>pyupgrade</code>] Fix <code>UP008</code> nested class matching (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24273">#24273</a>)</li>
  <li>[<code>pyupgrade</code>] Ignore strings with string-only escapes (<code>UP012</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16058">#16058</a>)</li>
  <li>[<code>ruff</code>] <code>RUF072</code>: skip formfeeds on dedent (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24308">#24308</a>)</li>
  <li>[<code>ruff</code>] Avoid re-using symbol in <code>RUF024</code> fix (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24316">#24316</a>)</li>
  <li>[<code>ruff</code>] Parenthesize expression in <code>RUF050</code> fix (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24234">#24234</a>)</li> <li>Disallow starred
  expressions as values of starred expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24280">#24280</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>flake8-simplify</code>] Suppress <code>SIM105</code> for
  <code>except*</code> before Python 3.12 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23869">#23869</a>)</li>
  <li>[<code>pyflakes</code>] Extend <code>F507</code> to flag <code>%</code>-format strings with
  zero placeholders (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24215">#24215</a>)</li>
  <li>[<code>pyupgrade</code>] <code>UP018</code> should detect more unnecessarily wrapped literals
  (UP018) (<a href="https://redirect.github.com/astral-sh/ruff/pull/24093">#24093</a>)</li>
  <li>[<code>pyupgrade</code>] Fix <code>UP008</code> callable scope handling to support lambdas (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24274">#24274</a>)</li>
  <li>[<code>ruff</code>] <code>RUF010</code>: Mark fix as unsafe when it deletes a comment (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24270">#24270</a>)</li> </ul>
  <h3>Formatter</h3> <ul> <li>Add <code>nested-string-quote-style</code> formatting option (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24312">#24312</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>[<code>flake8-bugbear</code>] Clarify RUF071 fix safety for
  non-path string comparisons (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24149">#24149</a>)</li>
  <li>[<code>flake8-type-checking</code>] Clarify import cycle wording for
  <code>TC001</code>/<code>TC002</code>/<code>TC003</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24322">#24322</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Avoid rendering fix lines with trailing whitespace after <code>|</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24343">#24343</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/tranhoangtu-it"><code>@​tranhoangtu-it</code></a></li> <li><a
  href="https://github.com/dylwil3"><code>@​dylwil3</code></a></li> <li><a
  href="https://github.com/zsol"><code>@​zsol</code></a></li> <li><a
  href="https://github.com/renovate"><code>@​renovate</code></a></li> </ul> <!-- raw HTML omitted
  --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Commits</summary> <ul>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/724ccc1ae8a61e872cf58435f2c073189dc248f2"><code>724ccc1</code></a>
  Bump 0.15.9 (<a href="https://redirect.github.com/astral-sh/ruff/issues/24369">#24369</a>)</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/96d9e0964cb87498ef15510ea7f896ba336659f9"><code>96d9e09</code></a>
  [ty] Move the <code>deferred</code> submodule inside <code>infer/builder</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24368">#24368</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/130da28d610a466721bb942e8a5e0ec47bbe3469"><code>130da28</code></a>
  [ty] Infer the <code>extra_items</code> keyword argument to class-based TypedDicts as an...</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/a617c54b0708a8c1eb850cc3b2a5caee21137a28"><code>a617c54</code></a>
  [ty] Validate type qualifiers in functional TypedDict fields and the `extra_i...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/d8517087c6cd0aa4f33dcede605ff642941dd74b"><code>d851708</code></a>
  [ty] Improve robustness of various type-qualifier-related checks (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24251">#24251</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/aecb5877c6d6fe035c03aba994ec3a7b935b8f02"><code>aecb587</code></a>
  Only run the release-gate on workflow dispatch (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24366">#24366</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/b88957174311030927bf564da32d05dee0eb89d9"><code>b889571</code></a>
  [ty] Use <code>infer_type_expression</code> for parsing parameter annotations and return...</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/3286a62be986a8d6d04d95b3bc619f06e012fa2f"><code>3286a62</code></a>
  Add a &quot;release-gate&quot; step to the release workflow (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24365">#24365</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/5f88756ee10e3faf0e96c883c34c95fc78200536"><code>5f88756</code></a>
  Disallow starred expressions as values of starred expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24280">#24280</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/5c59f8a46965cac3470f09972196c8620faa4626"><code>5c59f8a</code></a>
  [<code>pyupgrade</code>] Ignore strings with string-only escapes (<code>UP012</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16058">#16058</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.15.8...0.15.9">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ruff&package-manager=uv&previous-version=0.15.8&new-version=0.15.9)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ruff from 0.15.8 to 0.15.9
  ([#63](https://github.com/jakub-k-slys/substack-gateway-oss/pull/63),
  [`3a5e36c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/3a5e36c92fdf7db23092008d7183080f5b053889))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.8 to 0.15.9. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.15.9</h2> <h2>Release Notes</h2> <p>Released on
  2026-04-02.</p> <h3>Preview features</h3> <ul> <li>[<code>pyflakes</code>] Flag annotated variable
  redeclarations as <code>F811</code> in preview mode (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24244">#24244</a>)</li>
  <li>[<code>ruff</code>] Allow dunder-named assignments in non-strict mode for <code>RUF067</code>
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24089">#24089</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>[<code>flake8-errmsg</code>] Avoid shadowing existing <code>msg</code> in fix
  for <code>EM101</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24363">#24363</a>)</li>
  <li>[<code>flake8-simplify</code>] Ignore pre-initialization references in <code>SIM113</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24235">#24235</a>)</li>
  <li>[<code>pycodestyle</code>] Fix <code>W391</code> fixes for consecutive empty notebook cells
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24236">#24236</a>)</li>
  <li>[<code>pyupgrade</code>] Fix <code>UP008</code> nested class matching (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24273">#24273</a>)</li>
  <li>[<code>pyupgrade</code>] Ignore strings with string-only escapes (<code>UP012</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16058">#16058</a>)</li>
  <li>[<code>ruff</code>] <code>RUF072</code>: skip formfeeds on dedent (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24308">#24308</a>)</li>
  <li>[<code>ruff</code>] Avoid re-using symbol in <code>RUF024</code> fix (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24316">#24316</a>)</li>
  <li>[<code>ruff</code>] Parenthesize expression in <code>RUF050</code> fix (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24234">#24234</a>)</li> <li>Disallow starred
  expressions as values of starred expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24280">#24280</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>flake8-simplify</code>] Suppress <code>SIM105</code> for
  <code>except*</code> before Python 3.12 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23869">#23869</a>)</li>
  <li>[<code>pyflakes</code>] Extend <code>F507</code> to flag <code>%</code>-format strings with
  zero placeholders (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24215">#24215</a>)</li>
  <li>[<code>pyupgrade</code>] <code>UP018</code> should detect more unnecessarily wrapped literals
  (UP018) (<a href="https://redirect.github.com/astral-sh/ruff/pull/24093">#24093</a>)</li>
  <li>[<code>pyupgrade</code>] Fix <code>UP008</code> callable scope handling to support lambdas (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24274">#24274</a>)</li>
  <li>[<code>ruff</code>] <code>RUF010</code>: Mark fix as unsafe when it deletes a comment (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24270">#24270</a>)</li> </ul>
  <h3>Formatter</h3> <ul> <li>Add <code>nested-string-quote-style</code> formatting option (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24312">#24312</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>[<code>flake8-bugbear</code>] Clarify RUF071 fix safety for
  non-path string comparisons (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24149">#24149</a>)</li>
  <li>[<code>flake8-type-checking</code>] Clarify import cycle wording for
  <code>TC001</code>/<code>TC002</code>/<code>TC003</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24322">#24322</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Avoid rendering fix lines with trailing whitespace after <code>|</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24343">#24343</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/tranhoangtu-it"><code>@​tranhoangtu-it</code></a></li> <li><a
  href="https://github.com/dylwil3"><code>@​dylwil3</code></a></li> <li><a
  href="https://github.com/zsol"><code>@​zsol</code></a></li> </ul> <!-- raw HTML omitted -->
  </blockquote> <p>... (truncated)</p> </details> <details> <summary>Changelog</summary>
  <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
  changelog</a>.</em></p> <blockquote> <h2>0.15.9</h2> <p>Released on 2026-04-02.</p> <h3>Preview
  features</h3> <ul> <li>[<code>pyflakes</code>] Flag annotated variable redeclarations as
  <code>F811</code> in preview mode (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24244">#24244</a>)</li>
  <li>[<code>ruff</code>] Allow dunder-named assignments in non-strict mode for <code>RUF067</code>
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24089">#24089</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>[<code>flake8-errmsg</code>] Avoid shadowing existing <code>msg</code> in fix
  for <code>EM101</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24363">#24363</a>)</li>
  <li>[<code>flake8-simplify</code>] Ignore pre-initialization references in <code>SIM113</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24235">#24235</a>)</li>
  <li>[<code>pycodestyle</code>] Fix <code>W391</code> fixes for consecutive empty notebook cells
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24236">#24236</a>)</li>
  <li>[<code>pyupgrade</code>] Fix <code>UP008</code> nested class matching (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24273">#24273</a>)</li>
  <li>[<code>pyupgrade</code>] Ignore strings with string-only escapes (<code>UP012</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/16058">#16058</a>)</li>
  <li>[<code>ruff</code>] <code>RUF072</code>: skip formfeeds on dedent (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24308">#24308</a>)</li>
  <li>[<code>ruff</code>] Avoid re-using symbol in <code>RUF024</code> fix (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24316">#24316</a>)</li>
  <li>[<code>ruff</code>] Parenthesize expression in <code>RUF050</code> fix (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24234">#24234</a>)</li> <li>Disallow starred
  expressions as values of starred expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24280">#24280</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>flake8-simplify</code>] Suppress <code>SIM105</code> for
  <code>except*</code> before Python 3.12 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23869">#23869</a>)</li>
  <li>[<code>pyflakes</code>] Extend <code>F507</code> to flag <code>%</code>-format strings with
  zero placeholders (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24215">#24215</a>)</li>
  <li>[<code>pyupgrade</code>] <code>UP018</code> should detect more unnecessarily wrapped literals
  (UP018) (<a href="https://redirect.github.com/astral-sh/ruff/pull/24093">#24093</a>)</li>
  <li>[<code>pyupgrade</code>] Fix <code>UP008</code> callable scope handling to support lambdas (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24274">#24274</a>)</li>
  <li>[<code>ruff</code>] <code>RUF010</code>: Mark fix as unsafe when it deletes a comment (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24270">#24270</a>)</li> </ul>
  <h3>Formatter</h3> <ul> <li>Add <code>nested-string-quote-style</code> formatting option (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24312">#24312</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>[<code>flake8-bugbear</code>] Clarify RUF071 fix safety for
  non-path string comparisons (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24149">#24149</a>)</li>
  <li>[<code>flake8-type-checking</code>] Clarify import cycle wording for
  <code>TC001</code>/<code>TC002</code>/<code>TC003</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24322">#24322</a>)</li> </ul> <h3>Other
  changes</h3> <ul> <li>Avoid rendering fix lines with trailing whitespace after <code>|</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24343">#24343</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/tranhoangtu-it"><code>@​tranhoangtu-it</code></a></li> <li><a
  href="https://github.com/dylwil3"><code>@​dylwil3</code></a></li> <li><a
  href="https://github.com/zsol"><code>@​zsol</code></a></li> <li><a
  href="https://github.com/renovate"><code>@​renovate</code></a></li> </ul> <!-- raw HTML omitted
  --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Commits</summary> <ul>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/724ccc1ae8a61e872cf58435f2c073189dc248f2"><code>724ccc1</code></a>
  Bump 0.15.9 (<a href="https://redirect.github.com/astral-sh/ruff/issues/24369">#24369</a>)</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/96d9e0964cb87498ef15510ea7f896ba336659f9"><code>96d9e09</code></a>
  [ty] Move the <code>deferred</code> submodule inside <code>infer/builder</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24368">#24368</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/130da28d610a466721bb942e8a5e0ec47bbe3469"><code>130da28</code></a>
  [ty] Infer the <code>extra_items</code> keyword argument to class-based TypedDicts as an...</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/a617c54b0708a8c1eb850cc3b2a5caee21137a28"><code>a617c54</code></a>
  [ty] Validate type qualifiers in functional TypedDict fields and the `extra_i...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/d8517087c6cd0aa4f33dcede605ff642941dd74b"><code>d851708</code></a>
  [ty] Improve robustness of various type-qualifier-related checks (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24251">#24251</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/aecb5877c6d6fe035c03aba994ec3a7b935b8f02"><code>aecb587</code></a>
  Only run the release-gate on workflow dispatch (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24366">#24366</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/b88957174311030927bf564da32d05dee0eb89d9"><code>b889571</code></a>
  [ty] Use <code>infer_type_expression</code> for parsing parameter annotations and return...</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/3286a62be986a8d6d04d95b3bc619f06e012fa2f"><code>3286a62</code></a>
  Add a &quot;release-gate&quot; step to the release workflow (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24365">#24365</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/5f88756ee10e3faf0e96c883c34c95fc78200536"><code>5f88756</code></a>
  Disallow starred expressions as values of starred expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24280">#24280</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/5c59f8a46965cac3470f09972196c8620faa4626"><code>5c59f8a</code></a>
  [<code>pyupgrade</code>] Ignore strings with string-only escapes (<code>UP012</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/16058">#16058</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.15.8...0.15.9">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ruff&package-manager=uv&previous-version=0.15.8&new-version=0.15.9)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ruff from 0.15.9 to 0.15.10
  ([`16dc512`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/16dc512bd6541109f302417e525ef0a041d3a44d))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.9 to 0.15.10. - [Release
  notes](https://github.com/astral-sh/ruff/releases) -
  [Changelog](https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ruff/compare/0.15.9...0.15.10)

--- updated-dependencies: - dependency-name: ruff dependency-version: 0.15.10

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ruff from 0.15.9 to 0.15.10
  ([#69](https://github.com/jakub-k-slys/substack-gateway-oss/pull/69),
  [`eefa46b`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/eefa46b5c64870754bd0712dbec8d57df9c0ef1e))

Bumps [ruff](https://github.com/astral-sh/ruff) from 0.15.9 to 0.15.10. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's
  releases</a>.</em></p> <blockquote> <h2>0.15.10</h2> <h2>Release Notes</h2> <p>Released on
  2026-04-09.</p> <h3>Preview features</h3> <ul> <li>[<code>flake8-logging</code>] Allow closures in
  except handlers (<code>LOG004</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24464">#24464</a>)</li>
  <li>[<code>flake8-self</code>] Make <code>SLF</code> diagnostics robust to non-self-named
  variables (<a href="https://redirect.github.com/astral-sh/ruff/pull/24281">#24281</a>)</li>
  <li>[<code>flake8-simplify</code>] Make the fix for <code>collapsible-if</code> safe in
  <code>preview</code> (<code>SIM102</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24371">#24371</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>Avoid emitting multi-line f-string elements before Python 3.12 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24377">#24377</a>)</li> <li>Avoid syntax
  error from <code>E502</code> fixes in f-strings and t-strings (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24410">#24410</a>)</li> <li>Strip form feeds
  from indent passed to <code>dedent_to</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24381">#24381</a>)</li>
  <li>[<code>pyupgrade</code>] Fix panic caused by handling of octals (<code>UP012</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24390">#24390</a>)</li> <li>Reject
  multi-line f-string elements before Python 3.12 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24355">#24355</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>ruff</code>] Treat f-string interpolation as potential side effect
  (<code>RUF019</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24426">#24426</a>)</li> </ul>
  <h3>Server</h3> <ul> <li>Add support for custom file extensions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24463">#24463</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Document adding fixes in CONTRIBUTING.md (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24393">#24393</a>)</li> <li>Fix JSON typo in
  settings example (<a href="https://redirect.github.com/astral-sh/ruff/pull/24517">#24517</a>)</li>
  </ul> <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/dylwil3"><code>@​dylwil3</code></a></li> <li><a
  href="https://github.com/silverstein"><code>@​silverstein</code></a></li> <li><a
  href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li> <li><a
  href="https://github.com/shizukushq"><code>@​shizukushq</code></a></li> <li><a
  href="https://github.com/zanieb"><code>@​zanieb</code></a></li> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> </ul> <h2>Install ruff
  0.15.10</h2> <h3>Install prebuilt binaries via shell script</h3> <pre lang="sh"><code>curl --proto
  '=https' --tlsv1.2 -LsSf
  https://releases.astral.sh/github/ruff/releases/download/0.15.10/ruff-installer.sh | sh
  </code></pre> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details> <details>
  <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
  <blockquote> <h2>0.15.10</h2> <p>Released on 2026-04-09.</p> <h3>Preview features</h3> <ul>
  <li>[<code>flake8-logging</code>] Allow closures in except handlers (<code>LOG004</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24464">#24464</a>)</li>
  <li>[<code>flake8-self</code>] Make <code>SLF</code> diagnostics robust to non-self-named
  variables (<a href="https://redirect.github.com/astral-sh/ruff/pull/24281">#24281</a>)</li>
  <li>[<code>flake8-simplify</code>] Make the fix for <code>collapsible-if</code> safe in
  <code>preview</code> (<code>SIM102</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24371">#24371</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>Avoid emitting multi-line f-string elements before Python 3.12 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24377">#24377</a>)</li> <li>Avoid syntax
  error from <code>E502</code> fixes in f-strings and t-strings (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24410">#24410</a>)</li> <li>Strip form feeds
  from indent passed to <code>dedent_to</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24381">#24381</a>)</li>
  <li>[<code>pyupgrade</code>] Fix panic caused by handling of octals (<code>UP012</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24390">#24390</a>)</li> <li>Reject
  multi-line f-string elements before Python 3.12 (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24355">#24355</a>)</li> </ul> <h3>Rule
  changes</h3> <ul> <li>[<code>ruff</code>] Treat f-string interpolation as potential side effect
  (<code>RUF019</code>) (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24426">#24426</a>)</li> </ul>
  <h3>Server</h3> <ul> <li>Add support for custom file extensions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24463">#24463</a>)</li> </ul>
  <h3>Documentation</h3> <ul> <li>Document adding fixes in CONTRIBUTING.md (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24393">#24393</a>)</li> <li>Fix JSON typo in
  settings example (<a href="https://redirect.github.com/astral-sh/ruff/pull/24517">#24517</a>)</li>
  </ul> <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/dylwil3"><code>@​dylwil3</code></a></li> <li><a
  href="https://github.com/silverstein"><code>@​silverstein</code></a></li> <li><a
  href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li> <li><a
  href="https://github.com/shizukushq"><code>@​shizukushq</code></a></li> <li><a
  href="https://github.com/zanieb"><code>@​zanieb</code></a></li> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> </ul> </blockquote>
  </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ruff/commit/252f76102a618bff6537b6c53c316ca3837f4abf"><code>252f761</code></a>
  Bump 0.15.10 (<a href="https://redirect.github.com/astral-sh/ruff/issues/24519">#24519</a>)</li>
  <li><a
  href="https://github.com/astral-sh/ruff/commit/37a1ec8bb8e30955787b0cdf6e97f7f2254dba7f"><code>37a1ec8</code></a>
  [ty] Fix assignability of intersections with bounded typevars (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24502">#24502</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/f518cc9ca0c830773dd49c3964eb5e49d52c8aed"><code>f518cc9</code></a>
  [ty] Allow partially stringified <code>type[…]</code> annotations (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24518">#24518</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/16c4090d0a711b9c0523b932014f3daf140f35bc"><code>16c4090</code></a>
  docs: fix JSON typo in settings example (<a

href="https://redirect.github.com/astral-sh/ruff/issues/24517">#24517</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/99d97bd72f1934ac2af93e52468c10ef1c7a1a4e"><code>99d97bd</code></a>
  [ty] Tighten up a few edge cases in <code>Concatenate</code> type-expression parsing (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/2">#2</a>...</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/2714e345bdd64a5baae3844c0d25db7b0b9fe330"><code>2714e34</code></a>
  [ty] Enable <code>pull-diagnostics</code> by default in E2E tests (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24516">#24516</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/d8bc700722ab1b7272a4d724839da7c569b349d4"><code>d8bc700</code></a>
  LSP: Add support for custom extensions (<a

href="https://redirect.github.com/astral-sh/ruff/issues/24463">#24463</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/a45f96d65dbd4f958b07accd718f8d2af48cb956"><code>a45f96d</code></a>
  [ty] stop special-casing str constructor (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24514">#24514</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/87a0f01cfd016e0297ef05ab638cde006bf8d947"><code>87a0f01</code></a>
  [ruff] Treat f-string interpolation as potential side effect in RUF019 (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24426">#24426</a>)</li> <li><a
  href="https://github.com/astral-sh/ruff/commit/e9ba8489b8d1f1fd5fd66887a74d5f2f58f733d4"><code>e9ba848</code></a>
  [ty] Fix excess subscript argument inference for non-generic types (<a
  href="https://redirect.github.com/astral-sh/ruff/issues/24354">#24354</a>)</li> <li>Additional
  commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.15.9...0.15.10">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ruff&package-manager=uv&previous-version=0.15.9&new-version=0.15.10)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ty from 0.0.19 to 0.0.24
  ([`2697104`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/26971043c41c4bf45cc8ff67dafc938211305b4a))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.19 to 0.0.24. - [Release
  notes](https://github.com/astral-sh/ty/releases) -
  [Changelog](https://github.com/astral-sh/ty/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ty/compare/0.0.19...0.0.24)

--- updated-dependencies: - dependency-name: ty dependency-version: 0.0.24

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ty from 0.0.19 to 0.0.24
  ([#52](https://github.com/jakub-k-slys/substack-gateway-oss/pull/52),
  [`48f1540`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/48f15406a5952f866c00dcaa54621fbac758bbc6))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.19 to 0.0.24. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ty/releases">ty's
  releases</a>.</em></p> <blockquote> <h2>0.0.24</h2> <h2>Release Notes</h2> <p>Released on
  2026-03-19.</p> <h3>Bug fixes</h3> <ul> <li>Ensure <code>TypedDict</code> subscripts for unknown
  keys return <code>Unknown</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23926">#23926</a>)</li> <li>Fix overflow
  with recursive <code>TypeIs</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23784">#23784</a>)</li> <li>Fix variance of
  frozen dataclass-transform models (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23931">#23931</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Improve <a
  href="https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_semanticTokens">semantic
  token</a> classification for attribute access on union types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23841">#23841</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Improve performance and correctness by avoiding inferring intersection
  types for call arguments as a result of bidirectional inference (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23933">#23933</a>)</li> <li>Narrow keyword
  arguments when unpacking dictionary instances (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23436">#23436</a>)</li> <li>Discover
  <code>/usr/local/lib</code> dist-packages on Debian/Ubuntu (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23797">#23797</a>)</li> <li>Sync vendored
  typeshed stubs (<a href="https://redirect.github.com/astral-sh/ruff/pull/23963">#23963</a>). <a
  href="https://github.com/python/typeshed/compare/fa659b1def704dea3dc8e25c7857b23eac69df4d...f8f0794d0fe249c06dc9f31a004d85be6cca6ced">Typeshed
  diff</a></li> </ul> <h2>Install ty 0.0.24</h2> <h3>Install prebuilt binaries via shell script</h3>
  <pre lang="sh"><code>curl --proto '=https' --tlsv1.2 -LsSf
  https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-installer.sh | sh </code></pre>
  <h3>Install prebuilt binaries via powershell script</h3> <pre lang="sh"><code>powershell
  -ExecutionPolicy Bypass -c &quot;irm
  https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-installer.ps1 | iex&quot;
  </code></pre> <h2>Download ty 0.0.24</h2> <table> <thead> <tr> <th>File</th> <th>Platform</th>
  <th>Checksum</th> </tr> </thead> <tbody> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-aarch64-apple-darwin.tar.gz">ty-aarch64-apple-darwin.tar.gz</a></td>
  <td>Apple Silicon macOS</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-aarch64-apple-darwin.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-x86_64-apple-darwin.tar.gz">ty-x86_64-apple-darwin.tar.gz</a></td>
  <td>Intel macOS</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-x86_64-apple-darwin.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-aarch64-pc-windows-msvc.zip">ty-aarch64-pc-windows-msvc.zip</a></td>
  <td>ARM64 Windows</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-aarch64-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-i686-pc-windows-msvc.zip">ty-i686-pc-windows-msvc.zip</a></td>
  <td>x86 Windows</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-i686-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-x86_64-pc-windows-msvc.zip">ty-x86_64-pc-windows-msvc.zip</a></td>
  <td>x64 Windows</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-x86_64-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-aarch64-unknown-linux-gnu.tar.gz">ty-aarch64-unknown-linux-gnu.tar.gz</a></td>
  <td>ARM64 Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-aarch64-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-i686-unknown-linux-gnu.tar.gz">ty-i686-unknown-linux-gnu.tar.gz</a></td>
  <td>x86 Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-i686-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-powerpc64-unknown-linux-gnu.tar.gz">ty-powerpc64-unknown-linux-gnu.tar.gz</a></td>
  <td>PPC64 Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-powerpc64-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-powerpc64le-unknown-linux-gnu.tar.gz">ty-powerpc64le-unknown-linux-gnu.tar.gz</a></td>
  <td>PPC64LE Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-powerpc64le-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-s390x-unknown-linux-gnu.tar.gz">ty-s390x-unknown-linux-gnu.tar.gz</a></td>
  <td>S390x Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-s390x-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> </tbody> </table> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details>
  <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ty/blob/main/CHANGELOG.md">ty's changelog</a>.</em></p>
  <blockquote> <h2>0.0.24</h2> <p>Released on 2026-03-19.</p> <h3>Bug fixes</h3> <ul> <li>Ensure
  <code>TypedDict</code> subscripts for unknown keys return <code>Unknown</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23926">#23926</a>)</li> <li>Fix overflow
  with recursive <code>TypeIs</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23784">#23784</a>)</li> <li>Fix variance of
  frozen dataclass-transform models (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23931">#23931</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Improve <a
  href="https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_semanticTokens">semantic
  token</a> classification for attribute access on union types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23841">#23841</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Improve performance and correctness by avoiding inferring intersection
  types for call arguments as a result of bidirectional inference (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23933">#23933</a>)</li> <li>Narrow keyword
  arguments when unpacking dictionary instances (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23436">#23436</a>)</li> <li>Discover
  <code>/usr/local/lib</code> dist-packages on Debian/Ubuntu (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23797">#23797</a>)</li> <li>Sync vendored
  typeshed stubs (<a href="https://redirect.github.com/astral-sh/ruff/pull/23963">#23963</a>). <a
  href="https://github.com/python/typeshed/compare/fa659b1def704dea3dc8e25c7857b23eac69df4d...f8f0794d0fe249c06dc9f31a004d85be6cca6ced">Typeshed
  diff</a></li> </ul> <h2>Performance</h2> <ul> <li>Introduce fast path for protocol
  non-assignability (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23952">#23952</a>)</li> <li>Improved
  generic-solver performance in cases involving overload sets (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23881">#23881</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a href="https://github.com/Geo5"><code>@​Geo5</code></a></li>
  <li><a href="https://github.com/ibraheemdev"><code>@​ibraheemdev</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/dcreager"><code>@​dcreager</code></a></li> <li><a
  href="https://github.com/ollema"><code>@​ollema</code></a></li> <li><a
  href="https://github.com/sharkdp"><code>@​sharkdp</code></a></li> </ul> <h2>0.0.23</h2>
  <p>Released on 2026-03-13.</p> <h3>Bug fixes</h3> <ul> <li>Fix false-positive diagnostics for
  PEP-604 union annotations on attribute targets on Python 3.9 when <code>from __future__ import
  annotations</code> is active (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23915">#23915</a>)</li>
  <li><code>dataclass_transform</code>: Respect <code>kw_only</code> overwrites in dataclasses (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23930">#23930</a>)</li> <li>Fix
  too-many-cycle panics when inferring loop variables with <code>Literal</code> types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23875">#23875</a>)</li> </ul>
  <h3>Server</h3> <ul> <li>Fix <a
  href="https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_foldingRange">folding
  range</a> classification of lines starting with <code>#</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23831">#23831</a>)</li> <li>Fix <a
  href="https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_foldingRange">folding
  ranges</a> for notebooks (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23830">#23830</a>)</li> </ul> <!-- raw HTML
  omitted --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Commits</summary>
  <ul> <li><a
  href="https://github.com/astral-sh/ty/commit/876233049afc2530181f5b8af390c6d57c65bb80"><code>8762330</code></a>
  Bump version to 0.0.24 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3084">#3084</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/a6f24e14c0d41b17b44ea514b230a25bad411b65"><code>a6f24e1</code></a>
  Update prek dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3045">#3045</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/95150e7634e4b863223cea12e96f48baa23625d3"><code>95150e7</code></a>
  Typing FAQ: New entry explaining invariance (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3073">#3073</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/bc9e8a839385b3ee5a45d3df6e5f79885dcad17d"><code>bc9e8a8</code></a>
  Remove the repository code of conduct in favor of the organization one (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3058">#3058</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/3d12b2e9f81cd98ccc27f0285f8056da9bb999d5"><code>3d12b2e</code></a>
  Update astral-sh/setup-uv action to v7.6.0 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3054">#3054</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/64fe9c2fd1610cc6b25b1dfda0a8bb7694fc9467"><code>64fe9c2</code></a>
  Update actions/attest-build-provenance action to v4 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3046">#3046</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/86d05eb2a7da77605d42ad86a5adbde131431047"><code>86d05eb</code></a>
  Update docker/setup-buildx-action action to v4 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3050">#3050</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/eb3f320a525075daa431a0ed19d5cbff12dc5c2b"><code>eb3f320</code></a>
  Update docker/metadata-action action to v6 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3049">#3049</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/7da93b86f69724734cfa4a90d3df3ca3b44bc4e4"><code>7da93b8</code></a>
  Update docker/login-action action to v4 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3048">#3048</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/fa4db72937dacb89a6271327a7433b01322136f2"><code>fa4db72</code></a>
  Update docker/build-push-action action to v7 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3047">#3047</a>)</li> <li>Additional commits
  viewable in <a href="https://github.com/astral-sh/ty/compare/0.0.19...0.0.24">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ty&package-manager=uv&previous-version=0.0.19&new-version=0.0.24)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ty from 0.0.23 to 0.0.24
  ([`2e95fb3`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/2e95fb319697f7a87ee1096da5ada896d9df144c))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.23 to 0.0.24. - [Release
  notes](https://github.com/astral-sh/ty/releases) -
  [Changelog](https://github.com/astral-sh/ty/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ty/compare/0.0.23...0.0.24)

--- updated-dependencies: - dependency-name: ty dependency-version: 0.0.24

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ty from 0.0.23 to 0.0.24
  ([#5](https://github.com/jakub-k-slys/substack-gateway-oss/pull/5),
  [`9191920`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/919192007bb9832d1d6e97659ce28ace7979d51c))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.23 to 0.0.24. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ty/releases">ty's
  releases</a>.</em></p> <blockquote> <h2>0.0.24</h2> <h2>Release Notes</h2> <p>Released on
  2026-03-19.</p> <h3>Bug fixes</h3> <ul> <li>Ensure <code>TypedDict</code> subscripts for unknown
  keys return <code>Unknown</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23926">#23926</a>)</li> <li>Fix overflow
  with recursive <code>TypeIs</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23784">#23784</a>)</li> <li>Fix variance of
  frozen dataclass-transform models (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23931">#23931</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Improve <a
  href="https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_semanticTokens">semantic
  token</a> classification for attribute access on union types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23841">#23841</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Improve performance and correctness by avoiding inferring intersection
  types for call arguments as a result of bidirectional inference (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23933">#23933</a>)</li> <li>Narrow keyword
  arguments when unpacking dictionary instances (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23436">#23436</a>)</li> <li>Discover
  <code>/usr/local/lib</code> dist-packages on Debian/Ubuntu (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23797">#23797</a>)</li> <li>Sync vendored
  typeshed stubs (<a href="https://redirect.github.com/astral-sh/ruff/pull/23963">#23963</a>). <a
  href="https://github.com/python/typeshed/compare/fa659b1def704dea3dc8e25c7857b23eac69df4d...f8f0794d0fe249c06dc9f31a004d85be6cca6ced">Typeshed
  diff</a></li> </ul> <h2>Install ty 0.0.24</h2> <h3>Install prebuilt binaries via shell script</h3>
  <pre lang="sh"><code>curl --proto '=https' --tlsv1.2 -LsSf
  https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-installer.sh | sh </code></pre>
  <h3>Install prebuilt binaries via powershell script</h3> <pre lang="sh"><code>powershell
  -ExecutionPolicy Bypass -c &quot;irm
  https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-installer.ps1 | iex&quot;
  </code></pre> <h2>Download ty 0.0.24</h2> <table> <thead> <tr> <th>File</th> <th>Platform</th>
  <th>Checksum</th> </tr> </thead> <tbody> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-aarch64-apple-darwin.tar.gz">ty-aarch64-apple-darwin.tar.gz</a></td>
  <td>Apple Silicon macOS</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-aarch64-apple-darwin.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-x86_64-apple-darwin.tar.gz">ty-x86_64-apple-darwin.tar.gz</a></td>
  <td>Intel macOS</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-x86_64-apple-darwin.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-aarch64-pc-windows-msvc.zip">ty-aarch64-pc-windows-msvc.zip</a></td>
  <td>ARM64 Windows</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-aarch64-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-i686-pc-windows-msvc.zip">ty-i686-pc-windows-msvc.zip</a></td>
  <td>x86 Windows</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-i686-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-x86_64-pc-windows-msvc.zip">ty-x86_64-pc-windows-msvc.zip</a></td>
  <td>x64 Windows</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-x86_64-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-aarch64-unknown-linux-gnu.tar.gz">ty-aarch64-unknown-linux-gnu.tar.gz</a></td>
  <td>ARM64 Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-aarch64-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-i686-unknown-linux-gnu.tar.gz">ty-i686-unknown-linux-gnu.tar.gz</a></td>
  <td>x86 Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-i686-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-powerpc64-unknown-linux-gnu.tar.gz">ty-powerpc64-unknown-linux-gnu.tar.gz</a></td>
  <td>PPC64 Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-powerpc64-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-powerpc64le-unknown-linux-gnu.tar.gz">ty-powerpc64le-unknown-linux-gnu.tar.gz</a></td>
  <td>PPC64LE Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-powerpc64le-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-s390x-unknown-linux-gnu.tar.gz">ty-s390x-unknown-linux-gnu.tar.gz</a></td>
  <td>S390x Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.24/ty-s390x-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> </tbody> </table> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details>
  <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ty/blob/main/CHANGELOG.md">ty's changelog</a>.</em></p>
  <blockquote> <h2>0.0.24</h2> <p>Released on 2026-03-19.</p> <h3>Bug fixes</h3> <ul> <li>Ensure
  <code>TypedDict</code> subscripts for unknown keys return <code>Unknown</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23926">#23926</a>)</li> <li>Fix overflow
  with recursive <code>TypeIs</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23784">#23784</a>)</li> <li>Fix variance of
  frozen dataclass-transform models (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23931">#23931</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Improve <a
  href="https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#textDocument_semanticTokens">semantic
  token</a> classification for attribute access on union types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23841">#23841</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Improve performance and correctness by avoiding inferring intersection
  types for call arguments as a result of bidirectional inference (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23933">#23933</a>)</li> <li>Narrow keyword
  arguments when unpacking dictionary instances (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23436">#23436</a>)</li> <li>Discover
  <code>/usr/local/lib</code> dist-packages on Debian/Ubuntu (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23797">#23797</a>)</li> <li>Sync vendored
  typeshed stubs (<a href="https://redirect.github.com/astral-sh/ruff/pull/23963">#23963</a>). <a
  href="https://github.com/python/typeshed/compare/fa659b1def704dea3dc8e25c7857b23eac69df4d...f8f0794d0fe249c06dc9f31a004d85be6cca6ced">Typeshed
  diff</a></li> </ul> <h2>Performance</h2> <ul> <li>Introduce fast path for protocol
  non-assignability (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23952">#23952</a>)</li> <li>Improved
  generic-solver performance in cases involving overload sets (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23881">#23881</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a href="https://github.com/Geo5"><code>@​Geo5</code></a></li>
  <li><a href="https://github.com/ibraheemdev"><code>@​ibraheemdev</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/dcreager"><code>@​dcreager</code></a></li> <li><a
  href="https://github.com/ollema"><code>@​ollema</code></a></li> <li><a
  href="https://github.com/sharkdp"><code>@​sharkdp</code></a></li> </ul> </blockquote> </details>
  <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ty/commit/876233049afc2530181f5b8af390c6d57c65bb80"><code>8762330</code></a>
  Bump version to 0.0.24 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3084">#3084</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/a6f24e14c0d41b17b44ea514b230a25bad411b65"><code>a6f24e1</code></a>
  Update prek dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3045">#3045</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/95150e7634e4b863223cea12e96f48baa23625d3"><code>95150e7</code></a>
  Typing FAQ: New entry explaining invariance (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3073">#3073</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/bc9e8a839385b3ee5a45d3df6e5f79885dcad17d"><code>bc9e8a8</code></a>
  Remove the repository code of conduct in favor of the organization one (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3058">#3058</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/3d12b2e9f81cd98ccc27f0285f8056da9bb999d5"><code>3d12b2e</code></a>
  Update astral-sh/setup-uv action to v7.6.0 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3054">#3054</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/64fe9c2fd1610cc6b25b1dfda0a8bb7694fc9467"><code>64fe9c2</code></a>
  Update actions/attest-build-provenance action to v4 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3046">#3046</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/86d05eb2a7da77605d42ad86a5adbde131431047"><code>86d05eb</code></a>
  Update docker/setup-buildx-action action to v4 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3050">#3050</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/eb3f320a525075daa431a0ed19d5cbff12dc5c2b"><code>eb3f320</code></a>
  Update docker/metadata-action action to v6 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3049">#3049</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/7da93b86f69724734cfa4a90d3df3ca3b44bc4e4"><code>7da93b8</code></a>
  Update docker/login-action action to v4 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3048">#3048</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/fa4db72937dacb89a6271327a7433b01322136f2"><code>fa4db72</code></a>
  Update docker/build-push-action action to v7 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3047">#3047</a>)</li> <li>Additional commits
  viewable in <a href="https://github.com/astral-sh/ty/compare/0.0.23...0.0.24">compare
  view</a></li> </ul> </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ty&package-manager=uv&previous-version=0.0.23&new-version=0.0.24)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ty from 0.0.24 to 0.0.25
  ([`f4c67dc`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/f4c67dc5257f76659862c4d03e44640b0048fa3a))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.24 to 0.0.25. - [Release
  notes](https://github.com/astral-sh/ty/releases) -
  [Changelog](https://github.com/astral-sh/ty/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ty/compare/0.0.24...0.0.25)

--- updated-dependencies: - dependency-name: ty dependency-version: 0.0.25

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ty from 0.0.24 to 0.0.25
  ([`25c93aa`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/25c93aabb7a647cc23365fd4a4a92c013bef3dec))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.24 to 0.0.25. - [Release
  notes](https://github.com/astral-sh/ty/releases) -
  [Changelog](https://github.com/astral-sh/ty/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ty/compare/0.0.24...0.0.25)

--- updated-dependencies: - dependency-name: ty dependency-version: 0.0.25

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ty from 0.0.24 to 0.0.25
  ([#53](https://github.com/jakub-k-slys/substack-gateway-oss/pull/53),
  [`55b5910`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/55b5910e7d1060fd6437a7d0b6053aa7d2d6e55a))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.24 to 0.0.25. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ty/releases">ty's
  releases</a>.</em></p> <blockquote> <h2>0.0.25</h2> <h2>Release Notes</h2> <p>Released on
  2026-03-24.</p> <h3>Breaking changes</h3> <ul> <li>Support <code>type:ignore[ty:code]</code>
  suppressions (<a href="https://redirect.github.com/astral-sh/ruff/pull/24096">#24096</a>)</li>
  </ul> <h3>Bug fixes</h3> <ul> <li>Avoid eager TypedDict diagnostics in <code>TypedDict |
  dict</code> unions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24151">#24151</a>)</li> <li>Fix Salsa panic
  propagation (<a href="https://redirect.github.com/astral-sh/ruff/pull/24141">#24141</a>)</li>
  <li>Fix folding ranges of comments separated by statements (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24132">#24132</a>)</li> <li>Fix loop-header
  reachability cycles in conditional unpacking (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24006">#24006</a>)</li> <li>Fix subtyping of
  intersections containing <code>NewType</code>s of unions vs. unions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24087">#24087</a>)</li> <li>Fix untracked
  reads in Salsa queries that can lead to backdating panics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24051">#24051</a>)</li> <li>Prevent tainted
  loop bindings in cycle normalization (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24143">#24143</a>)</li> <li>Simplify an
  intersection of <code>N &amp; ~T</code> to <code>Never</code> if <code>B &amp; ~T</code> would
  simplify to <code>Never</code>, where <code>B</code> is the concrete base type of a
  <code>NewType</code> <code>N</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24086">#24086</a>)</li> </ul> <h3>LSP</h3>
  <ul> <li>Preserve blank lines between comments and imports in add-import action (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24066">#24066</a>)</li> </ul> <h3>Type
  checking</h3> <ul> <li>Add diagnostic hint for invalid assignments involving invariant generics
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24032">#24032</a>)</li> <li>Add
  precisely-typed overloads for <code>TypedDict</code> update (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24101">#24101</a>)</li> <li>Disallow
  read-only fields in <code>TypedDict</code> updates (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24128">#24128</a>)</li> <li>Expand bounded
  typevars to their upper bounds when evaluating truthiness comparisons between intersections and
  literal types (<a href="https://redirect.github.com/astral-sh/ruff/pull/24082">#24082</a>)</li>
  <li>Emit <code>reveal_type</code> diagnostics in unreachable code (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24070">#24070</a>)</li> <li>Improve
  <code>isinstance()</code> reachability analysis (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24077">#24077</a>)</li> <li>Improve keyword
  argument narrowing for nested dictionaries (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24010">#24010</a>)</li> <li>Infer
  <code>yield</code> expression types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23796">#23796</a>)</li> <li>Reduce
  diagnostic range for <code>invalid-metaclass</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24145">#24145</a>)</li> <li>Support
  narrowing for extended walrus targets (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24129">#24129</a>)</li>
  <li>Unions/intersections of gradual types should be assignable to <code>Never</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24056">#24056</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> <li><a
  href="https://github.com/Glyphack"><code>@​Glyphack</code></a></li> <li><a
  href="https://github.com/sharkdp"><code>@​sharkdp</code></a></li> <li><a
  href="https://github.com/ibraheemdev"><code>@​ibraheemdev</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/mvanhorn"><code>@​mvanhorn</code></a></li> <li><a
  href="https://github.com/carljm"><code>@​carljm</code></a></li> </ul> <h2>Install ty 0.0.25</h2>
  <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details> <details>
  <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ty/blob/main/CHANGELOG.md">ty's changelog</a>.</em></p>
  <blockquote> <h2>0.0.25</h2> <p>Released on 2026-03-24.</p> <h3>Breaking changes</h3> <ul>
  <li>Support <code>type:ignore[ty:code]</code> suppressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24096">#24096</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>Avoid eager TypedDict diagnostics in <code>TypedDict | dict</code> unions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24151">#24151</a>)</li> <li>Fix Salsa panic
  propagation (<a href="https://redirect.github.com/astral-sh/ruff/pull/24141">#24141</a>)</li>
  <li>Fix folding ranges of comments separated by statements (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24132">#24132</a>)</li> <li>Fix loop-header
  reachability cycles in conditional unpacking (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24006">#24006</a>)</li> <li>Fix subtyping of
  intersections containing <code>NewType</code>s of unions vs. unions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24087">#24087</a>)</li> <li>Fix untracked
  reads in Salsa queries that can lead to backdating panics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24051">#24051</a>)</li> <li>Prevent tainted
  loop bindings in cycle normalization (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24143">#24143</a>)</li> <li>Simplify an
  intersection of <code>N &amp; ~T</code> to <code>Never</code> if <code>B &amp; ~T</code> would
  simplify to <code>Never</code>, where <code>B</code> is the concrete base type of a
  <code>NewType</code> <code>N</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24086">#24086</a>)</li> </ul> <h3>LSP</h3>
  <ul> <li>Preserve blank lines between comments and imports in add-import action (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24066">#24066</a>)</li> </ul> <h3>Type
  checking</h3> <ul> <li>Add diagnostic hint for invalid assignments involving invariant generics
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24032">#24032</a>)</li> <li>Add
  precisely-typed overloads for <code>TypedDict</code> update (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24101">#24101</a>)</li> <li>Disallow
  read-only fields in <code>TypedDict</code> updates (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24128">#24128</a>)</li> <li>Expand bounded
  typevars to their upper bounds when evaluating truthiness comparisons between intersections and
  literal types (<a href="https://redirect.github.com/astral-sh/ruff/pull/24082">#24082</a>)</li>
  <li>Emit <code>reveal_type</code> diagnostics in unreachable code (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24070">#24070</a>)</li> <li>Improve
  <code>isinstance()</code> reachability analysis (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24077">#24077</a>)</li> <li>Improve keyword
  argument narrowing for nested dictionaries (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24010">#24010</a>)</li> <li>Infer
  <code>yield</code> expression types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23796">#23796</a>)</li> <li>Reduce
  diagnostic range for <code>invalid-metaclass</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24145">#24145</a>)</li> <li>Support
  narrowing for extended walrus targets (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24129">#24129</a>)</li>
  <li>Unions/intersections of gradual types should be assignable to <code>Never</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24056">#24056</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> <li><a
  href="https://github.com/Glyphack"><code>@​Glyphack</code></a></li> <li><a
  href="https://github.com/sharkdp"><code>@​sharkdp</code></a></li> <li><a
  href="https://github.com/ibraheemdev"><code>@​ibraheemdev</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/mvanhorn"><code>@​mvanhorn</code></a></li> <li><a
  href="https://github.com/carljm"><code>@​carljm</code></a></li> </ul> </blockquote> </details>
  <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ty/commit/d60899a14f6fe368e477c17f4205483aebdf84a8"><code>d60899a</code></a>
  Bump version to 0.0.25 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3125">#3125</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/db65b3e118a705be2694032fd2df613ea11565f1"><code>db65b3e</code></a>
  Update documentation to reflect <code>type:ignore</code> changes (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3121">#3121</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/9e464322e6a00a651861ec63af09f4e82fc903be"><code>9e46432</code></a>
  Use ty in Emacs with Eglot (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3107">#3107</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/1f30d7c82c0ce9d99533cd5924180a4365941c06"><code>1f30d7c</code></a>
  Update artifact github actions dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3113">#3113</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/255ef63825d35fb03f2755f05f2fd66b96a2c873"><code>255ef63</code></a>
  Revert &quot;Update Artifact GitHub Actions dependencies&quot; (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3112">#3112</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/5fe54ca92587d69ac83fc5614b4e9566f692ae34"><code>5fe54ca</code></a>
  Update Artifact GitHub Actions dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3108">#3108</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/a0cf1e7f3cacec90225b6b99d239ca43739d2800"><code>a0cf1e7</code></a>
  Update Swatinem/rust-cache action to v2.9.1 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3110">#3110</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/fd2acb44500fb65fa33e1e6b6c27daeaed382467"><code>fd2acb4</code></a>
  Update prek dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3109">#3109</a>)</li> <li>See full diff in
  <a href="https://github.com/astral-sh/ty/compare/0.0.24...0.0.25">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ty&package-manager=uv&previous-version=0.0.24&new-version=0.0.25)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ty from 0.0.24 to 0.0.25
  ([#6](https://github.com/jakub-k-slys/substack-gateway-oss/pull/6),
  [`0772e21`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/0772e219caf3bfec9ca9c3053f75a3de0a61fa50))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.24 to 0.0.25. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ty/releases">ty's
  releases</a>.</em></p> <blockquote> <h2>0.0.25</h2> <h2>Release Notes</h2> <p>Released on
  2026-03-24.</p> <h3>Breaking changes</h3> <ul> <li>Support <code>type:ignore[ty:code]</code>
  suppressions (<a href="https://redirect.github.com/astral-sh/ruff/pull/24096">#24096</a>)</li>
  </ul> <h3>Bug fixes</h3> <ul> <li>Avoid eager TypedDict diagnostics in <code>TypedDict |
  dict</code> unions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24151">#24151</a>)</li> <li>Fix Salsa panic
  propagation (<a href="https://redirect.github.com/astral-sh/ruff/pull/24141">#24141</a>)</li>
  <li>Fix folding ranges of comments separated by statements (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24132">#24132</a>)</li> <li>Fix loop-header
  reachability cycles in conditional unpacking (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24006">#24006</a>)</li> <li>Fix subtyping of
  intersections containing <code>NewType</code>s of unions vs. unions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24087">#24087</a>)</li> <li>Fix untracked
  reads in Salsa queries that can lead to backdating panics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24051">#24051</a>)</li> <li>Prevent tainted
  loop bindings in cycle normalization (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24143">#24143</a>)</li> <li>Simplify an
  intersection of <code>N &amp; ~T</code> to <code>Never</code> if <code>B &amp; ~T</code> would
  simplify to <code>Never</code>, where <code>B</code> is the concrete base type of a
  <code>NewType</code> <code>N</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24086">#24086</a>)</li> </ul> <h3>LSP</h3>
  <ul> <li>Preserve blank lines between comments and imports in add-import action (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24066">#24066</a>)</li> </ul> <h3>Type
  checking</h3> <ul> <li>Add diagnostic hint for invalid assignments involving invariant generics
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24032">#24032</a>)</li> <li>Add
  precisely-typed overloads for <code>TypedDict</code> update (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24101">#24101</a>)</li> <li>Disallow
  read-only fields in <code>TypedDict</code> updates (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24128">#24128</a>)</li> <li>Expand bounded
  typevars to their upper bounds when evaluating truthiness comparisons between intersections and
  literal types (<a href="https://redirect.github.com/astral-sh/ruff/pull/24082">#24082</a>)</li>
  <li>Emit <code>reveal_type</code> diagnostics in unreachable code (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24070">#24070</a>)</li> <li>Improve
  <code>isinstance()</code> reachability analysis (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24077">#24077</a>)</li> <li>Improve keyword
  argument narrowing for nested dictionaries (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24010">#24010</a>)</li> <li>Infer
  <code>yield</code> expression types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23796">#23796</a>)</li> <li>Reduce
  diagnostic range for <code>invalid-metaclass</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24145">#24145</a>)</li> <li>Support
  narrowing for extended walrus targets (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24129">#24129</a>)</li>
  <li>Unions/intersections of gradual types should be assignable to <code>Never</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24056">#24056</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> <li><a
  href="https://github.com/Glyphack"><code>@​Glyphack</code></a></li> <li><a
  href="https://github.com/sharkdp"><code>@​sharkdp</code></a></li> <li><a
  href="https://github.com/ibraheemdev"><code>@​ibraheemdev</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/mvanhorn"><code>@​mvanhorn</code></a></li> <li><a
  href="https://github.com/carljm"><code>@​carljm</code></a></li> </ul> <h2>Install ty 0.0.25</h2>
  <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details> <details>
  <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ty/blob/main/CHANGELOG.md">ty's changelog</a>.</em></p>
  <blockquote> <h2>0.0.25</h2> <p>Released on 2026-03-24.</p> <h3>Breaking changes</h3> <ul>
  <li>Support <code>type:ignore[ty:code]</code> suppressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24096">#24096</a>)</li> </ul> <h3>Bug
  fixes</h3> <ul> <li>Avoid eager TypedDict diagnostics in <code>TypedDict | dict</code> unions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24151">#24151</a>)</li> <li>Fix Salsa panic
  propagation (<a href="https://redirect.github.com/astral-sh/ruff/pull/24141">#24141</a>)</li>
  <li>Fix folding ranges of comments separated by statements (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24132">#24132</a>)</li> <li>Fix loop-header
  reachability cycles in conditional unpacking (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24006">#24006</a>)</li> <li>Fix subtyping of
  intersections containing <code>NewType</code>s of unions vs. unions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24087">#24087</a>)</li> <li>Fix untracked
  reads in Salsa queries that can lead to backdating panics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24051">#24051</a>)</li> <li>Prevent tainted
  loop bindings in cycle normalization (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24143">#24143</a>)</li> <li>Simplify an
  intersection of <code>N &amp; ~T</code> to <code>Never</code> if <code>B &amp; ~T</code> would
  simplify to <code>Never</code>, where <code>B</code> is the concrete base type of a
  <code>NewType</code> <code>N</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24086">#24086</a>)</li> </ul> <h3>LSP</h3>
  <ul> <li>Preserve blank lines between comments and imports in add-import action (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24066">#24066</a>)</li> </ul> <h3>Type
  checking</h3> <ul> <li>Add diagnostic hint for invalid assignments involving invariant generics
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24032">#24032</a>)</li> <li>Add
  precisely-typed overloads for <code>TypedDict</code> update (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24101">#24101</a>)</li> <li>Disallow
  read-only fields in <code>TypedDict</code> updates (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24128">#24128</a>)</li> <li>Expand bounded
  typevars to their upper bounds when evaluating truthiness comparisons between intersections and
  literal types (<a href="https://redirect.github.com/astral-sh/ruff/pull/24082">#24082</a>)</li>
  <li>Emit <code>reveal_type</code> diagnostics in unreachable code (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24070">#24070</a>)</li> <li>Improve
  <code>isinstance()</code> reachability analysis (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24077">#24077</a>)</li> <li>Improve keyword
  argument narrowing for nested dictionaries (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24010">#24010</a>)</li> <li>Infer
  <code>yield</code> expression types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23796">#23796</a>)</li> <li>Reduce
  diagnostic range for <code>invalid-metaclass</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24145">#24145</a>)</li> <li>Support
  narrowing for extended walrus targets (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24129">#24129</a>)</li>
  <li>Unions/intersections of gradual types should be assignable to <code>Never</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24056">#24056</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> <li><a
  href="https://github.com/Glyphack"><code>@​Glyphack</code></a></li> <li><a
  href="https://github.com/sharkdp"><code>@​sharkdp</code></a></li> <li><a
  href="https://github.com/ibraheemdev"><code>@​ibraheemdev</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/mvanhorn"><code>@​mvanhorn</code></a></li> <li><a
  href="https://github.com/carljm"><code>@​carljm</code></a></li> </ul> </blockquote> </details>
  <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ty/commit/d60899a14f6fe368e477c17f4205483aebdf84a8"><code>d60899a</code></a>
  Bump version to 0.0.25 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3125">#3125</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/db65b3e118a705be2694032fd2df613ea11565f1"><code>db65b3e</code></a>
  Update documentation to reflect <code>type:ignore</code> changes (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3121">#3121</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/9e464322e6a00a651861ec63af09f4e82fc903be"><code>9e46432</code></a>
  Use ty in Emacs with Eglot (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3107">#3107</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/1f30d7c82c0ce9d99533cd5924180a4365941c06"><code>1f30d7c</code></a>
  Update artifact github actions dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3113">#3113</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/255ef63825d35fb03f2755f05f2fd66b96a2c873"><code>255ef63</code></a>
  Revert &quot;Update Artifact GitHub Actions dependencies&quot; (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3112">#3112</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/5fe54ca92587d69ac83fc5614b4e9566f692ae34"><code>5fe54ca</code></a>
  Update Artifact GitHub Actions dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3108">#3108</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/a0cf1e7f3cacec90225b6b99d239ca43739d2800"><code>a0cf1e7</code></a>
  Update Swatinem/rust-cache action to v2.9.1 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3110">#3110</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/fd2acb44500fb65fa33e1e6b6c27daeaed382467"><code>fd2acb4</code></a>
  Update prek dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3109">#3109</a>)</li> <li>See full diff in
  <a href="https://github.com/astral-sh/ty/compare/0.0.24...0.0.25">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ty&package-manager=uv&previous-version=0.0.24&new-version=0.0.25)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ty from 0.0.25 to 0.0.27
  ([`b8b700e`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/b8b700ebd08701e9f68d9f499bad2969cbe76932))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.25 to 0.0.27. - [Release
  notes](https://github.com/astral-sh/ty/releases) -
  [Changelog](https://github.com/astral-sh/ty/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ty/compare/0.0.25...0.0.27)

--- updated-dependencies: - dependency-name: ty dependency-version: 0.0.27

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ty from 0.0.25 to 0.0.27
  ([`6fcd47d`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/6fcd47de292efb989a5d3df77a940649d97fd83a))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.25 to 0.0.27. - [Release
  notes](https://github.com/astral-sh/ty/releases) -
  [Changelog](https://github.com/astral-sh/ty/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ty/compare/0.0.25...0.0.27)

--- updated-dependencies: - dependency-name: ty dependency-version: 0.0.27

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ty from 0.0.25 to 0.0.27
  ([#11](https://github.com/jakub-k-slys/substack-gateway-oss/pull/11),
  [`e0b79ed`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e0b79ed5f9bbc328c100a35a935d639c41f939e2))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.25 to 0.0.27. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ty/releases">ty's
  releases</a>.</em></p> <blockquote> <h2>0.0.27</h2> <h2>Release Notes</h2> <p>Released on
  2026-03-31.</p> <h3>Bug fixes</h3> <ul> <li>Fix panic on debug builds when attempting to provide
  autocomplete suggestions for <code>list[int]&lt;CURSOR&gt;()</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24167">#24167</a>)</li> <li>Fix
  instance-attribute lookup in methods of protocol classes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24213">#24213</a>)</li> <li>Fix nested
  global and nonlocal lookups through forwarding scopes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24279">#24279</a>)</li> <li>Fix panic on
  <code>list[Annotated[()]]</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24303">#24303</a>)</li> <li>Fix stack
  overflow on <code>type A = TypeIs[Callable[[], A]]</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24245">#24245</a>)</li> <li>Use
  <code>_cls</code> as the name of the first argument for synthesized
  <code>collections.namedtuple</code> constructor methods (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24333">#24333</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Fix semantic token classification for properties accessed on instances (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24065">#24065</a>)</li> <li>Grey out unused
  bindings in the editor (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23305">#23305</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Add bidirectional type context for TypedDict <code>get()</code> defaults
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24231">#24231</a>)</li> <li>Add
  bidirectional type context for TypedDict <code>pop()</code> defaults (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24229">#24229</a>)</li> <li>Add support for
  functional TypedDict (<a href="https://redirect.github.com/astral-sh/ruff/pull/24174">#24174</a>,
  <a href="https://redirect.github.com/astral-sh/ruff/pull/24331">#24331</a>, <a
  href="https://redirect.github.com/astral-sh/ruff/pull/24295">#24295</a>)</li> <li>Ban type
  qualifiers in PEP-695 type aliases (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24242">#24242</a>)</li> <li>Enforce
  <code>Final</code> attribute assignment rules for annotated and augmented writes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23880">#23880</a>)</li> <li>Improve support
  for <code>Callable</code> type context (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23888">#23888</a>)</li> <li>Infer lambda
  expressions with <code>Callable</code> type context (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/22633">#22633</a>)</li> <li>Don't
  incorrectly infer the type of a method as being a singleton type when it's accessed off an
  instance (<a href="https://redirect.github.com/astral-sh/ruff/pull/24039">#24039</a>)</li>
  <li>Propagate type context through <code>await</code> expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24256">#24256</a>)</li> <li>Resolve
  union-likes in emitting union attribute errors (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24263">#24263</a>)</li> <li>Show the user
  where the variable was declared as <code>Final</code> when emitting a diagnostic about a
  <code>Final</code> variable being reassigned (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24194">#24194</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a href="https://github.com/carljm"><code>@​carljm</code></a></li>
  <li><a href="https://github.com/mvanhorn"><code>@​mvanhorn</code></a></li> <li><a
  href="https://github.com/oconnor663"><code>@​oconnor663</code></a></li> <li><a
  href="https://github.com/ibraheemdev"><code>@​ibraheemdev</code></a></li> <li><a
  href="https://github.com/zanieb"><code>@​zanieb</code></a></li> <li><a
  href="https://github.com/denyszhak"><code>@​denyszhak</code></a></li> <li><a
  href="https://github.com/Glyphack"><code>@​Glyphack</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> </ul> <h2>Install ty
  0.0.27</h2> <h3>Install prebuilt binaries via shell script</h3> <pre
  lang="sh"><code>&lt;/tr&gt;&lt;/table&gt; </code></pre> </blockquote> <p>... (truncated)</p>
  </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ty/blob/main/CHANGELOG.md">ty's changelog</a>.</em></p>
  <blockquote> <h2>0.0.27</h2> <p>Released on 2026-03-31.</p> <h3>Bug fixes</h3> <ul> <li>Fix panic
  on debug builds when attempting to provide autocomplete suggestions for
  <code>list[int]&lt;CURSOR&gt;()</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24167">#24167</a>)</li> <li>Fix
  instance-attribute lookup in methods of protocol classes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24213">#24213</a>)</li> <li>Fix nested
  global and nonlocal lookups through forwarding scopes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24279">#24279</a>)</li> <li>Fix panic on
  <code>list[Annotated[()]]</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24303">#24303</a>)</li> <li>Fix stack
  overflow on <code>type A = TypeIs[Callable[[], A]]</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24245">#24245</a>)</li> <li>Use
  <code>_cls</code> as the name of the first argument for synthesized
  <code>collections.namedtuple</code> constructor methods (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24333">#24333</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Fix semantic token classification for properties accessed on instances (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24065">#24065</a>)</li> <li>Grey out unused
  bindings in the editor (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23305">#23305</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Add bidirectional type context for TypedDict <code>get()</code> defaults
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24231">#24231</a>)</li> <li>Add
  bidirectional type context for TypedDict <code>pop()</code> defaults (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24229">#24229</a>)</li> <li>Add support for
  functional TypedDict (<a href="https://redirect.github.com/astral-sh/ruff/pull/24174">#24174</a>,
  <a href="https://redirect.github.com/astral-sh/ruff/pull/24331">#24331</a>, <a
  href="https://redirect.github.com/astral-sh/ruff/pull/24295">#24295</a>)</li> <li>Ban type
  qualifiers in PEP-695 type aliases (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24242">#24242</a>)</li> <li>Enforce
  <code>Final</code> attribute assignment rules for annotated and augmented writes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23880">#23880</a>)</li> <li>Improve support
  for <code>Callable</code> type context (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23888">#23888</a>)</li> <li>Infer lambda
  expressions with <code>Callable</code> type context (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/22633">#22633</a>)</li> <li>Don't
  incorrectly infer the type of a method as being a singleton type when it's accessed off an
  instance (<a href="https://redirect.github.com/astral-sh/ruff/pull/24039">#24039</a>)</li>
  <li>Propagate type context through <code>await</code> expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24256">#24256</a>)</li> <li>Resolve
  union-likes in emitting union attribute errors (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24263">#24263</a>)</li> <li>Show the user
  where the variable was declared as <code>Final</code> when emitting a diagnostic about a
  <code>Final</code> variable being reassigned (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24194">#24194</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a href="https://github.com/carljm"><code>@​carljm</code></a></li>
  <li><a href="https://github.com/mvanhorn"><code>@​mvanhorn</code></a></li> <li><a
  href="https://github.com/oconnor663"><code>@​oconnor663</code></a></li> <li><a
  href="https://github.com/ibraheemdev"><code>@​ibraheemdev</code></a></li> <li><a
  href="https://github.com/zanieb"><code>@​zanieb</code></a></li> <li><a
  href="https://github.com/denyszhak"><code>@​denyszhak</code></a></li> <li><a
  href="https://github.com/Glyphack"><code>@​Glyphack</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> </ul> <h2>0.0.26</h2>
  <p>Released on 2026-03-26.</p> <h3>Bug fixes</h3> <!-- raw HTML omitted --> </blockquote> <p>...
  (truncated)</p> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ty/commit/5c9e342c2ea67a0ac8749d32296dd3071974927a"><code>5c9e342</code></a>
  Bump version to 0.0.27 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3185">#3185</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/e6a57315251f37ab3516cb614f891ece91595393"><code>e6a5731</code></a>
  Update actions/cache action to v5.0.4 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3172">#3172</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/c47b982b86bb599d016af1d235174391f618ff16"><code>c47b982</code></a>
  Update prek dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3173">#3173</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/657abcfc82221440481f9c9b76c6b6a3b89d5d00"><code>657abcf</code></a>
  Update astral-sh/setup-uv action to v8 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3174">#3174</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/9e582cb48e9c2306073091d554c04853091d612b"><code>9e582cb</code></a>
  Fetch the cargo-dist binary directly instead of using the installer (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3160">#3160</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/d5c51ea65be68cffcfa1afe204e5f6003fc06b02"><code>d5c51ea</code></a>
  docs: use content tabs (<a

href="https://redirect.github.com/astral-sh/ty/issues/3146">#3146</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/9893776cbd744bec84a43463728ab3813b00968f"><code>9893776</code></a>
  Use the <code>release</code> environment in <code>publish-docs</code> (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3147">#3147</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/94030512727f4320e8184f120c4330ed8f42ec6f"><code>9403051</code></a>
  Bump version to 0.0.26 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3145">#3145</a>)</li> <li>See full diff in
  <a href="https://github.com/astral-sh/ty/compare/0.0.25...0.0.27">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ty&package-manager=uv&previous-version=0.0.25&new-version=0.0.27)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ty from 0.0.25 to 0.0.27
  ([#57](https://github.com/jakub-k-slys/substack-gateway-oss/pull/57),
  [`937fd99`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/937fd99f6f0f46a735c1e9b24601dad4a228a6cf))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.25 to 0.0.27. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ty/releases">ty's
  releases</a>.</em></p> <blockquote> <h2>0.0.27</h2> <h2>Release Notes</h2> <p>Released on
  2026-03-31.</p> <h3>Bug fixes</h3> <ul> <li>Fix panic on debug builds when attempting to provide
  autocomplete suggestions for <code>list[int]&lt;CURSOR&gt;()</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24167">#24167</a>)</li> <li>Fix
  instance-attribute lookup in methods of protocol classes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24213">#24213</a>)</li> <li>Fix nested
  global and nonlocal lookups through forwarding scopes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24279">#24279</a>)</li> <li>Fix panic on
  <code>list[Annotated[()]]</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24303">#24303</a>)</li> <li>Fix stack
  overflow on <code>type A = TypeIs[Callable[[], A]]</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24245">#24245</a>)</li> <li>Use
  <code>_cls</code> as the name of the first argument for synthesized
  <code>collections.namedtuple</code> constructor methods (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24333">#24333</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Fix semantic token classification for properties accessed on instances (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24065">#24065</a>)</li> <li>Grey out unused
  bindings in the editor (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23305">#23305</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Add bidirectional type context for TypedDict <code>get()</code> defaults
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24231">#24231</a>)</li> <li>Add
  bidirectional type context for TypedDict <code>pop()</code> defaults (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24229">#24229</a>)</li> <li>Add support for
  functional TypedDict (<a href="https://redirect.github.com/astral-sh/ruff/pull/24174">#24174</a>,
  <a href="https://redirect.github.com/astral-sh/ruff/pull/24331">#24331</a>, <a
  href="https://redirect.github.com/astral-sh/ruff/pull/24295">#24295</a>)</li> <li>Ban type
  qualifiers in PEP-695 type aliases (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24242">#24242</a>)</li> <li>Enforce
  <code>Final</code> attribute assignment rules for annotated and augmented writes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23880">#23880</a>)</li> <li>Improve support
  for <code>Callable</code> type context (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23888">#23888</a>)</li> <li>Infer lambda
  expressions with <code>Callable</code> type context (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/22633">#22633</a>)</li> <li>Don't
  incorrectly infer the type of a method as being a singleton type when it's accessed off an
  instance (<a href="https://redirect.github.com/astral-sh/ruff/pull/24039">#24039</a>)</li>
  <li>Propagate type context through <code>await</code> expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24256">#24256</a>)</li> <li>Resolve
  union-likes in emitting union attribute errors (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24263">#24263</a>)</li> <li>Show the user
  where the variable was declared as <code>Final</code> when emitting a diagnostic about a
  <code>Final</code> variable being reassigned (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24194">#24194</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a href="https://github.com/carljm"><code>@​carljm</code></a></li>
  <li><a href="https://github.com/mvanhorn"><code>@​mvanhorn</code></a></li> <li><a
  href="https://github.com/oconnor663"><code>@​oconnor663</code></a></li> <li><a
  href="https://github.com/ibraheemdev"><code>@​ibraheemdev</code></a></li> <li><a
  href="https://github.com/zanieb"><code>@​zanieb</code></a></li> <li><a
  href="https://github.com/denyszhak"><code>@​denyszhak</code></a></li> <li><a
  href="https://github.com/Glyphack"><code>@​Glyphack</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> </ul> <h2>Install ty
  0.0.27</h2> <h3>Install prebuilt binaries via shell script</h3> <pre
  lang="sh"><code>&lt;/tr&gt;&lt;/table&gt; </code></pre> </blockquote> <p>... (truncated)</p>
  </details> <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ty/blob/main/CHANGELOG.md">ty's changelog</a>.</em></p>
  <blockquote> <h2>0.0.27</h2> <p>Released on 2026-03-31.</p> <h3>Bug fixes</h3> <ul> <li>Fix panic
  on debug builds when attempting to provide autocomplete suggestions for
  <code>list[int]&lt;CURSOR&gt;()</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24167">#24167</a>)</li> <li>Fix
  instance-attribute lookup in methods of protocol classes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24213">#24213</a>)</li> <li>Fix nested
  global and nonlocal lookups through forwarding scopes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24279">#24279</a>)</li> <li>Fix panic on
  <code>list[Annotated[()]]</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24303">#24303</a>)</li> <li>Fix stack
  overflow on <code>type A = TypeIs[Callable[[], A]]</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24245">#24245</a>)</li> <li>Use
  <code>_cls</code> as the name of the first argument for synthesized
  <code>collections.namedtuple</code> constructor methods (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24333">#24333</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Fix semantic token classification for properties accessed on instances (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24065">#24065</a>)</li> <li>Grey out unused
  bindings in the editor (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23305">#23305</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Add bidirectional type context for TypedDict <code>get()</code> defaults
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24231">#24231</a>)</li> <li>Add
  bidirectional type context for TypedDict <code>pop()</code> defaults (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24229">#24229</a>)</li> <li>Add support for
  functional TypedDict (<a href="https://redirect.github.com/astral-sh/ruff/pull/24174">#24174</a>,
  <a href="https://redirect.github.com/astral-sh/ruff/pull/24331">#24331</a>, <a
  href="https://redirect.github.com/astral-sh/ruff/pull/24295">#24295</a>)</li> <li>Ban type
  qualifiers in PEP-695 type aliases (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24242">#24242</a>)</li> <li>Enforce
  <code>Final</code> attribute assignment rules for annotated and augmented writes (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23880">#23880</a>)</li> <li>Improve support
  for <code>Callable</code> type context (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23888">#23888</a>)</li> <li>Infer lambda
  expressions with <code>Callable</code> type context (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/22633">#22633</a>)</li> <li>Don't
  incorrectly infer the type of a method as being a singleton type when it's accessed off an
  instance (<a href="https://redirect.github.com/astral-sh/ruff/pull/24039">#24039</a>)</li>
  <li>Propagate type context through <code>await</code> expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24256">#24256</a>)</li> <li>Resolve
  union-likes in emitting union attribute errors (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24263">#24263</a>)</li> <li>Show the user
  where the variable was declared as <code>Final</code> when emitting a diagnostic about a
  <code>Final</code> variable being reassigned (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24194">#24194</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a href="https://github.com/carljm"><code>@​carljm</code></a></li>
  <li><a href="https://github.com/mvanhorn"><code>@​mvanhorn</code></a></li> <li><a
  href="https://github.com/oconnor663"><code>@​oconnor663</code></a></li> <li><a
  href="https://github.com/ibraheemdev"><code>@​ibraheemdev</code></a></li> <li><a
  href="https://github.com/zanieb"><code>@​zanieb</code></a></li> <li><a
  href="https://github.com/denyszhak"><code>@​denyszhak</code></a></li> <li><a
  href="https://github.com/Glyphack"><code>@​Glyphack</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li> </ul> <h2>0.0.26</h2>
  <p>Released on 2026-03-26.</p> <h3>Bug fixes</h3> <!-- raw HTML omitted --> </blockquote> <p>...
  (truncated)</p> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ty/commit/5c9e342c2ea67a0ac8749d32296dd3071974927a"><code>5c9e342</code></a>
  Bump version to 0.0.27 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3185">#3185</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/e6a57315251f37ab3516cb614f891ece91595393"><code>e6a5731</code></a>
  Update actions/cache action to v5.0.4 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3172">#3172</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/c47b982b86bb599d016af1d235174391f618ff16"><code>c47b982</code></a>
  Update prek dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3173">#3173</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/657abcfc82221440481f9c9b76c6b6a3b89d5d00"><code>657abcf</code></a>
  Update astral-sh/setup-uv action to v8 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3174">#3174</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/9e582cb48e9c2306073091d554c04853091d612b"><code>9e582cb</code></a>
  Fetch the cargo-dist binary directly instead of using the installer (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3160">#3160</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/d5c51ea65be68cffcfa1afe204e5f6003fc06b02"><code>d5c51ea</code></a>
  docs: use content tabs (<a

href="https://redirect.github.com/astral-sh/ty/issues/3146">#3146</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/9893776cbd744bec84a43463728ab3813b00968f"><code>9893776</code></a>
  Use the <code>release</code> environment in <code>publish-docs</code> (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3147">#3147</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/94030512727f4320e8184f120c4330ed8f42ec6f"><code>9403051</code></a>
  Bump version to 0.0.26 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3145">#3145</a>)</li> <li>See full diff in
  <a href="https://github.com/astral-sh/ty/compare/0.0.25...0.0.27">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ty&package-manager=uv&previous-version=0.0.25&new-version=0.0.27)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ty from 0.0.27 to 0.0.29
  ([`1644e76`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/1644e76fe7e0bda9401fd06cb3965efca7817e41))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.27 to 0.0.29. - [Release
  notes](https://github.com/astral-sh/ty/releases) -
  [Changelog](https://github.com/astral-sh/ty/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ty/compare/0.0.27...0.0.29)

--- updated-dependencies: - dependency-name: ty dependency-version: 0.0.29

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ty from 0.0.27 to 0.0.29
  ([`badc67c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/badc67c6a8b8dfc80103eb2853437022048d19a3))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.27 to 0.0.29. - [Release
  notes](https://github.com/astral-sh/ty/releases) -
  [Changelog](https://github.com/astral-sh/ty/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ty/compare/0.0.27...0.0.29)

--- updated-dependencies: - dependency-name: ty dependency-version: 0.0.29

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ty from 0.0.27 to 0.0.29
  ([#14](https://github.com/jakub-k-slys/substack-gateway-oss/pull/14),
  [`1fb873b`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/1fb873b312be0189ddbbf9fba93eb6c45dbc893a))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.27 to 0.0.29. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ty/releases">ty's
  releases</a>.</em></p> <blockquote> <h2>0.0.29</h2> <h2>Release Notes</h2> <p>Released on
  2026-04-05.</p> <h3>Bug fixes</h3> <ul> <li>Avoid special-casing for
  <code>dataclasses.field</code> if it's not in <code>field_specifiers</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24397">#24397</a>)</li> <li>Reject
  unsupported <code>environment.python-version</code> values in configuration files (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24402">#24402</a>)</li> <li>Respect
  supported lower bounds from <code>requires-python</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24401">#24401</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Add support for <code>types.new_class</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23144">#23144</a>)</li> <li>Fix PEP 695 type
  aliases in <code>with</code> statement (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24395">#24395</a>)</li> <li>Respect
  <code>__new__</code> and metaclass <code>__call__</code> return types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24357">#24357</a>)</li> <li>Treat enum
  attributes with type annotations as members (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23776">#23776</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/carljm"><code>@​carljm</code></a></li> </ul> <h2>Install ty 0.0.29</h2>
  <h3>Install prebuilt binaries via shell script</h3> <pre lang="sh"><code>curl --proto '=https'
  --tlsv1.2 -LsSf https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-installer.sh | sh
  </code></pre> <h3>Install prebuilt binaries via powershell script</h3> <pre
  lang="sh"><code>powershell -ExecutionPolicy Bypass -c &quot;irm
  https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-installer.ps1 | iex&quot;
  </code></pre> <h2>Download ty 0.0.29</h2> <table> <thead> <tr> <th>File</th> <th>Platform</th>
  <th>Checksum</th> </tr> </thead> <tbody> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-aarch64-apple-darwin.tar.gz">ty-aarch64-apple-darwin.tar.gz</a></td>
  <td>Apple Silicon macOS</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-aarch64-apple-darwin.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-x86_64-apple-darwin.tar.gz">ty-x86_64-apple-darwin.tar.gz</a></td>
  <td>Intel macOS</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-x86_64-apple-darwin.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-aarch64-pc-windows-msvc.zip">ty-aarch64-pc-windows-msvc.zip</a></td>
  <td>ARM64 Windows</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-aarch64-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-i686-pc-windows-msvc.zip">ty-i686-pc-windows-msvc.zip</a></td>
  <td>x86 Windows</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-i686-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-x86_64-pc-windows-msvc.zip">ty-x86_64-pc-windows-msvc.zip</a></td>
  <td>x64 Windows</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-x86_64-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-aarch64-unknown-linux-gnu.tar.gz">ty-aarch64-unknown-linux-gnu.tar.gz</a></td>
  <td>ARM64 Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-aarch64-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-i686-unknown-linux-gnu.tar.gz">ty-i686-unknown-linux-gnu.tar.gz</a></td>
  <td>x86 Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-i686-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-powerpc64-unknown-linux-gnu.tar.gz">ty-powerpc64-unknown-linux-gnu.tar.gz</a></td>
  <td>PPC64 Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-powerpc64-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-powerpc64le-unknown-linux-gnu.tar.gz">ty-powerpc64le-unknown-linux-gnu.tar.gz</a></td>
  <td>PPC64LE Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-powerpc64le-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> </tbody> </table> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details>
  <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ty/blob/main/CHANGELOG.md">ty's changelog</a>.</em></p>
  <blockquote> <h2>0.0.29</h2> <p>Released on 2026-04-05.</p> <h3>Bug fixes</h3> <ul> <li>Avoid
  special-casing for <code>dataclasses.field</code> if it's not in <code>field_specifiers</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24397">#24397</a>)</li> <li>Reject
  unsupported <code>environment.python-version</code> values in configuration files (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24402">#24402</a>)</li> <li>Respect
  supported lower bounds from <code>requires-python</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24401">#24401</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Add support for <code>types.new_class</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23144">#23144</a>)</li> <li>Fix PEP 695 type
  aliases in <code>with</code> statement (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24395">#24395</a>)</li> <li>Respect
  <code>__new__</code> and metaclass <code>__call__</code> return types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24357">#24357</a>)</li> <li>Treat enum
  attributes with type annotations as members (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23776">#23776</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/carljm"><code>@​carljm</code></a></li> </ul> <h2>0.0.28</h2> <p>Released
  on 2026-04-02.</p> <h3>Bug fixes</h3> <ul> <li>Mark loop header assignments as used to avoid false
  positives in &quot;unused variable&quot; diagnostics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24336">#24336</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Show constructor signature of classes when hovering over them (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24257">#24257</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Avoid emitting cascading diagnostics when parsing invalid type expressions
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24326">#24326</a>)</li> <li>Handle most
  &quot;deep&quot; mutual TypeVar constraints (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24079">#24079</a>)</li> <li>Improve
  consistency and quality of diagnostics relating to invalid type forms (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24325">#24325</a>)</li> <li>Improve
  robustness of various type-qualifier-related checks (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24251">#24251</a>)</li> <li>Infer the
  <code>extra_items</code> keyword argument to class-based TypedDicts as an annotation expression
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24362">#24362</a>)</li> <li>Use
  bidirectional inference to fix false positives on operations such as <code>x: list[int | None] =
  [None] * 2</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24197">#24197</a>)</li> <li>Sync vendored
  typeshed stubs (<a href="https://redirect.github.com/astral-sh/ruff/pull/24340">#24340</a>). <a
  href="https://github.com/python/typeshed/compare/f8f0794d0fe249c06dc9f31a004d85be6cca6ced...c5e47faeda2cf9d233f91bc1dc95814b0cc7ccba">Typeshed
  diff</a></li> <li>Tighten up validation of subscripts and attributes in type expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24329">#24329</a>)</li> <li>Use
  <code>infer_type_expression</code> for parsing parameter annotations and return-type annotations
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24353">#24353</a>)</li> <li>Use
  <code>infer_type_expression</code> for validating PEP-613 type aliases (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24370">#24370</a>)</li> <li>Validate
  TypedDict fields when subclassing (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24338">#24338</a>)</li> <li>Validate type
  qualifiers in functional TypedDict fields and the <code>extra_items</code> keyword to functional
  TypedDicts (<a href="https://redirect.github.com/astral-sh/ruff/pull/24360">#24360</a>)</li>
  <li>Improve diagnostics for invalid functional <code>TypedDict</code>s (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24345">#24345</a>)</li> </ul> <!-- raw HTML
  omitted --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Commits</summary>
  <ul> <li><a
  href="https://github.com/astral-sh/ty/commit/438a78d688a38781e0675e57874b30dfed5fc964"><code>438a78d</code></a>
  Bump version to 0.0.29 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3218">#3218</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/927aad261f59c957f83237471b4441dfce1ff425"><code>927aad2</code></a>
  Bump version to 0.0.28 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3206">#3206</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/29d288e5e8012277f94aff7fdcff913b65f13f39"><code>29d288e</code></a>
  Publish installers to <code>/installers/ty/latest</code> on the mirror (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3202">#3202</a>)</li> <li>See full diff in
  <a href="https://github.com/astral-sh/ty/compare/0.0.27...0.0.29">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ty&package-manager=uv&previous-version=0.0.27&new-version=0.0.29)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ty from 0.0.27 to 0.0.29
  ([#62](https://github.com/jakub-k-slys/substack-gateway-oss/pull/62),
  [`a2ffe95`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/a2ffe95603af9d0dc20afeb0838d84e4ac839540))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.27 to 0.0.29. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ty/releases">ty's
  releases</a>.</em></p> <blockquote> <h2>0.0.29</h2> <h2>Release Notes</h2> <p>Released on
  2026-04-05.</p> <h3>Bug fixes</h3> <ul> <li>Avoid special-casing for
  <code>dataclasses.field</code> if it's not in <code>field_specifiers</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24397">#24397</a>)</li> <li>Reject
  unsupported <code>environment.python-version</code> values in configuration files (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24402">#24402</a>)</li> <li>Respect
  supported lower bounds from <code>requires-python</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24401">#24401</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Add support for <code>types.new_class</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23144">#23144</a>)</li> <li>Fix PEP 695 type
  aliases in <code>with</code> statement (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24395">#24395</a>)</li> <li>Respect
  <code>__new__</code> and metaclass <code>__call__</code> return types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24357">#24357</a>)</li> <li>Treat enum
  attributes with type annotations as members (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23776">#23776</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/carljm"><code>@​carljm</code></a></li> </ul> <h2>Install ty 0.0.29</h2>
  <h3>Install prebuilt binaries via shell script</h3> <pre lang="sh"><code>curl --proto '=https'
  --tlsv1.2 -LsSf https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-installer.sh | sh
  </code></pre> <h3>Install prebuilt binaries via powershell script</h3> <pre
  lang="sh"><code>powershell -ExecutionPolicy Bypass -c &quot;irm
  https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-installer.ps1 | iex&quot;
  </code></pre> <h2>Download ty 0.0.29</h2> <table> <thead> <tr> <th>File</th> <th>Platform</th>
  <th>Checksum</th> </tr> </thead> <tbody> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-aarch64-apple-darwin.tar.gz">ty-aarch64-apple-darwin.tar.gz</a></td>
  <td>Apple Silicon macOS</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-aarch64-apple-darwin.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-x86_64-apple-darwin.tar.gz">ty-x86_64-apple-darwin.tar.gz</a></td>
  <td>Intel macOS</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-x86_64-apple-darwin.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-aarch64-pc-windows-msvc.zip">ty-aarch64-pc-windows-msvc.zip</a></td>
  <td>ARM64 Windows</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-aarch64-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-i686-pc-windows-msvc.zip">ty-i686-pc-windows-msvc.zip</a></td>
  <td>x86 Windows</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-i686-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-x86_64-pc-windows-msvc.zip">ty-x86_64-pc-windows-msvc.zip</a></td>
  <td>x64 Windows</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-x86_64-pc-windows-msvc.zip.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-aarch64-unknown-linux-gnu.tar.gz">ty-aarch64-unknown-linux-gnu.tar.gz</a></td>
  <td>ARM64 Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-aarch64-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-i686-unknown-linux-gnu.tar.gz">ty-i686-unknown-linux-gnu.tar.gz</a></td>
  <td>x86 Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-i686-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-powerpc64-unknown-linux-gnu.tar.gz">ty-powerpc64-unknown-linux-gnu.tar.gz</a></td>
  <td>PPC64 Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-powerpc64-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> <tr> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-powerpc64le-unknown-linux-gnu.tar.gz">ty-powerpc64le-unknown-linux-gnu.tar.gz</a></td>
  <td>PPC64LE Linux</td> <td><a
  href="https://releases.astral.sh/github/ty/releases/download/0.0.29/ty-powerpc64le-unknown-linux-gnu.tar.gz.sha256">checksum</a></td>
  </tr> </tbody> </table> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details>
  <details> <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ty/blob/main/CHANGELOG.md">ty's changelog</a>.</em></p>
  <blockquote> <h2>0.0.29</h2> <p>Released on 2026-04-05.</p> <h3>Bug fixes</h3> <ul> <li>Avoid
  special-casing for <code>dataclasses.field</code> if it's not in <code>field_specifiers</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24397">#24397</a>)</li> <li>Reject
  unsupported <code>environment.python-version</code> values in configuration files (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24402">#24402</a>)</li> <li>Respect
  supported lower bounds from <code>requires-python</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24401">#24401</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Add support for <code>types.new_class</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23144">#23144</a>)</li> <li>Fix PEP 695 type
  aliases in <code>with</code> statement (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24395">#24395</a>)</li> <li>Respect
  <code>__new__</code> and metaclass <code>__call__</code> return types (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24357">#24357</a>)</li> <li>Treat enum
  attributes with type annotations as members (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/23776">#23776</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> <li><a
  href="https://github.com/carljm"><code>@​carljm</code></a></li> </ul> <h2>0.0.28</h2> <p>Released
  on 2026-04-02.</p> <h3>Bug fixes</h3> <ul> <li>Mark loop header assignments as used to avoid false
  positives in &quot;unused variable&quot; diagnostics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24336">#24336</a>)</li> </ul> <h3>LSP
  server</h3> <ul> <li>Show constructor signature of classes when hovering over them (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24257">#24257</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Avoid emitting cascading diagnostics when parsing invalid type expressions
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24326">#24326</a>)</li> <li>Handle most
  &quot;deep&quot; mutual TypeVar constraints (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24079">#24079</a>)</li> <li>Improve
  consistency and quality of diagnostics relating to invalid type forms (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24325">#24325</a>)</li> <li>Improve
  robustness of various type-qualifier-related checks (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24251">#24251</a>)</li> <li>Infer the
  <code>extra_items</code> keyword argument to class-based TypedDicts as an annotation expression
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24362">#24362</a>)</li> <li>Use
  bidirectional inference to fix false positives on operations such as <code>x: list[int | None] =
  [None] * 2</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24197">#24197</a>)</li> <li>Sync vendored
  typeshed stubs (<a href="https://redirect.github.com/astral-sh/ruff/pull/24340">#24340</a>). <a
  href="https://github.com/python/typeshed/compare/f8f0794d0fe249c06dc9f31a004d85be6cca6ced...c5e47faeda2cf9d233f91bc1dc95814b0cc7ccba">Typeshed
  diff</a></li> <li>Tighten up validation of subscripts and attributes in type expressions (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24329">#24329</a>)</li> <li>Use
  <code>infer_type_expression</code> for parsing parameter annotations and return-type annotations
  (<a href="https://redirect.github.com/astral-sh/ruff/pull/24353">#24353</a>)</li> <li>Use
  <code>infer_type_expression</code> for validating PEP-613 type aliases (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24370">#24370</a>)</li> <li>Validate
  TypedDict fields when subclassing (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24338">#24338</a>)</li> <li>Validate type
  qualifiers in functional TypedDict fields and the <code>extra_items</code> keyword to functional
  TypedDicts (<a href="https://redirect.github.com/astral-sh/ruff/pull/24360">#24360</a>)</li>
  <li>Improve diagnostics for invalid functional <code>TypedDict</code>s (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24345">#24345</a>)</li> </ul> <!-- raw HTML
  omitted --> </blockquote> <p>... (truncated)</p> </details> <details> <summary>Commits</summary>
  <ul> <li><a
  href="https://github.com/astral-sh/ty/commit/438a78d688a38781e0675e57874b30dfed5fc964"><code>438a78d</code></a>
  Bump version to 0.0.29 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3218">#3218</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/927aad261f59c957f83237471b4441dfce1ff425"><code>927aad2</code></a>
  Bump version to 0.0.28 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3206">#3206</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/29d288e5e8012277f94aff7fdcff913b65f13f39"><code>29d288e</code></a>
  Publish installers to <code>/installers/ty/latest</code> on the mirror (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3202">#3202</a>)</li> <li>See full diff in
  <a href="https://github.com/astral-sh/ty/compare/0.0.27...0.0.29">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ty&package-manager=uv&previous-version=0.0.27&new-version=0.0.29)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

---

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

- **deps-dev**: Bump ty from 0.0.29 to 0.0.31
  ([`ec206d3`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/ec206d33157f1c66bf64299559c482f9d07fc787))

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.29 to 0.0.31. - [Release
  notes](https://github.com/astral-sh/ty/releases) -
  [Changelog](https://github.com/astral-sh/ty/blob/main/CHANGELOG.md) -
  [Commits](https://github.com/astral-sh/ty/compare/0.0.29...0.0.31)

--- updated-dependencies: - dependency-name: ty dependency-version: 0.0.31

dependency-type: direct:development

update-type: version-update:semver-patch ...

Signed-off-by: dependabot[bot] <support@github.com>

- **deps-dev**: Bump ty from 0.0.29 to 0.0.31
  ([#68](https://github.com/jakub-k-slys/substack-gateway-oss/pull/68),
  [`cdd1467`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/cdd1467112e798619e212fbf82f9227e5bc48a3c))

[//]: # (dependabot-start) ⚠️ **Dependabot is rebasing this PR** ⚠️

Rebasing might not happen immediately, so don't worry if this takes some time.

Note: if you make any changes to this PR yourself, they will take precedence over the rebase.

---

[//]: # (dependabot-end)

Bumps [ty](https://github.com/astral-sh/ty) from 0.0.29 to 0.0.31. <details> <summary>Release
  notes</summary> <p><em>Sourced from <a href="https://github.com/astral-sh/ty/releases">ty's
  releases</a>.</em></p> <blockquote> <h2>0.0.31</h2> <h2>Release Notes</h2> <p>Released on
  2026-04-15.</p> <h3>Bug fixes</h3> <ul> <li>Avoid panic from double inference for
  <code>namedtuple(typename=T, field_names=x, **{})</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24641">#24641</a>)</li> <li>Avoid panic from
  double inference with missing functional <code>Enum(...)</code> names (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24638">#24638</a>)</li> <li>Avoid panic from
  double inference with functional <code>Enum(value=...)</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24639">#24639</a>)</li> <li>Fix cases where
  <code>invalid-key</code> fix doesn't converge, and <code>override-of-final-method</code> produces
  invalid syntax (<a href="https://redirect.github.com/astral-sh/ruff/pull/24649">#24649</a>)</li>
  <li>Fix unnecessary <code>ty:ignore</code> comments inserted by <code>--add-ignore</code> for
  diagnostics starting on the same line (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24651">#24651</a>)</li> </ul> <h3>CLI</h3>
  <ul> <li>Add <code>--fix</code> mode to enable auto-fix for diagnostics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24097">#24097</a>)</li> </ul>
  <h3>Performance</h3> <ul> <li>Avoid excessive memory usage for dataclasses with many fields (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24620">#24620</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Check inherited <code>NamedTuple</code> field conflicts (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24542">#24542</a>)</li> <li>Error when
  duplicate keywords are provided to TypedDict constructors (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24449">#24449</a>)</li> <li>Respect mixed
  positional and keyword arguments in TypedDict constructor (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24448">#24448</a>)</li> <li>Respect subclass
  shadowing for inherited NamedTuple fields (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24640">#24640</a>)</li> <li>Skip
  <code>EnumMeta.__call__</code> for enum constructor signatures (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24513">#24513</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/sharkdp"><code>@​sharkdp</code></a></li> <li><a
  href="https://github.com/Glyphack"><code>@​Glyphack</code></a></li> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> </ul> <h2>Install ty
  0.0.31</h2> <h3>Install prebuilt binaries via shell script</h3> <pre lang="sh"><code>curl --proto
  '=https' --tlsv1.2 -LsSf
  https://releases.astral.sh/github/ty/releases/download/0.0.31/ty-installer.sh | sh </code></pre>
  <h3>Install prebuilt binaries via powershell script</h3> <pre lang="sh"><code>powershell
  -ExecutionPolicy Bypass -c &quot;irm
  https://releases.astral.sh/github/ty/releases/download/0.0.31/ty-installer.ps1 | iex&quot;
  </code></pre> <!-- raw HTML omitted --> </blockquote> <p>... (truncated)</p> </details> <details>
  <summary>Changelog</summary> <p><em>Sourced from <a
  href="https://github.com/astral-sh/ty/blob/main/CHANGELOG.md">ty's changelog</a>.</em></p>
  <blockquote> <h2>0.0.31</h2> <p>Released on 2026-04-15.</p> <h3>Bug fixes</h3> <ul> <li>Avoid
  panic from double inference for <code>namedtuple(typename=T, field_names=x, **{})</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24641">#24641</a>)</li> <li>Avoid panic from
  double inference with missing functional <code>Enum(...)</code> names (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24638">#24638</a>)</li> <li>Avoid panic from
  double inference with functional <code>Enum(value=...)</code> (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24639">#24639</a>)</li> <li>Fix cases where
  <code>invalid-key</code> fix doesn't converge, and <code>override-of-final-method</code> produces
  invalid syntax (<a href="https://redirect.github.com/astral-sh/ruff/pull/24649">#24649</a>)</li>
  <li>Fix unnecessary <code>ty:ignore</code> comments inserted by <code>--add-ignore</code> for
  diagnostics starting on the same line (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24651">#24651</a>)</li> </ul> <h3>CLI</h3>
  <ul> <li>Add <code>--fix</code> mode to enable auto-fix for diagnostics (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24097">#24097</a>)</li> </ul>
  <h3>Performance</h3> <ul> <li>Avoid excessive memory usage for dataclasses with many fields (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24620">#24620</a>)</li> </ul> <h3>Core type
  checking</h3> <ul> <li>Check inherited <code>NamedTuple</code> field conflicts (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24542">#24542</a>)</li> <li>Error when
  duplicate keywords are provided to TypedDict constructors (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24449">#24449</a>)</li> <li>Respect mixed
  positional and keyword arguments in TypedDict constructor (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24448">#24448</a>)</li> <li>Respect subclass
  shadowing for inherited NamedTuple fields (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24640">#24640</a>)</li> <li>Skip
  <code>EnumMeta.__call__</code> for enum constructor signatures (<a
  href="https://redirect.github.com/astral-sh/ruff/pull/24513">#24513</a>)</li> </ul>
  <h3>Contributors</h3> <ul> <li><a
  href="https://github.com/sharkdp"><code>@​sharkdp</code></a></li> <li><a
  href="https://github.com/Glyphack"><code>@​Glyphack</code></a></li> <li><a
  href="https://github.com/MichaReiser"><code>@​MichaReiser</code></a></li> <li><a
  href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li> </ul>
  <h2>0.0.30</h2> <p>Released on 2026-04-13.</p> <p>As of v0.0.30, ty no longer unions
  <code>Unknown</code> into most inferred types of unannotated attributes. For example:</p> <pre
  lang="python"><code>class Foo: def __init__(self) -&gt; None: self.value = 1
  <p>reveal_type(Foo().value) # revealed: int Foo().value = &quot;x&quot; # error:
  [invalid-assignment] </code></pre></p> <!-- raw HTML omitted --> </blockquote> <p>...
  (truncated)</p> </details> <details> <summary>Commits</summary> <ul> <li><a
  href="https://github.com/astral-sh/ty/commit/daaa40454966558ffd2a0ea3dcf86bc1749c8715"><code>daaa404</code></a>
  Bump version to 0.0.31 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3280">#3280</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/12e86b58b5034a29266268195afc16feeab6e3ea"><code>12e86b5</code></a>
  Bump version to 0.0.30 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3270">#3270</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/67077ad5fbde5adc1df0e3169525040ad1139dab"><code>67077ad</code></a>
  Reorder sections in FAQ (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3267">#3267</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/01144db2dc10e0e8dbf1665fbb7faf1a545d0df4"><code>01144db</code></a>
  Update docker/login-action action to v4.1.0 (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3262">#3262</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/48b3fe3d5636f8ac337f0e9cf014c80190a1b427"><code>48b3fe3</code></a>
  Update prek dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3261">#3261</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/7c8133816405d504c81651f341b833ae12c9574b"><code>7c81338</code></a>
  Create a &quot;deployment&quot; for the release-gate job (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3239">#3239</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/a447e03aa5a8147aa69ed9eac5d68d36198d6237"><code>a447e03</code></a>
  Add a &quot;release-gate&quot; step to the release workflow (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3205">#3205</a>)</li> <li><a
  href="https://github.com/astral-sh/ty/commit/5131a0e5c26d3cb4daf5fb489ddd54beca8e4a61"><code>5131a0e</code></a>
  Update prek dependencies (<a
  href="https://redirect.github.com/astral-sh/ty/issues/3221">#3221</a>)</li> <li>See full diff in
  <a href="https://github.com/astral-sh/ty/compare/0.0.29...0.0.31">compare view</a></li> </ul>
  </details> <br />

[![Dependabot compatibility
  score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=ty&package-manager=uv&previous-version=0.0.29&new-version=0.0.31)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can
  also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start) [//]: # (dependabot-automerge-end)

<details> <summary>Dependabot commands and options</summary> <br />

You can trigger Dependabot actions by commenting on this PR: - `@dependabot rebase` will rebase this
  PR - `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
  - `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of
  the specified dependency - `@dependabot ignore this major version` will close this PR and stop
  Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it
  yourself) - `@dependabot ignore this minor version` will close this PR and stop Dependabot
  creating any more for this minor version (unless you reopen the PR or upgrade to it yourself) -
  `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for
  this dependency (unless you reopen the PR or upgrade to it yourself)

</details>

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

- Bump GHA versions
  ([`a41ecfc`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/a41ecfc171b9576533175fd894b4d788f551f216))

- Bump GHA versions
  ([`1885091`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/188509193d3e48428318b5364a3e3d5fe57f96e0))

- Expand e2e summary to show per-scenario results
  ([`acc2b3f`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/acc2b3f0ea51bcd510b8cdaddcbe5f4750b1f72b))

Replace the feature-level aggregated table with a section per feature that lists each scenario
  individually, showing Passed / Failed / Skipped status for every testcase element in the JUnit XML
  output.

https://claude.ai/code/session_014PHSG4aNJ8F6gj8GFesYan

- Expand e2e summary to show per-scenario results
  ([#70](https://github.com/jakub-k-slys/substack-gateway-oss/pull/70),
  [`4ad36d9`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/4ad36d9d9f27e481962710c27e4d37af3ad5b4ec))

Replace the feature-level aggregated table with a section per feature that lists each scenario
  individually, showing Passed / Failed / Skipped status for every testcase element in the JUnit XML
  output.

https://claude.ai/code/session_014PHSG4aNJ8F6gj8GFesYan

- Rework deployment
  ([`ddf8c99`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/ddf8c9918920b8e3d8bc49e7ab1467b50f7d777a))

- Run e2e tests twice daily at 08:00 and 16:00 UTC
  ([`f5a5342`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/f5a534218c4d3077f418d52fdd9382eab3dde5b1))

https://claude.ai/code/session_014PHSG4aNJ8F6gj8GFesYan

- Send per-scenario e2e results to Telegram
  ([`5f45e18`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/5f45e181afe46981a0971da0081dd8badbc0baa6))

Mirror the step summary detail level in the Telegram message: each feature section now lists every
  scenario with its individual pass/fail/skip icon, matching what is already shown in the GitHub
  step summary.

https://claude.ai/code/session_011QtA5GwTxad1m4DhiBCVaS

- Send per-scenario e2e results to Telegram
  ([#71](https://github.com/jakub-k-slys/substack-gateway-oss/pull/71),
  [`d15da56`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/d15da56bb10d6795c9749b4b85de67274a949be1))

Mirror the step summary detail level in the Telegram message: each feature section now lists every
  scenario with its individual pass/fail/skip icon, matching what is already shown in the GitHub
  step summary.

https://claude.ai/code/session_011QtA5GwTxad1m4DhiBCVaS

- Update production GHA
  ([`367b05c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/367b05c713cb6f782263b2d7b64887597f8a6a23))

- Update pyproject.toml
  ([`e5a7140`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e5a714005727a2c86d42fe0244c1655f9c3d2a3f))

- Update release workflow to use new token and remove schedule
  ([`a9ef276`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/a9ef276bd6d14b7a7fb3435706de0a8e666450e1))

Removed scheduled trigger and updated GitHub token secrets.

### Documentation

- Clarify validation and semver commit rules
  ([`1384c35`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/1384c355201224a679d6a3dc18c97c8d7e1cc0ee))

### Features

- Add following Atom feed for pro users
  ([#60](https://github.com/jakub-k-slys/substack-gateway-oss/pull/60),
  [`a2fd8fe`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/a2fd8fe4c1c93c9626950fc64b394fb49baddb83))

- Add GET /api/v1/profiles/{slug} endpoint
  ([`fd7ae29`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/fd7ae29a8628b8639b8b50297d0ddb7ed0353f48))

Exposes public Substack profile lookup by handle/slug. Promotes _get_profile_by_slug to a public
  client method and wires it through a new profiles router with full BDD test coverage (5
  scenarios).

https://claude.ai/code/session_01Q67ac3YRNupaRFNHPxt2Ks

- Add GET /me/notes and GET /me/posts endpoints
  ([`456f942`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/456f94265a5bd4e54cd6fecc8b8bc6ebaf0f1b86))

Notes uses cursor-based pagination (GET /notes?cursor=). Posts resolves the authenticated user's
  numeric ID first via the profile chain, then fetches GET /profile/posts?profile_user_id={id}.

Adds SubstackNote/SubstackPreviewPost Pydantic models, NoteResponse/ PostResponse schemas, two new
  client methods, and 8 BDD scenarios across me_notes.feature and me_posts.feature.

https://claude.ai/code/session_01Q67ac3YRNupaRFNHPxt2Ks

- Add GET /posts/{id} and GET /posts/{id}/comments endpoints
  ([`16e4f3a`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/16e4f3a715df392956ff3df8a47841479fc35a14))

Post lookup hits the global substack.com endpoint (GET /posts/by-id/{id}) and returns full post data
  including html_body, reactions, tags, and cover_image. Comments hit the publication-scoped
  endpoint (GET /post/{id}/comments) and return a flat items list.

Adds SubstackFullPost/SubstackComment Pydantic models, FullPostResponse/
  CommentResponse/CommentsResponse schemas, two client methods, and 7 BDD scenarios in
  posts.feature.

https://claude.ai/code/session_01Q67ac3YRNupaRFNHPxt2Ks

- Add GET /profiles/{slug}/posts and GET /profiles/{slug}/notes
  ([`8a8c69c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/8a8c69c9f9a7b41640778dca3b99d50da28864f5))

Both endpoints resolve slug → profile id via public_profile first. Posts then hit GET /profile/posts
  (pub-scoped, offset pagination). Notes hit GET /reader/feed/profile/{id}?types=note (global
  substack.com, cursor pagination).

Also fixes a bug in get_own_posts: the real Substack /profile/posts response wraps posts in { posts:
  [...], nextCursor } rather than returning a bare array. Introduced SubstackProfilePostsPage model
  and PostsPageResponse.from_substack() factory to handle the wrapper. Updated the synthetic posts
  sample to match the real envelope shape.

8 new BDD scenarios across profile_posts.feature and profile_notes.feature.

https://claude.ai/code/session_01Q67ac3YRNupaRFNHPxt2Ks

- Add Pro note and post like APIs plus MCP tools
  ([#58](https://github.com/jakub-k-slys/substack-gateway-oss/pull/58),
  [`40b39e2`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/40b39e24e405394ff84a3e9051c8a2f7aae39782))

Adds Pro-only like/unlike support for Substack notes and posts across both REST and MCP surfaces.

## REST API

Added Pro-only endpoints:

- `PUT /api/v1/notes/{note_id}/like` - `DELETE /api/v1/notes/{note_id}/like` - `PUT
  /api/v1/posts/{post_id}/like` - `DELETE /api/v1/posts/{post_id}/like`

All endpoints return `204 No Content`.

## MCP

Added Pro-only MCP tools:

- `like_note(note_id, token)` - `unlike_note(note_id, token)` - `like_post(post_id, token)` -
  `unlike_post(post_id, token)`

The MCP tools return simple confirmation messages.

## Upstream mapping

Notes: - like: `POST /api/v1/comment/{id}/reaction` - unlike: `DELETE /api/v1/comment/{id}/reaction`
  - hardcoded note unlike payload includes `tabId: "for-you"`

Posts: - like: `POST /api/v1/post/{id}/reaction` - unlike: `DELETE /api/v1/post/{id}/reaction` -
  post like uses `{"reaction":"❤","surface":"reader"}` - post unlike uses `{}`

- Add tier-specific root metadata
  ([`ed5dbc5`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/ed5dbc5b689a40aaf80576e6f6f2fedc44ff0843))

- Add tier-specific root metadata
  ([`5d2116f`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/5d2116fc7ed105786f1d97976b9e2cef95322616))

- Cache following feed profiles
  ([`e42905e`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e42905e5e5b15997290a7128d2ef7e5709da9d66))

- Dockerize Gateway PRO
  ([`3e09b58`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/3e09b586b920871175efa3ae5abc1e5060f50c83))

- Expose application feature metadata
  ([`2ff9aea`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/2ff9aea6acb0a4fa02ccbb1b347b6ffedfd72a8f))

- Format pro feature environment
  ([`34eb44c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/34eb44ceb9f821bb4906770bbd83ed844f9f1cf6))

- Initialize Substack Gateway OSS
  ([`35c5dd8`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/35c5dd83534cac6915d45f135b38fb162bcfb777))

- Make oss mcp read only
  ([`6393557`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/63935572d093a39037e919dd855fc86ded27720c))

- Make oss mcp read only
  ([`bba485b`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/bba485b623b7fc9a6a2b2a3b1ba1fdd1e1f9bbd1))

- Make oss mcp read only
  ([`5259f60`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/5259f60b355a4d6b308506e1482eaa6c0069ca19))

- Mark partial following feeds in responses
  ([`f4a17d0`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/f4a17d055df4c217185b0aeb67db1f595c708130))

- Move publication url into bearer token
  ([`2944387`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/2944387e409880e44d4d66037c9b77fc3f8b0cbb))

- Move publication url into bearer token
  ([`fb5848c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/fb5848c5743935f48c65ccda76fafec3ae4b60ac))

- Move publication url into bearer token
  ([`e87dea9`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/e87dea915d9cc726e489f780ceaf74de928c84eb))

- Normalize Atom feed ids and links
  ([`ba3c3d6`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/ba3c3d6ea6aa4b723004c53c443abbbd90303244))

- Profile feed ([#59](https://github.com/jakub-k-slys/substack-gateway-oss/pull/59),
  [`149e840`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/149e8404ecf2651b70bd5eb9c55d1c47abc5eb7b))

- Provide version on endpoint
  ([`a08534f`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/a08534f8019472c9a40f81e1f35d790c47622bf9))

- Require full validation for code changes
  ([`d9a8cd3`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/d9a8cd30fdadb108bceffca9f9deea2c2cf2a751))

- Require full validation for code changes
  ([`298b0c8`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/298b0c89e5ef18ee59f1c0db4f0373f169a6dfc2))

- Require full validation for code changes
  ([`47882d4`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/47882d4d33a0a7e8284b0df17f1f5bb73ec72b80))

- Separate gateway auth from substack credentials
  ([`79a2200`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/79a22001d9012d7d5880a38b16f69a3f2758b6b7))

- Separate gateway auth from substack credentials
  ([`20c1c83`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/20c1c83935207093e0195a1eb31f9c1c352ac432))

- Separate gateway auth from substack credentials
  ([`571eaf1`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/571eaf12657861a7bc127c4e085b314e6b2c9383))

- Update feed limits and sample fixtures
  ([`0738947`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/0738947f14349667b940d3ad2a313c892f2ac483))

### Refactoring

- Replace oss subtree
  ([`0645984`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/0645984f51c45fe14a288c9316f2cff6b14cb004))

- Split oss and pro config settings
  ([`c161e7a`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/c161e7ae0799fed38e67687316c07c832a52c0e6))

### Testing

- Fix e2e gateway token auth
  ([`c0a1c13`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/c0a1c138ae3efe4fb71f00626d5c3e73d3e271b4))
