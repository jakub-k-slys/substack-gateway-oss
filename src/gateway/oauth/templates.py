"""HTML page renderers for the two-phase login flow, built with htpy."""

from __future__ import annotations

from htpy import (
    body,
    button,
    code,
    details,
    div,
    form,
    h1,
    head,
    html,
    input,
    label,
    li,
    meta,
    ol,
    p,
    strong,
    style,
    summary,
    title,
)
from markupsafe import Markup
from starlette.responses import HTMLResponse

_SHARED_CSS = Markup("""
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f5f0; min-height: 100vh;
  display: flex; align-items: center; justify-content: center;
}
.step { font-size: .78rem; color: #999; font-weight: 600;
        letter-spacing: .05em; text-transform: uppercase; margin-bottom: 6px; }
h1 { font-size: 1.4rem; font-weight: 700; margin-bottom: 4px; color: #111; }
.sub { font-size: .9rem; color: #666; margin-bottom: 28px; }
label { display: block; font-size: .85rem; font-weight: 600; color: #333; margin-bottom: 6px; }
input:focus { border-color: #ff6719; }
button {
  width: 100%; padding: 11px; background: #ff6719; color: #fff;
  border: none; border-radius: 8px; font-size: 1rem;
  font-weight: 600; cursor: pointer; transition: background .15s; margin-top: 12px;
}
button:hover { background: #e55c12; }
.error {
  color: #c0392b; font-size: .88rem; margin-bottom: 16px;
  padding: 10px 12px; background: #fdf3f3;
  border-radius: 6px; border: 1px solid #f5c6cb;
}
""")

_LOGIN_CSS = _SHARED_CSS + Markup("""
.card {
  background: #fff; border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0,0,0,.08);
  padding: 40px 36px; width: 100%; max-width: 380px;
}
input[type=email], input[type=password] {
  width: 100%; padding: 10px 12px;
  border: 1.5px solid #ddd; border-radius: 8px;
  font-size: .95rem; outline: none; margin-bottom: 18px;
  transition: border-color .15s;
}
""")

_TOKEN_CSS = _SHARED_CSS + Markup("""
.card {
  background: #fff; border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0,0,0,.08);
  padding: 40px 36px; width: 100%; max-width: 420px;
}
.hint { font-size: .78rem; color: #888; margin-top: -12px; margin-bottom: 16px; }
input[type=password], input[type=url] {
  width: 100%; padding: 10px 12px;
  border: 1.5px solid #ddd; border-radius: 8px;
  font-size: .95rem; outline: none; margin-bottom: 6px;
  transition: border-color .15s; font-family: monospace;
}
input[type=url] { font-family: inherit; }
details { margin-bottom: 20px; }
summary { font-size: .82rem; color: #888; cursor: pointer; user-select: none; padding: 4px 0; }
.howto {
  font-size: .82rem; color: #555; margin-top: 10px; line-height: 1.6;
  background: #f9f9f6; border-radius: 6px; padding: 12px 14px;
}
code { background: rgba(0,0,0,.06); padding: 1px 5px; border-radius: 3px; font-size: .9em; }
""")


def _page(content) -> str:
    return "<!doctype html>" + str(content)


def render_login(request_id: str, error: str = "") -> HTMLResponse:
    doc = html(lang="en")[
        head[
            meta(charset="UTF-8"),
            meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            title["Substack Gateway — Sign in (1/2)"],
            style[_LOGIN_CSS],
        ],
        body[
            div(class_="card")[
                p(class_="step")["Step 1 of 2"],
                h1["Substack Gateway"],
                p(class_="sub")["Sign in with your account credentials"],
                p(class_="error")[error] if error else None,
                form(method="post")[
                    input(type="hidden", name="request_id", value=request_id),
                    label(for_="email")["Email"],
                    input(
                        type="email",
                        id="email",
                        name="email",
                        required=True,
                        autofocus=True,
                        placeholder="you@example.com",
                    ),
                    label(for_="password")["Password"],
                    input(
                        type="password",
                        id="password",
                        name="password",
                        required=True,
                        placeholder="••••••••",
                    ),
                    button(type="submit")["Continue →"],
                ],
            ],
        ],
    ]
    return HTMLResponse(_page(doc))


def render_token_form(session_id: str, error: str = "") -> HTMLResponse:
    doc = html(lang="en")[
        head[
            meta(charset="UTF-8"),
            meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            title["Substack Gateway — Connect Substack (2/2)"],
            style[_TOKEN_CSS],
        ],
        body[
            div(class_="card")[
                p(class_="step")["Step 2 of 2"],
                h1["Connect your Substack"],
                p(class_="sub")[
                    "Enter your Substack session cookies so the gateway can act on your behalf"
                ],
                p(class_="error")[error] if error else None,
                details[
                    summary["How do I find these values?"],
                    div(class_="howto")[
                        ol(style="padding-left:18px")[
                            li["Open ", strong["substack.com"], " and sign in"],
                            li[
                                "Open DevTools → Application → Cookies → ",
                                code["https://substack.com"],
                            ],
                            li[
                                "Copy the values for ",
                                code["substack.sid"],
                                " and ",
                                code["connect.sid"],
                            ],
                        ],
                    ],
                ],
                form(method="post")[
                    input(type="hidden", name="session_id", value=session_id),
                    label(for_="substack_sid")["substack.sid cookie"],
                    input(
                        type="password",
                        id="substack_sid",
                        name="substack_sid",
                        required=True,
                        placeholder="s%3A…",
                    ),
                    p(class_="hint")["Value of the ", code["substack.sid"], " cookie"],
                    label(for_="connect_sid")["connect.sid cookie"],
                    input(
                        type="password",
                        id="connect_sid",
                        name="connect_sid",
                        required=True,
                        placeholder="s%3A…",
                    ),
                    p(class_="hint")["Value of the ", code["connect.sid"], " cookie"],
                    label(for_="pub_url")["Publication URL"],
                    input(
                        type="url",
                        id="pub_url",
                        name="pub_url",
                        required=True,
                        placeholder="https://yourname.substack.com",
                    ),
                    p(class_="hint")[
                        "Your Substack publication URL (no trailing slash)"
                    ],
                    button(type="submit")["Authorize"],
                ],
            ],
        ],
    ]
    return HTMLResponse(_page(doc))
