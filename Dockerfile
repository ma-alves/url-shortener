FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY . /app

WORKDIR /app
RUN uv sync --frozen --no-cache

CMD ["uv", "run", "uvicorn", "--port", "8000", "--host", "0.0.0.0", "app.main:app"]