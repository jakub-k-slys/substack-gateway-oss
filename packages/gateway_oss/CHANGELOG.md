# CHANGELOG


## v0.5.0 (2026-04-04)

### Chores

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

### Features

- Separate gateway auth from substack credentials
  ([`20c1c83`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/20c1c83935207093e0195a1eb31f9c1c352ac432))


## v0.4.0 (2026-03-23)

### Features

- Make oss mcp read only
  ([`bba485b`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/bba485b623b7fc9a6a2b2a3b1ba1fdd1e1f9bbd1))

- Require full validation for code changes
  ([`298b0c8`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/298b0c89e5ef18ee59f1c0db4f0373f169a6dfc2))


## v0.3.0 (2026-03-23)

### Features

- Move publication url into bearer token
  ([`fb5848c`](https://github.com/jakub-k-slys/substack-gateway-oss/commit/fb5848c5743935f48c65ccda76fafec3ae4b60ac))


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
