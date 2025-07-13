# syntax=docker/dockerfile:1.4

# Base image for all stages
FROM python:3.11-slim as python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Builder stage
FROM python-base as builder
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy project files
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
COPY app ./app

# Install dependencies
RUN poetry install --no-dev --no-root

# Development stage
FROM python-base as development
ENV FASTAPI_ENV=development

COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

WORKDIR $PYSETUP_PATH
COPY . .

# Install development dependencies
RUN poetry install

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.presentation.api.v1.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM python-base as production
ENV FASTAPI_ENV=production

COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

WORKDIR $PYSETUP_PATH
COPY . .

# Create non-root user
RUN addgroup --system --gid 1001 nedlia && \
    adduser --system --uid 1001 --group nedlia && \
    chown -R nedlia:nedlia $PYSETUP_PATH

USER nedlia

EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.presentation.api.v1.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
