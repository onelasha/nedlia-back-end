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
- MongoDB (for data storage)

## Installation

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

## Running the Application

### Development Mode

```bash
# Activate the poetry shell
poetry shell

# Run the application
poetry run python -m app

# Or use hypercorn directly with auto-reload
poetry run hypercorn app.main:app --reload --bind 0.0.0.0:8000
```

### Production Mode

```bash
# Using Docker
docker build -t nedlia-backend .
docker run -p 8000:8000 nedlia-backend

# Or using poetry in production mode
ENVIRONMENT=production poetry run python -m app
```

## Development Tools

The project uses several development tools:

- **Black**: Code formatting
- **isort**: Import sorting
- **Pylint**: Code linting
- **Flake8**: Style guide enforcement
- **Pytest**: Testing framework

Run the tools:
```bash
# Format code
poetry run black .
poetry run isort .

# Lint code
poetry run pylint app
poetry run flake8 app

# Run tests
poetry run pytest
```

## Testing

```bash
# Run all tests
poetry run pytest

# Run tests with coverage report
poetry run pytest --cov=app

# Generate HTML coverage report
poetry run pytest --cov=app --cov-report=html
```

View the coverage report by opening `htmlcov/index.html` in your browser.

## API Documentation

Once the application is running, you can access:
- API documentation: http://localhost:8000/docs
- Alternative API documentation: http://localhost:8000/redoc
- Health check: http://localhost:8000/v1/health

## License

This project is licensed under the terms of the MIT license.
