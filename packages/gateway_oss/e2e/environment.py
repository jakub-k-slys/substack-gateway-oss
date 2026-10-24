from __future__ import annotations

import os
import time

import httpx

# Substack throttles bursts: run back to back, the suite's last scenarios get
# 429s. The gateway passes those through, so the suite paces itself instead.
_RETRYABLE_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})


class _PacedTransport(httpx.BaseTransport):
    """Space requests out and retry idempotent ones that Substack throttled."""

    # Shared across scenarios: each scenario opens its own client, but the
    # throttling budget belongs to the whole run.
    _last_request_at = 0.0

    def __init__(
        self,
        inner: httpx.BaseTransport,
        *,
        interval_sec: float,
        retries: int,
        backoff_sec: float,
    ) -> None:
        self._inner = inner
        self._interval_sec = interval_sec
        self._retries = retries
        self._backoff_sec = backoff_sec

    def _wait_for_slot(self) -> None:
        cls = type(self)
        delay = cls._last_request_at + self._interval_sec - time.monotonic()
        if delay > 0:
            time.sleep(delay)
        cls._last_request_at = time.monotonic()

    def _retry_delay(self, response: httpx.Response, attempt: int) -> float:
        retry_after = response.headers.get("retry-after", "")
        if retry_after.isdigit():
            return float(retry_after)
        return self._backoff_sec * 2**attempt

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        attempt = 0
        while True:
            self._wait_for_slot()
            response = self._inner.handle_request(request)
            if (
                response.status_code != 429
                or request.method not in _RETRYABLE_METHODS
                or attempt >= self._retries
            ):
                return response
            response.read()
            response.close()
            time.sleep(self._retry_delay(response, attempt))
            attempt += 1

    def close(self) -> None:
        self._inner.close()


def before_scenario(context, scenario):
    configured_base_url = os.environ.get("SUBSTACK_GATEWAY_BASE_URL", "").strip()
    base_url = configured_base_url or "http://localhost:5001"
    timeout_sec = float(os.environ.get("SUBSTACK_GATEWAY_E2E_TIMEOUT_SEC", "120"))
    context.client = httpx.Client(
        base_url=base_url,
        timeout=httpx.Timeout(timeout_sec),
        transport=_PacedTransport(
            httpx.HTTPTransport(),
            interval_sec=float(
                os.environ.get("SUBSTACK_GATEWAY_E2E_REQUEST_INTERVAL_SEC", "1")
            ),
            retries=int(os.environ.get("SUBSTACK_GATEWAY_E2E_429_RETRIES", "4")),
            backoff_sec=float(
                os.environ.get("SUBSTACK_GATEWAY_E2E_429_BACKOFF_SEC", "5")
            ),
        ),
    )
    context.headers: dict[str, str] = {}
    context.response = None
    context.mcp_response = None
    context.mcp_payload = None
    context.draft_id = None
    context.draft_deleted = False

    if not configured_base_url:
        try:
            context.client.get("/")
        except httpx.HTTPError:
            scenario.skip(
                "SUBSTACK_GATEWAY_BASE_URL not configured and local gateway is not running"
            )


def after_scenario(context, scenario):
    # Best-effort cleanup so a failing scenario does not leave a draft behind.
    if context.draft_id and not context.draft_deleted:
        try:
            context.client.delete(
                f"/api/v1/drafts/{context.draft_id}", headers=context.headers
            )
        except httpx.HTTPError:
            pass
    context.client.close()
