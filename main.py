from __future__ import annotations

import logging
import logging.config
import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.responses import Response

from api.v1 import router as v1_router
from client.exceptions import SubstackAPIError, SubstackAuthError
from config import settings


def _configure_logging() -> None:
    level = settings.log_level.upper()
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s %(levelname)-8s %(name)s %(message)s",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stderr",
                },
            },
            "root": {"handlers": ["console"], "level": level},
            "loggers": {
                # Suppress chatty low-level HTTP library debug output.
                "httpx": {"level": "WARNING"},
                "httpcore": {"level": "WARNING"},
            },
        }
    )


_configure_logging()

_log = logging.getLogger(__name__)

app = FastAPI(
    title="Substack Gateway",
    description="REST API gateway for Substack",
    version="1.0.0",
)


@app.middleware("http")
async def log_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    request.state.request_id = request_id
    _log.debug("[%s] → %s %s", request_id, request.method, request.url.path)
    start = time.monotonic()
    response = await call_next(request)
    elapsed = time.monotonic() - start
    _log.info(
        "[%s] %s %s → %d (%.3fs)",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        elapsed,
    )
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(SubstackAuthError)
async def substack_auth_error_handler(
    request: Request, exc: SubstackAuthError
) -> JSONResponse:
    rid = getattr(request.state, "request_id", "-")
    _log.warning(
        "[%s] Auth error on %s %s: [%d] %s",
        rid,
        request.method,
        request.url.path,
        exc.status_code,
        exc.message,
    )
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


@app.exception_handler(SubstackAPIError)
async def substack_api_error_handler(
    request: Request, exc: SubstackAPIError
) -> JSONResponse:
    # Map specific upstream codes to semantically correct HTTP responses;
    # everything else becomes 502 Bad Gateway.
    status = exc.status_code if exc.status_code in _PASSTHROUGH_CODES else 502
    rid = getattr(request.state, "request_id", "-")
    _log.warning(
        "[%s] API error on %s %s: upstream=%d response=%d — %s",
        rid,
        request.method,
        request.url.path,
        exc.status_code,
        status,
        exc.message,
    )
    return JSONResponse(status_code=status, content={"detail": exc.message})


_PASSTHROUGH_CODES = {404, 429}

app.include_router(v1_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True, loop="uvloop")
