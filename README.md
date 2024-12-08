[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=onelasha_nedlia-back-end&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=onelasha_nedlia-back-end)
# nedlia-back-end
Nedlia Back end
Updating one

1. First, create your local environment file. You can do this manually:

```commandline
# Create a .env file in the project root with your development settings
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


2. Then you can run the application in several ways:
```commandline
# Method 1: Using the start script (recommended)
./scripts/start.sh development

# Method 2: Direct Python execution
python -m app

# Method 3: Using uvicorn directly (for development with auto-reload)
uvicorn app.main:app --reload --port 8000
```


3. To switch environments:
```commandline
# For testing
./scripts/start.sh testing

# For production
./scripts/start.sh production
```

4. To verify it's working:
```commandline
# Check the health endpoint
curl http://localhost:8000/v1/health

# Check feature flags
curl http://localhost:8000/v1/features/status/sample-feature-state
```

5. Running Tests:
```commandline
# Install test dependencies
pip install -r requirements/test.txt

# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app

# Run tests verbosely (shows more details)
pytest -v

# Run a specific test file
pytest tests/test_main.py

# Run tests and generate HTML coverage report
pytest --cov=app --cov-report=html
```

After running tests with coverage, you can find the HTML report in the `htmlcov` directory.
Open `htmlcov/index.html` in your browser to view the detailed coverage report.