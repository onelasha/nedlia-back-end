# Implementation Guide

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Core Components](#core-components)
- [Authentication Flow](#authentication-flow)
- [Data Models](#data-models)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)

[← Back to Main Documentation](../README.md)

## Overview
This service follows Clean Architecture and Domain-Driven Design principles, focusing on user profile management with Okta integration.

## Project Structure
```
app/
├── domain/                 # Domain layer
│   ├── entities/          # Domain entities
│   │   └── user.py       # User profile entity
│   ├── repositories/      # Repository interfaces
│   └── value_objects/     # Value objects
├── application/           # Application layer
│   ├── services/         # Application services
│   └── use_cases/        # Use cases
├── infrastructure/        # Infrastructure layer
│   ├── auth/             # Auth components
│   │   └── okta_client.py # Okta integration
│   ├── persistence/      # Database components
│   │   └── models/      # Database models
│   └── middleware/       # Middleware components
└── presentation/         # Presentation layer
    └── api/             # API endpoints
```

## Core Components

### 1. User Entity
```python
class User(BaseEntity):
    """User profile entity synchronized with Okta."""
    
    # Core fields
    email: EmailStr
    first_name: str
    last_name: str
    okta_id: str
    
    # Extended profile
    phone: Optional[str]
    avatar_url: Optional[str]
    locale: str
    timezone: str
    
    # Custom attributes
    preferences: Dict[str, Any]
    metadata: Dict[str, Any]
```

### 2. Okta Client
```python
class OktaAuthClient:
    """Okta authentication client."""
    
    async def get_user(self, user_id: str) -> Optional[dict]
    async def update_user(self, user_id: str, profile: dict) -> bool
    async def validate_token(self, token: str) -> Optional[dict]
```

### 3. Authentication Middleware
```python
class OktaAuthMiddleware(HTTPBearer):
    """Okta authentication middleware."""
    
    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]
```

## Authentication Flow

1. **Token Validation**
   ```mermaid
   sequenceDiagram
       Client->>API: Request with Bearer token
       API->>OktaAuthMiddleware: Validate token
       OktaAuthMiddleware->>Okta: Verify JWT
       Okta-->>OktaAuthMiddleware: Token claims
       OktaAuthMiddleware->>API: Inject user context
       API-->>Client: Response
   ```

2. **Profile Sync**
   ```mermaid
   sequenceDiagram
       Okta->>Webhook: Profile update event
       Webhook->>UserService: Update profile
       UserService->>MongoDB: Save changes
       MongoDB-->>Webhook: Success
       Webhook-->>Okta: 200 OK
   ```

## Data Models

### MongoDB User Model
```python
class UserModel(Document):
    """User profile model synchronized with Okta."""
    
    # Core fields
    email: Indexed(EmailStr, unique=True)
    first_name: str
    last_name: str
    okta_id: Indexed(str, unique=True)
    
    # Extended profile
    phone: Optional[str]
    avatar_url: Optional[str]
    locale: str
    timezone: str
    
    # Custom attributes
    preferences: Dict[str, Any]
    metadata: Dict[str, Any]
```

## API Endpoints

### Profile Management
```python
@router.get("/users/me")
async def get_current_user(
    user: User = Depends(get_current_user)
) -> UserResponse

@router.patch("/users/me")
async def update_current_user(
    data: UpdateUserRequest,
    user: User = Depends(get_current_user)
) -> UserResponse
```

### Webhooks
```python
@router.post("/webhooks/okta")
async def handle_okta_webhook(
    request: Request,
    user_service: UserService = Depends()
) -> dict
```

## Error Handling

### HTTP Exceptions
```python
class AuthenticationError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

class ProfileSyncError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=500,
            detail=f"Profile sync failed: {detail}",
        )
```

### Webhook Error Handling
```python
try:
    await sync_profile(user_id)
except Exception as e:
    logger.error(f"Profile sync failed: {e}")
    raise ProfileSyncError(str(e))
```

## Testing

### Unit Tests
```python
async def test_user_profile_sync():
    # Given
    user = User(...)
    okta_profile = {...}
    
    # When
    user.update_from_okta(okta_profile)
    
    # Then
    assert user.email == okta_profile["email"]
    assert user.first_name == okta_profile["firstName"]
```

### Integration Tests
```python
async def test_webhook_handler():
    # Given
    payload = {
        "eventType": "user.profile.update",
        "target": {"id": "user123"}
    }
    
    # When
    response = await client.post("/webhooks/okta", json=payload)
    
    # Then
    assert response.status_code == 200
    assert await UserModel.find_one({"okta_id": "user123"})
```

## Configuration

### Environment Variables
```bash
# Okta Settings
OKTA_ORG_URL="https://{yourOktaDomain}"
OKTA_CLIENT_ID="{yourClientId}"
OKTA_CLIENT_SECRET="{yourClientSecret}"
OKTA_API_TOKEN="{yourApiToken}"
OKTA_ISSUER="https://{yourOktaDomain}/oauth2/default"
OKTA_AUDIENCE="api://default"
```

### Feature Flags
```bash
# Feature Flags
PROFILE_SYNC_ENABLED=true
WEBHOOKS_ENABLED=true
```

## Monitoring

### Health Checks
```python
@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "okta": await check_okta_health(),
        "database": await check_db_health(),
    }
```

### Metrics
```python
PROFILE_SYNC_LATENCY = Histogram(
    "profile_sync_latency_seconds",
    "Time taken to sync user profile with Okta",
)

WEBHOOK_PROCESSING_TIME = Histogram(
    "webhook_processing_time_seconds",
    "Time taken to process Okta webhooks",
)
```

## Security Considerations

1. **Token Handling**
   - Never store tokens in code
   - Use secure environment variables
   - Implement token refresh logic

2. **API Security**
   - Use minimum required scopes
   - Implement rate limiting
   - Validate webhook signatures

3. **Data Protection**
   - Encrypt sensitive data
   - Implement attribute-level access control
   - Regular security audits
