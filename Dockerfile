FROM python:3.11-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy

WORKDIR /app

COPY . .

RUN uv build --all-packages --wheel --out-dir /tmp/wheels


FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HOST=0.0.0.0 \
    PORT=5001

WORKDIR /app

COPY --from=builder /tmp/wheels /tmp/wheels

RUN python -m pip install --no-cache-dir /tmp/wheels/*.whl \
    && rm -rf /tmp/wheels

RUN useradd --create-home --shell /usr/sbin/nologin appuser

USER appuser

EXPOSE 5001

CMD ["gateway_oss"]
