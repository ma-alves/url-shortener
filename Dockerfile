FROM python:3.12-slim
RUN useradd -ms /bin/sh -u 1001 app
USER app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# COPY . /app

WORKDIR /app
COPY --chown=app:app . /app

RUN uv sync --frozen --no-cache

CMD ["uv", "run", "uvicorn", "--port", "8000", "--host", "0.0.0.0", "app.main:app"]