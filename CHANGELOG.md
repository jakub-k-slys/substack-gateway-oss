# CHANGELOG


## v0.2.0 (2026-03-23)

### Chores

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

### Features

- Add tier-specific root metadata
  ([`ed5dbc5`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/ed5dbc5b689a40aaf80576e6f6f2fedc44ff0843))


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
