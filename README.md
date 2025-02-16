# Nedlia Backend

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=onelasha_nedlia-back-end&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=onelasha_nedlia-back-end)

A modern FastAPI-based backend service built with Clean Architecture principles.

## Project Structure

```
nedlia-back-end/
├── app/                    # Application source code
│   ├── api/               # API layer
│   │   └── v1/           # API version 1 endpoints
│   ├── core/             # Core application code
│   │   └── config.py     # Configuration management
│   ├── domain/           # Domain layer
│   │   ├── entities/     # Business entities
│   │   ├── interfaces/   # Abstract interfaces
│   │   ├── repositories/ # Repository implementations
│   │   └── services/     # Business logic services
│   ├── infrastructure/   # Infrastructure layer
│   │   ├── config/      # Infrastructure configurations
│   │   └── database/    # Database implementations
│   └── main.py          # Application entry point
├── tests/                # Test suite
├── Dockerfile           # Container definition
├── pyproject.toml       # Project dependencies and settings
└── setup.cfg           # Development tool configurations
```

## Prerequisites

- Python 3.13+
- Poetry (Python package manager)
- Docker (optional, for containerized deployment)
- Docker Compose (optional, for local development)
- MongoDB (for data storage)

## Installation

### Using Poetry (Local Development)

1. Clone the repository:
```bash
git clone https://github.com/onelasha/nedlia-back-end.git
cd nedlia-back-end
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create your environment file:
```bash
cat > .env << EOL
# Application
APP_NAME=Nedlia API
APP_VERSION=1.0.0
ENVIRONMENT=development

# Server
HOST=127.0.0.1
PORT=8000

# Feature Flags
GROWTHBOOK_API_HOST=https://cdn.growthbook.io
GROWTHBOOK_CLIENT_KEY=sdk-________
GROWTHBOOK_CACHE_TTL=60
EOL
```

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/onelasha/nedlia-back-end.git
cd nedlia-back-end
```

2. Start the development environment:
```bash
# Development mode with hot reload
docker compose -f docker-compose.dev.yml up

# Or production mode
docker compose up
```

## Running the Application

### Local Development

```bash
# Activate the poetry shell
poetry shell

# Run with Hypercorn (recommended)
poetry run hypercorn app.main:app --reload --bind 0.0.0.0:8000 --log-level DEBUG

# Or use the VS Code launch configuration
# Press F5 and select "FastAPI: Hypercorn" or "FastAPI: Uvicorn"
```

### Docker Development

```bash
# Start development environment with hot reload
docker compose -f docker-compose.dev.yml up

# Clean up when done
docker compose -f docker-compose.dev.yml down --volumes
```

### Production Deployment

```bash
# Build and run with Docker Compose
docker compose up -d

# Or build and run manually
docker build -t nedlia-backend .
docker run -p 8000:8000 \
  -e ENVIRONMENT=production \
  -e DB_HOST=your-db-host \
  nedlia-backend
```

## Docker Configuration

The project includes several Docker-related files:

- `Dockerfile`: Multi-stage build for production
- `docker-compose.yml`: Production orchestration
- `docker-compose.dev.yml`: Development environment with hot reload

Key features:
- Multi-stage builds for smaller images
- Poetry for dependency management
- Hot reload in development
- Production-ready Hypercorn configuration
- Proper security settings
- Environment variable management

## Development Tools

The project uses several development tools:

- **Black**: Code formatting
- **isort**: Import sorting
- **Pylint**: Code linting
- **Docker**: Containerization
- **Docker Compose**: Local development orchestration
- **VS Code**: Integrated development environment with custom launch configurations

## API Documentation

When running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
