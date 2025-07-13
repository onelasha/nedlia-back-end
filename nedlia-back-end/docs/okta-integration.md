# Okta Integration Guide

## Table of Contents
- [Overview](#overview)
- [Setup Steps](#setup-steps)
  - [1. Okta Developer Account](#1-okta-developer-account)
  - [2. Create API Service Application](#2-create-api-service-application)
  - [3. Configure CORS and Security](#3-configure-cors-and-security)
  - [4. Profile Schema](#4-profile-schema)
  - [5. Webhook Setup](#5-webhook-setup)
- [Integration Points](#integration-points)
  - [Token Validation](#token-validation)
  - [Profile Sync](#profile-sync)
  - [Webhook Handling](#webhook-handling)
- [Testing](#testing)
  - [Mock Server](#mock-server)
  - [Test Environment](#test-environment)
- [Troubleshooting](#troubleshooting)
  - [Common Issues](#common-issues)
  - [Monitoring](#monitoring)
- [Security Best Practices](#security-best-practices)
  - [Token Handling](#token-handling)
  - [API Security](#api-security)
  - [Data Protection](#data-protection)
- [Resources](#resources)

[← Back to Main Documentation](../README.md)

## Overview
This service integrates with Okta for identity and access management. Okta handles all authentication, while this service manages user profiles and preferences.

## Setup Steps

[↑ Back to top](#table-of-contents)

### 1. Okta Developer Account
1. Sign up at https://developer.okta.com/signup/
2. Note your Okta domain (e.g., `dev-123456.okta.com`)

### 2. Create API Service Application
1. In Okta Developer Console:
   - Applications > Create App Integration
   - Select "API Services"
   - Name: "Nedlia User Profile Service"
   - Grant type: Client Credentials

2. Note down:
   - Client ID
   - Client Secret
   - API Token (from API > Tokens)

### 3. Configure CORS and Security
1. Security > API:
   - Add your service URLs to trusted origins
   - Configure allowed redirect URIs
   - Set appropriate access policies

2. Configure scopes:
   - Authorization Servers
   - Add custom scopes if needed
   - Configure access policies

### 4. Profile Schema
1. Directory > Profile Editor:
   - Add custom attributes for your service
   - Map Okta user profile to your schema
   - Configure attribute access policies

### 5. Webhook Setup
1. Workflow > Event Hooks:
   - Add webhook endpoint
   - Select events to monitor:
     - `user.lifecycle.create`
     - `user.lifecycle.update`
     - `user.profile.update`

## Integration Points

[↑ Back to top](#table-of-contents)

### 1. Token Validation
```python
from okta.jwt import JWTVerifier

async def validate_token(token: str) -> dict:
    jwt_verifier = JWTVerifier(issuer=settings.okta.issuer, client_id=settings.okta.client_id)
    return await jwt_verifier.verify_access_token(token)
```

### 2. Profile Sync
```python
from okta.client import Client as OktaClient

async def sync_profile(okta_id: str) -> None:
    client = OktaClient(settings.okta)
    user = await client.get_user(okta_id)
    profile = map_okta_profile(user.profile)
    await update_local_profile(profile)
```

### 3. Webhook Handling
```python
@router.post("/webhooks/okta")
async def handle_okta_webhook(payload: OktaWebhookPayload):
    event_type = payload.eventType
    if event_type == "user.lifecycle.create":
        await create_profile(payload.data)
    elif event_type == "user.profile.update":
        await sync_profile(payload.data.id)
```

## Testing

[↑ Back to top](#table-of-contents)

### 1. Mock Server
For development and testing, use the provided Okta mock server:
```bash
poetry run okta-mock-server
```

### 2. Test Environment
Create a separate test application in Okta and use different credentials for testing:
```bash
# .env.test
OKTA_USE_MOCK=true
OKTA_ORG_URL="https://test-123456.okta.com"
OKTA_CLIENT_ID="test-client-id"
OKTA_CLIENT_SECRET="test-client-secret"
```

## Troubleshooting

[↑ Back to top](#table-of-contents)

### Common Issues
1. Token Validation Fails
   - Check issuer URL format
   - Verify client ID and secret
   - Check token expiration

2. Profile Sync Issues
   - Verify API token permissions
   - Check attribute mapping
   - Validate webhook signatures

3. Rate Limiting
   - Implement caching
   - Use bulk operations
   - Handle rate limit errors

### Monitoring
1. Enable Okta System Log monitoring
2. Set up alerts for authentication failures
3. Monitor webhook delivery status
4. Track profile sync errors

## Security Best Practices

[↑ Back to top](#table-of-contents)

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

## Resources

[↑ Back to top](#table-of-contents)

- [Okta Developer Documentation](https://developer.okta.com/docs/reference/)
- [API Services Guide](https://developer.okta.com/docs/guides/implement-oauth-for-okta/overview/)
- [Python SDK Reference](https://github.com/okta/okta-sdk-python)
- [JWT Validation Guide](https://developer.okta.com/docs/guides/validate-access-tokens/python/overview/)
