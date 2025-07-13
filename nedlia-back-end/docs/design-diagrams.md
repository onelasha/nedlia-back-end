# Design Diagrams

## Table of Contents
- [Architecture Overview](#architecture-overview)
- [Component Interactions](#component-interactions)
- [Authentication Flow](#authentication-flow)
- [Profile Sync Flow](#profile-sync-flow)
- [Data Model](#data-model)
- [Error Handling Flow](#error-handling-flow)

[← Back to Main Documentation](../README.md)

## Architecture Overview

```mermaid
graph TB
    subgraph Client Applications
        WebApp[Web Application]
        MobileApp[Mobile Application]
    end

    subgraph API Layer
        API[FastAPI Service]
        Auth[Auth Middleware]
        Routes[API Routes]
    end

    subgraph Application Layer
        Services[Application Services]
        UseCases[Use Cases]
    end

    subgraph Domain Layer
        Entities[Domain Entities]
        Repos[Repository Interfaces]
        ValueObjects[Value Objects]
    end

    subgraph Infrastructure Layer
        OktaClient[Okta Client]
        MongoDB[(MongoDB)]
        Redis[(Redis Cache)]
    end

    WebApp & MobileApp --> API
    API --> Auth
    Auth --> Routes
    Routes --> Services
    Services --> UseCases
    UseCases --> Entities
    UseCases --> Repos
    Entities --> ValueObjects
    OktaClient --> Auth
    MongoDB --> Repos
    Redis --> Services
```

## Component Interactions

```mermaid
sequenceDiagram
    participant Client
    participant API as API Gateway
    participant Auth as Auth Middleware
    participant Service as User Service
    participant Okta
    participant DB as MongoDB

    Client->>API: Request with JWT
    API->>Auth: Validate Token
    Auth->>Okta: Verify Token
    Okta-->>Auth: Token Claims
    Auth->>Service: Get User Profile
    Service->>DB: Query User
    DB-->>Service: User Data
    Service-->>API: User Profile
    API-->>Client: Response
```

## Authentication Flow

```mermaid
stateDiagram-v2
    [*] --> RequestReceived
    RequestReceived --> TokenExtraction: Extract Bearer Token
    TokenExtraction --> TokenValidation: Validate with Okta
    TokenValidation --> UserContext: Valid Token
    TokenValidation --> Unauthorized: Invalid Token
    UserContext --> RequestProcessing: Inject User Info
    RequestProcessing --> [*]: Complete Request
    Unauthorized --> [*]: Return 401
```

## Profile Sync Flow

```mermaid
sequenceDiagram
    participant Okta
    participant Webhook
    participant Service as User Service
    participant Cache as Redis Cache
    participant DB as MongoDB

    Okta->>Webhook: Profile Update Event
    activate Webhook
    Webhook->>Service: Process Event
    Service->>DB: Get Current Profile
    DB-->>Service: Profile Data
    Service->>Okta: Get Updated Profile
    Okta-->>Service: Okta Profile
    Service->>DB: Update Profile
    Service->>Cache: Invalidate Cache
    Webhook-->>Okta: 200 OK
    deactivate Webhook
```

## Data Model

```mermaid
classDiagram
    class User {
        +String id
        +String email
        +String first_name
        +String last_name
        +String okta_id
        +Boolean is_active
        +DateTime last_sync
        +String phone
        +String avatar_url
        +String locale
        +String timezone
        +Dict preferences
        +Dict metadata
        +DateTime created_at
        +DateTime updated_at
        +update_from_okta()
        +to_okta_profile()
    }

    class UserModel {
        +String id
        +String email
        +String first_name
        +String last_name
        +String okta_id
        +Boolean is_active
        +DateTime last_sync
        +String phone
        +String avatar_url
        +String locale
        +String timezone
        +Dict preferences
        +Dict metadata
        +DateTime created_at
        +DateTime updated_at
        +to_entity()
        +from_entity()
    }

    class OktaProfile {
        +String id
        +String email
        +String firstName
        +String lastName
        +String mobilePhone
        +String locale
        +String timezone
        +Dict customAttributes
    }

    User --|> UserModel : maps to
    User --|> OktaProfile : syncs with
```

## Error Handling Flow

```mermaid
stateDiagram-v2
    [*] --> RequestProcessing
    RequestProcessing --> Success: Try
    RequestProcessing --> ErrorHandling: Catch
    
    state ErrorHandling {
        [*] --> AuthError
        [*] --> ValidationError
        [*] --> BusinessError
        [*] --> TechnicalError
        
        AuthError --> Return401
        ValidationError --> Return400
        BusinessError --> Return422
        TechnicalError --> Return500
    }
    
    Success --> [*]: 200 OK
    Return401 --> [*]: 401 Unauthorized
    Return400 --> [*]: 400 Bad Request
    Return422 --> [*]: 422 Unprocessable
    Return500 --> [*]: 500 Server Error
```

## System Context

```mermaid
C4Context
    title System Context Diagram
    
    Enterprise_Boundary(b0, "Enterprise") {
        Person(client, "Client", "Application user accessing the system")
        
        System_Boundary(b1, "User Profile Service") {
            Container(api, "API Service", "FastAPI", "Handles user profile management")
            ContainerDb(db, "Database", "MongoDB", "Stores user profiles")
            ContainerDb(cache, "Cache", "Redis", "Caches user data")
        }
        
        System_Ext(okta, "Okta", "Identity provider")
    }
    
    Rel(client, api, "Uses", "HTTPS/REST")
    Rel(api, okta, "Authenticates", "HTTPS/OAuth2")
    Rel(api, db, "Reads/Writes")
    Rel(api, cache, "Caches")
    Rel(okta, api, "Webhooks", "HTTPS/REST")

    UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```

## Deployment Architecture

```mermaid
graph TB
    subgraph Cloud Platform
        subgraph Container Registry
            Images[Docker Images]
        end
        
        subgraph Kubernetes Cluster
            subgraph API Pod
                Service[API Service]
                Cache[Redis Sidecar]
            end
            
            subgraph Database
                Primary[(MongoDB Primary)]
                Secondary1[(MongoDB Secondary)]
                Secondary2[(MongoDB Secondary)]
            end
            
            subgraph Ingress
                LB[Load Balancer]
                SSL[SSL Termination]
            end
        end
        
        subgraph Monitoring
            Prometheus[Prometheus]
            Grafana[Grafana Dashboard]
        end
    end
    
    subgraph External Services
        Okta[Okta IdP]
    end
    
    Client-->LB
    LB-->SSL
    SSL-->Service
    Service-->Cache
    Service-->Primary
    Primary-->Secondary1
    Primary-->Secondary2
    Service-->Okta
    Service-->Prometheus
    Prometheus-->Grafana
```

## Sequence Flows

### User Profile Update

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Service
    participant Cache
    participant DB
    participant Okta
    
    Client->>API: PATCH /users/me
    activate API
    
    API->>Service: Update Profile
    activate Service
    
    Service->>DB: Get Current Profile
    DB-->>Service: Profile Data
    
    Service->>Okta: Update Okta Profile
    Okta-->>Service: Success
    
    Service->>DB: Save Updated Profile
    DB-->>Service: Success
    
    Service->>Cache: Invalidate Cache
    Cache-->>Service: Success
    
    Service-->>API: Updated Profile
    deactivate Service
    
    API-->>Client: 200 OK
    deactivate API
```

### Webhook Processing

```mermaid
sequenceDiagram
    participant Okta
    participant Webhook
    participant Queue
    participant Worker
    participant DB
    participant Cache
    
    Okta->>Webhook: Profile Event
    activate Webhook
    
    Webhook->>Queue: Enqueue Event
    Queue-->>Webhook: Success
    Webhook-->>Okta: 202 Accepted
    deactivate Webhook
    
    Queue->>Worker: Process Event
    activate Worker
    
    Worker->>DB: Update Profile
    DB-->>Worker: Success
    
    Worker->>Cache: Invalidate
    Cache-->>Worker: Success
    
    Worker-->>Queue: Complete
    deactivate Worker
```
