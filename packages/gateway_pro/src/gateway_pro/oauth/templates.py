"""HTML page renderers for the three-phase login flow, built with htpy."""

from __future__ import annotations

from htpy import (
    a,
    body,
    button,
    div,
    form,
    h1,
    head,
    html,
    input,
    label,
    link,
    meta,
    p,
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
            title["Substack Gateway — Authorize App (2/3)"],
            link(rel="stylesheet", href="/login/static/token.css"),
        ],
        body[
            div(class_="card")[
                p(class_="step")["Step 2 of 3"],
                h1["Authorize access"],
                p(class_="sub")[
                    "Confirm that this gateway client may access your account."
                ],
                p(class_="error")[error] if error else None,
                form(method="post")[
                    input(type="hidden", name="session_id", value=session_id),
                    p(class_="hint")[
                        "This step authorizes the gateway user account only. "
                        "MCP tool calls provide Substack credentials explicitly."
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
                p(class_="sub")["Gateway access has been authorized."],
                a(href=redirect_url, class_="btn")["Complete setup →"],
            ],
        ],
    ]
    return HTMLResponse(_page(doc))
