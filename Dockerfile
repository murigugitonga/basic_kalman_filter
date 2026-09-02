FROM ghcr.io/astral-sh/uv:python3.11-alpine

WORKDIR /app

# Copy lock and project configuration metadata directly
COPY pyproject.toml uv.lock ./

# Synchronize dependencies out of the project workspace context
RUN uv sync --frozen --no-install-project

# Copy active application files
COPY main.py index.html ./

EXPOSE 10000

CMD ["/app/.venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
