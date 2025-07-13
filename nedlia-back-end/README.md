# Nedlia User Profile Service

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
  - [Clean Architecture](#clean-architecture)
  - [Domain-Driven Design](#domain-driven-design)
  - [Infrastructure](#infrastructure)
- [Features](#features)
  - [Core Features](#core-features)
  - [Technical Features](#technical-features)
- [Security & Integration](#security--integration)
  - [Okta Integration](#okta-integration)
  - [Profile Sync](#profile-sync)
  - [Data Protection](#data-protection)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development Setup](#local-development-setup)
  - [Docker Setup](#docker-setup)
- [Development](#development)
  - [Code Style](#code-style)
  - [Git Workflow](#git-workflow)
  - [Documentation](#documentation)
- [Testing](#testing)
  - [Unit Tests](#unit-tests)
  - [Integration Tests](#integration-tests)
  - [E2E Tests](#e2e-tests)
- [Deployment](#deployment)
  - [Docker Deployment](#docker-deployment)
  - [Cloud Deployment](#cloud-deployment)
- [Monitoring](#monitoring)
  - [Health Checks](#health-checks)
  - [Metrics](#metrics)
  - [Logging](#logging)
- [Additional Documentation](#additional-documentation)
  - [Implementation Guide](docs/implementation.md)
  - [API Documentation](#api-documentation)
  - [Architecture Guide](#architecture-guide)
  - [Okta Integration Guide](docs/okta-integration.md)

## Overview
A domain-centric microservice responsible for user profile management within the Nedlia ecosystem, integrated with Okta for identity and access management. Built with Python, FastAPI, and MongoDB, following Domain-Driven Design principles and Clean Architecture. This service is part of the Nedlia platform's bounded context for user profiles and preferences.

## 🏗️ Domain & Architecture

### Domain Context
This microservice operates within the User Profile bounded context of the Nedlia platform, responsible for:
- User profile data management
- User preferences and settings
- Profile verification and status
- Integration with Okta identity service

### Domain Model
- **User Profile Aggregate**
  - UserProfile Entity (root)
  - OktaId Value Object
  - ProfileStatus Value Object
  - ContactInfo Value Object
  - Preferences Value Object

- **Domain Events**
  - ProfileCreated
  - ProfileUpdated
  - PreferencesChanged
  - ProfileVerified

- **Domain Services**
  - OktaIntegrationService
  - ProfileVerificationService
  - PreferencesManagementService

### Architecture Layers

```
nedlia-back-end/
├── app/
│   ├── domain/              # Enterprise business rules and entities
│   │   ├── entities/        # Core business objects
│   │   ├── value_objects/   # Immutable value objects
│   │   ├── repositories/    # Abstract repository interfaces
│   │   └── exceptions/      # Domain-specific exceptions
│   │
│   ├── application/         # Application-specific business rules
│   │   ├── services/        # Business logic orchestration
│   │   └── dtos/           # Data Transfer Objects
│   │
│   ├── infrastructure/      # External frameworks and tools
│   │   ├── config/         # Application configuration
│   │   ├── persistence/    # MongoDB implementations
│   │   ├── logging/        # Logging configuration
│   │   ├── middleware/     # FastAPI middleware
│   │   └── errors/         # Error handlers
│   │
│   └── presentation/        # Interface adapters
│       └── api/            # API endpoints and routes
│
├── tests/                  # Test suites
├── pyproject.toml         # Project dependencies
└── .env.example          # Environment configuration template
```

### Domain Layer
- Core user management business logic
- Framework and infrastructure independent
- Pure Python with minimal external dependencies
- Components:
  - **UserProfile Entity**
    - Profile data management
    - Okta ID association
    - Profile verification status
    - Preferences management
  - **Value Objects**
    - OktaId (external identity)
    - ContactInfo (email, phone)
    - Preferences (user settings)
    - ProfileStatus (state machine)
  - **Repository Interface**
    - ProfileRepository (persistence contract)
    - ProfileSearchCriteria (query specs)
  - **Domain Events**
    - Profile lifecycle events
    - Preferences change events
  - **Domain Exceptions**
    - ProfileNotFoundError
    - InvalidProfileDataError
    - DuplicateProfileError
    - OktaIntegrationError

### Application Layer
- Profile management use cases
- Okta integration flows
- Preferences management
- Components:
  - **Use Cases**
    - CreateUserProfile
    - UpdateProfile
    - ManagePreferences
    - VerifyProfile
    - SyncWithOkta
    - QueryProfiles
  - **DTOs**
    - ProfileCreationDto
    - ProfileUpdateDto
    - PreferencesDto
    - OktaUserDto
  - **Event Handlers**
    - OktaUserCreatedHandler
    - ProfileUpdatedHandler
    - PreferencesChangedHandler

### Infrastructure Layer
- Technical implementations and external integrations
- Implements interfaces defined in domain layer
- Components:
  - **Persistence**: MongoDB implementation
    - Beanie ODM models
    - Repository implementations
    - Connection management
  - **Configuration**: Application settings
    - Environment-based config
    - Dependency injection setup
  - **Logging**: Structured logging
    - JSON format
    - Correlation IDs
    - Log levels
  - **Middleware**: Request processing
    - Authentication
    - Request logging
    - Metrics collection
  - **Error Handling**: HTTP error responses
    - Domain exception mapping
    - Consistent error format

### Presentation Layer
- API interface and request handling
- FastAPI routes and endpoints
- Components:
  - **API Routes**: Endpoint definitions
    - Resource-based organization
    - OpenAPI documentation
    - Response models
  - **Middleware**: Request processing
    - CORS handling
    - Authentication
    - Rate limiting
  - **Health Checks**: System status
    - Database connectivity
    - Dependencies status
  - **API Versioning**: v1 structure

## 🚀 Service Capabilities

### Core Domain Features
- **Profile Management**
  - Profile creation and updates
  - Preferences management
  - Profile verification
  - Status tracking
  - Bulk profile operations

- **Okta Integration**
  - Okta webhook handling
  - User profile sync
  - JWT token validation
  - SSO support

- **Integration**
  - REST API for other services
  - Event publishing
  - Webhook notifications
  - Health and status checks

### Technical Features
- **Clean Architecture**
  - Strict separation of concerns
  - Domain-centric design
  - Framework independence
  - High testability
  - Maintainable codebase

- **Domain-Driven Design**
  - Rich domain models
  - Bounded contexts
  - Value objects
  - Repository pattern
  - Domain events

### Technology Stack
- **FastAPI Framework**
  - High performance async
  - Type hints throughout
  - OpenAPI/Swagger docs
  - Dependency injection
  - Pydantic validation

- **MongoDB 8.0**
  - Async driver (Motor)
  - Beanie ODM
  - Connection pooling
  - Document-based model
  - Schemaless flexibility

- **Redis Integration**
  - Session management
  - Rate limiting
  - Cache layer
  - Pub/Sub capability

### Observability & Monitoring
- **Logging**
  - Structured JSON format
  - Request correlation IDs
  - Log levels by environment
  - Contextual logging

- **Metrics**
  - Prometheus integration
  - Request metrics
  - Business metrics
  - Custom metrics support

- **Health Checks**
  - Database connectivity
  - Redis connectivity
  - System resources
  - Dependencies status

### 🔐 Security & Integration

### Okta Integration
- **Authentication Flow**
  - Okta handles user authentication
  - JWT token validation
  - SSO support
  - Token refresh handling

### Okta Setup
1. **Create Okta Application**
   ```bash
   # Register your application in Okta Developer Console
   # 1. Applications > Create App Integration
   # 2. Select: API Services
   # 3. Configure settings
   ```

2. **Configure Okta Settings**
   ```bash
   # In your .env file
   OKTA_ORG_URL="https://{yourOktaDomain}"
   OKTA_CLIENT_ID="{yourClientId}"
   OKTA_CLIENT_SECRET="{yourClientSecret}"
   OKTA_API_TOKEN="{yourApiToken}"
   OKTA_ISSUER="https://{yourOktaDomain}/oauth2/default"
   ```

3. **Configure CORS & Redirect URIs**
   - Add your service URL to Okta's trusted origins
   - Configure allowed redirect URIs
   - Set up CORS policies in your service

### Profile Sync
- **Automatic Sync**
  - Profile updates from Okta
  - Custom attribute mapping
  - Webhook event handling

### Data Protection
- JWT validation
- Input validation
- CORS policies
- Rate limiting

### Developer Experience
- **Dependency Management**
  - Poetry
  - Lock file
  - Virtual environments
  - Development groups

- **Code Quality**
  - Type checking (mypy)
  - Linting (flake8)
  - Formatting (black)
  - Import sorting (isort)

- **Testing**
  - Unit tests
  - Integration tests
  - Async test support
  - Fixtures and factories

## 🛠️ Technical Stack

### Core Technologies
- **Language**: Python ^3.11
- **Web Framework**: FastAPI ^0.104.0
- **ASGI Server**: Uvicorn ^0.23.2

### Data Layer
- **Database**: MongoDB 8.0
- **ODM**: Beanie ^1.23.0
- **Driver**: Motor ^3.3.1
- **Caching**: Redis ^5.0.1

### Security
- **Okta SDK**: okta-sdk-python
- **JWT Validation**: python-jose[cryptography]
- **Form Parsing**: python-multipart

### Observability
- **Logging**: structlog ^23.2.0
- **Metrics**: prometheus-client ^0.17.1

### Development Tools
- **Dependency Management**: Poetry
- **Type Checking**: mypy
- **Linting**: flake8
- **Formatting**: black
- **Import Sorting**: isort
- **Testing**: pytest
- **Documentation**: OpenAPI/Swagger

## 🚦 Getting Started

### Prerequisites

#### Required
- Python 3.11 or higher
- Poetry package manager
- MongoDB 8.0 or higher
- Git
- Okta Developer Account

#### Optional
- Redis 5.0 or higher (for caching)
- Docker & Docker Compose (for containerization)
- Make (for development scripts)

#### Okta Setup
1. Create a free Okta Developer Account at https://developer.okta.com/signup/
2. Create an API Services application in Okta
3. Note down your:
   - Okta Domain
   - Client ID
   - Client Secret
   - API Token

### Local Development Setup

1. **Clone the Repository**
```bash
git clone https://github.com/onelasha/nedlia-back-end.git
cd nedlia-back-end
```

2. **Install Dependencies**
```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install project dependencies
poetry install
```

3. **Configure Environment**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# Required variables:
# - DB_URL: MongoDB connection string
# - DB_NAME: Database name
# - OKTA_ORG_URL: Your Okta organization URL
# - OKTA_CLIENT_ID: Your Okta client ID
# - OKTA_CLIENT_SECRET: Your Okta client secret
# - OKTA_API_TOKEN: Your Okta API token
```

4. **Start Required Services**
```bash
# Start MongoDB (choose one method)

# Using Docker:
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=secret \
  mongo:8.0

# Or local installation:
mongod --dbpath /path/to/data/db

# Start Redis (optional, for caching)
docker run -d \
  --name redis \
  -p 6379:6379 \
  redis:5.0
```

5. **Start Development Server**
```bash
# Start with hot reload
poetry run uvicorn app.presentation.api.v1.main:app --reload --host 0.0.0.0 --port 8000

# Or using the development script
poetry run dev
```

### Docker Deployment

1. **Build Application Image**
```bash
# Build with current architecture
docker build -t nedlia-backend:latest .

# Or multi-platform build
docker buildx build --platform linux/amd64,linux/arm64 -t nedlia-backend:latest .
```

2. **Run with Docker Compose**
```bash
# Start all services
docker-compose up -d

# Or run individually
docker run -d \
  --name nedlia-api \
  -p 8000:8000 \
  -e DB_URL=mongodb://mongodb:27017 \
  -e DB_NAME=nedlia \
  -e REDIS_URL=redis://redis:6379 \
  -e SECURITY_SECRET_KEY=your-secret-key \
  --network nedlia-network \
  nedlia-backend:latest
```

### Verify Installation

1. **Check API Status**
```bash
curl http://localhost:8000/api/v1/health
```

2. **Access Documentation**
- OpenAPI UI: http://localhost:8000/docs
- ReDoc UI: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

3. **Monitor Metrics**
```bash
curl http://localhost:8000/metrics
```

## 🏗️ Project Structure

```
nedlia-back-end/
├── app/
│   ├── domain/
│   │   ├── entities/         # Domain entities
│   │   ├── value_objects/    # Value objects
│   │   ├── repositories/     # Repository interfaces
│   │   ├── services/        # Domain services
│   │   ├── events/          # Domain events
│   │   └── exceptions/      # Domain exceptions
│   │
│   ├── application/
│   │   ├── services/        # Application services
│   │   ├── interfaces/      # Port interfaces
│   │   ├── use_cases/      # Use case implementations
│   │   └── dtos/           # Data Transfer Objects
│   │
│   ├── infrastructure/
│   │   ├── config/         # Configuration
│   │   ├── persistence/    # Database implementations
│   │   ├── messaging/      # Message queue
│   │   ├── logging/        # Logging setup
│   │   └── middleware/     # Middleware components
│   │
│   └── presentation/
│       └── api/
│           └── v1/         # API v1 endpoints
│
├── tests/
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── e2e/              # End-to-end tests
│
├── migrations/            # Alembic migrations
├── infrastructure/        # Infrastructure as Code
│   ├── docker/           # Docker configurations
│   └── terraform/        # Terraform configurations
│
├── pyproject.toml        # Project dependencies
├── README.md            # Project documentation
└── .env.example         # Environment variables template
```

## 🔍 Implementation Details

### Domain Layer

#### Entities
- Base entity with common attributes (ID, timestamps)
- Rich domain model with business logic
- Example: User entity with email, password, and status

#### Value Objects
- Immutable objects defined by their attributes
- Validation on creation
- Examples: Email, Password, PhoneNumber

#### Repositories
- Interface definitions for data access
- Abstract base repository with common operations
- Specific repositories for each entity

### Application Layer

#### Services
- Orchestrate domain objects
- Implement use cases
- Handle business operations
- Example: UserService for user management

#### DTOs
- Define data transfer contracts
- Input/Output models
- Validation rules

### Infrastructure Layer

#### Database
- Async SQLAlchemy setup
- Connection pooling
- Repository implementations
- Migration management

#### Middleware
- Request logging
- Metrics collection
- Error handling
- Authentication

### Presentation Layer

#### API Routes
- RESTful endpoints
- OpenAPI documentation
- Input validation
- Error handling
- Authentication/Authorization

## 📊 Monitoring and Observability

### Logging
- Structured JSON logging
- Request correlation IDs
- Log levels configuration
- Contextual information

### Metrics
- Request counts
- Response times
- Error rates
- Database connection pool stats

### Health Checks
- Application status
- Database connectivity
- Dependencies status

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- Rate limiting
- CORS configuration
- Input validation
- SQL injection protection

## 🧪 Testing

### Configure Test Environment
1. Create a separate Okta test application
2. Set up test environment variables:
```bash
# .env.test
OKTA_ORG_URL="https://{yourTestOktaDomain}"
OKTA_CLIENT_ID="{yourTestClientId}"
OKTA_CLIENT_SECRET="{yourTestClientSecret}"
OKTA_API_TOKEN="{yourTestApiToken}"
```

### Unit Tests
```bash
poetry run pytest tests/unit
```

### Integration Tests
```bash
# Tests with Okta integration
poetry run pytest tests/integration
```

### E2E Tests
```bash
# Full flow tests including Okta auth
poetry run pytest tests/e2e
```

### Mock Okta for Development
```bash
# Use the provided Okta mock server
poetry run okta-mock-server

# Or use environment variable
OKTA_USE_MOCK=true poetry run dev
```

## 📚 Documentation

- OpenAPI/Swagger UI at `/docs`
- API documentation
- Code documentation
- Architecture documentation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
