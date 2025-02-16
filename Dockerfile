FROM python:3.13-slim as python-base

# Python setup
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Build dependencies
FROM python-base as builder-base
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install poetry using pip
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Copy project dependency files
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

# Install runtime deps
RUN poetry install --no-dev --no-root

# Run stage
FROM python-base as production
ENV FASTAPI_ENV=production

# Copy virtual env from builder
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH

# Create and switch to a new user
RUN useradd --create-home appuser
WORKDIR /app
USER appuser

# Copy application code with read-only permissions
COPY app/ app/
RUN chmod -R 444 /app/app

# Set environment variables
ENV PYTHONPATH=/app \
    ENVIRONMENT=production \
    PYTHONUNBUFFERED=1 \
    FORCE_COLOR=1 \
    HYPERCORN_WORKER_CLASS=asyncio \
    HYPERCORN_WORKERS=2 \
    HYPERCORN_BIND=0.0.0.0:8000 \
    HYPERCORN_ACCESS_LOG=- \
    HYPERCORN_ERROR_LOG=- \
    HYPERCORN_LOG_LEVEL=INFO

# Expose port
EXPOSE 8000

# Run the application with Hypercorn
CMD ["hypercorn", "app.main:app", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--worker-class", "asyncio", \
     "--access-logformat", "%(h)s %(r)s %(s)s %(b)s %(D)s", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "INFO"]
