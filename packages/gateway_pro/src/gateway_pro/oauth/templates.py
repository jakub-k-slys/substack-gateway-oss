"""HTML page renderers for the three-phase login flow, built with htpy."""

from __future__ import annotations

from htpy import (
    a,
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
    link,
    meta,
    ol,
    p,
    strong,
    summary,
    title,
)
from starlette.responses import HTMLResponse


def _page(content) -> str:
    return f"<!doctype html>{content}"


def render_login(request_id: str, error: str = "") -> HTMLResponse:
    doc = html(lang="en")[
        head[
            meta(charset="UTF-8"),
            meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            title["Substack Gateway — Sign in (1/3)"],
            link(rel="stylesheet", href="/login/static/login.css"),
        ],
        body[
            div(class_="card")[
                p(class_="step")["Step 1 of 3"],
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
            title["Substack Gateway — Connect Substack (2/3)"],
            link(rel="stylesheet", href="/login/static/token.css"),
        ],
        body[
            div(class_="card")[
                p(class_="step")["Step 2 of 3"],
                h1["Connect your Substack"],
                p(class_="sub")[
                    "Enter your base64-encoded Substack token so the gateway can act on your behalf"
                ],
                p(class_="error")[error] if error else None,
                details[
                    summary["How do I create the token?"],
                    div(class_="howto")[
                        ol(style="padding-left:18px")[
                            li["Open ", strong["substack.com"], " and sign in"],
                            li[
                                "Open DevTools → Application → Cookies → ",
                                code["https://substack.com"],
                            ],
                            li[
                                "Copy the values for ",
                                code["publication_url"],
                                ", ",
                                code["substack.sid"],
                                " and ",
                                code["connect.sid"],
                            ],
                            li[
                                "Create JSON: ",
                                code[
                                    '{"publication_url":"https://yourname.substack.com","substack_sid":"…","connect_sid":"…"}'
                                ],
                            ],
                            li["Base64-encode the JSON and paste it below"],
                        ],
                    ],
                ],
                form(method="post")[
                    input(type="hidden", name="session_id", value=session_id),
                    label(for_="token")["Substack token"],
                    input(
                        type="password",
                        id="token",
                        name="token",
                        required=True,
                        placeholder="base64-encoded token",
                    ),
                    p(class_="hint")[
                        "Base64-encoded JSON containing ",
                        code["publication_url"],
                        ", ",
                        code["substack_sid"],
                        " and ",
                        code["connect_sid"],
                    ],
                    button(type="submit")["Authorize"],
                ],
            ],
        ],
    ]
    return HTMLResponse(_page(doc))


def render_success(redirect_url: str) -> HTMLResponse:
    doc = html(lang="en")[
        head[
            meta(charset="UTF-8"),
            meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            title["Substack Gateway — Done (3/3)"],
            link(rel="stylesheet", href="/login/static/token.css"),
        ],
        body[
            div(class_="card")[
                p(class_="step")["Step 3 of 3"],
                h1["All done!"],
                p(class_="sub")["Your Substack account has been connected."],
                a(href=redirect_url, class_="btn")["Complete setup →"],
            ],
        ],
    ]
    return HTMLResponse(_page(doc))
