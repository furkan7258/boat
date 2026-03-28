FROM python:3.12-slim AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install udsearch from GitLab (dependency of boat-backend)
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
RUN uv pip install --system "ud-tools @ git+https://gitlab.com/furkan4829/tools/ud-tools.git"

COPY pyproject.toml .
RUN uv pip install --system "."

COPY . .

# ---------- production ----------
FROM python:3.12-slim

RUN groupadd -r boat && useradd -r -g boat -d /app -s /sbin/nologin boat

WORKDIR /app

ENV PYTHONPATH=/app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app

RUN chown -R boat:boat /app

USER boat

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

ENTRYPOINT ["./entrypoint.sh"]
