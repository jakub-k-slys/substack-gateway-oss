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
    return "<!doctype html>" + str(content)


def render_login(request_id: str, error: str = "") -> HTMLResponse:
    doc = html(lang="en")[
        head[
            meta(charset="UTF-8"),
            meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            title["Substack Gateway — Sign in (1/2)"],
            link(rel="stylesheet", href="/login/static/login.css"),
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
            link(rel="stylesheet", href="/login/static/token.css"),
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
