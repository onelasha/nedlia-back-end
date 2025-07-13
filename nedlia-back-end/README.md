# Nedlia Backend API

A modern, enterprise-grade Python microservice built with FastAPI, following Clean Architecture and Domain-Driven Design principles.

## 🏗️ Architecture Overview

This project implements Clean Architecture with DDD principles, organizing code into distinct layers:

```
app/
├── domain/          # Enterprise business rules and entities
├── application/     # Application-specific business rules
├── infrastructure/  # External frameworks and tools
└── presentation/    # Interface adapters (API endpoints)
```

### Domain Layer (Inside)
- Contains enterprise-wide business rules
- Pure Python with no external dependencies
- Includes:
  - Entities (core business objects)
  - Value Objects (immutable objects defined by attributes)
  - Repository Interfaces (data access contracts)
  - Domain Services (complex business operations)
  - Domain Events (business occurrences)
  - Domain Exceptions (business rule violations)

### Application Layer
- Contains application-specific business rules
- Orchestrates the flow of data and domain objects
- Implements use cases
- Includes:
  - Services (orchestration of domain objects)
  - DTOs (data transfer objects)
  - Interface Adapters
  - Command/Query handlers

### Infrastructure Layer
- Contains technical capabilities and tools
- Implements interfaces defined in domain layer
- Includes:
  - Database implementations
  - External services integration
  - Message queues
  - File systems
  - Framework configurations

### Presentation Layer
- Contains API endpoints and controllers
- Handles HTTP requests/responses
- Includes:
  - REST API routes
  - Request/Response models
  - Authentication/Authorization
  - Input validation

## 🚀 Key Features

- **Clean Architecture**
  - Clear separation of concerns
  - Domain-centric design
  - Framework independence
  - Highly testable

- **Domain-Driven Design**
  - Rich domain model
  - Encapsulated business logic
  - Value objects for immutability
  - Domain events for decoupling

- **Modern FastAPI Setup**
  - Async/await support
  - OpenAPI documentation
  - Type hints throughout
  - Dependency injection

- **Database**
  - MongoDB 8.0 with Motor and Beanie ODM
  - Async connection pooling
  - Repository pattern
  - Document-based data model

- **Observability**
  - Structured JSON logging
  - Request correlation IDs
  - Prometheus metrics
  - Health check endpoints

- **Security**
  - CORS configuration
  - JWT authentication
  - Password hashing
  - Rate limiting

- **Developer Experience**
  - Poetry for dependency management
  - Type checking with mypy
  - Code formatting with black
  - Import sorting with isort
  - Pre-commit hooks

## 🛠️ Technical Stack

- **Python**: ^3.11
- **Web Framework**: FastAPI
- **Database**: MongoDB 8.0
- **ODM**: Beanie (Motor/PyMongo)
- **Caching**: Redis
- **Dependency Management**: Poetry
- **Testing**: pytest
- **Logging**: structlog
- **Metrics**: Prometheus
- **Documentation**: OpenAPI/Swagger

## 🚦 Getting Started

### Prerequisites

- Python 3.11+
- Poetry
- MongoDB 8.0+
- Redis (optional)
- Docker (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-org/nedlia-back-end.git
cd nedlia-back-end
```

2. Install dependencies:
```bash
poetry install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run database migrations:
```bash
poetry run alembic upgrade head
```

5. Start the development server:
```bash
poetry run dev
```

### Docker Deployment

1. Build the image:
```bash
docker build -t nedlia-backend .
```

2. Run the container:
```bash
docker run -d -p 8000:8000 \
  -e DB_URL=postgresql://user:pass@host/db \
  -e REDIS_URL=redis://redis:6379 \
  nedlia-backend
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

### Unit Tests
- Domain logic testing
- Service layer testing
- Mocked dependencies

### Integration Tests
- Repository testing
- API endpoint testing
- Database integration

### E2E Tests
- Full application testing
- API contract testing
- Performance testing

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
