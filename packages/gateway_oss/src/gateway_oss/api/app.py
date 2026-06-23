from __future__ import annotations

import logging
import logging.config
import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.responses import Response

from gateway_oss import __app_version__
from gateway_oss.api.v1 import router as v1_router
from gateway_oss.client.exceptions import SubstackAPIError, SubstackAuthError
from gateway_oss.config import settings
from gateway_oss.extensions.runtime import get_runtime

_SILENT_PATHS = {"/api/v1/health/live", "/api/v1/health/ready"}


class _SilentPathsFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        return not any(path in message for path in _SILENT_PATHS)


def _configure_logging() -> None:
    level = settings.log_level.upper()
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "silent_paths": {
                    "()": _SilentPathsFilter,
                },
            },
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
                    "filters": ["silent_paths"],
                    "stream": "ext://sys.stderr",
                },
            },
            "root": {"handlers": ["console"], "level": level},
            "loggers": {
                # Suppress chatty low-level HTTP library debug output.
                "httpx": {"level": "WARNING"},
                "httpcore": {"level": "WARNING"},
                # uvicorn.access has its own handler with propagate=False, so
                # the filter on the console handler doesn't reach it.
                "uvicorn.access": {"filters": ["silent_paths"]},
            },
        }
    )


_configure_logging()

_log = logging.getLogger(__name__)

_PASSTHROUGH_CODES = {404, 429}

api = FastAPI(
    title="Substack Gateway",
    description="REST API gateway for Substack",
    version=__app_version__,
)


@api.middleware("http")
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


def _error_response(
    request: Request, status: int, message: str, log_extra: str
) -> JSONResponse:
    rid = getattr(request.state, "request_id", "-")
    _log.warning(
        "[%s] %s %s %s → %d: %s",
        rid,
        request.method,
        request.url.path,
        log_extra,
        status,
        message,
    )
    return JSONResponse(status_code=status, content={"detail": message})


@api.exception_handler(SubstackAuthError)
async def substack_auth_error_handler(
    request: Request, exc: SubstackAuthError
) -> JSONResponse:
    return _error_response(
        request,
        exc.status_code,
        exc.message,
        f"auth [upstream={exc.status_code}]",
    )


@api.exception_handler(SubstackAPIError)
async def substack_api_error_handler(
    request: Request, exc: SubstackAPIError
) -> JSONResponse:
    # Map specific upstream codes to semantically correct HTTP responses;
    # everything else becomes 502 Bad Gateway.
    status = exc.status_code if exc.status_code in _PASSTHROUGH_CODES else 502
    return _error_response(
        request,
        status,
        exc.message,
        f"api [upstream={exc.status_code} response={status}]",
    )


api.include_router(v1_router, prefix="/v1")
for extension in get_runtime().extensions:
    extension.register_api(api, get_runtime().context)
