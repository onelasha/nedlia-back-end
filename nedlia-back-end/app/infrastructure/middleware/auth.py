"""Authentication middleware."""

from typing import Optional
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.infrastructure.auth.okta_client import OktaAuthClient

class OktaAuthMiddleware(HTTPBearer):
    """Okta authentication middleware."""

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.auth_client = OktaAuthClient()

    async def __call__(self, request: Request) -> Optional[HTTPAuthorizationCredentials]:
        """Validate token and inject user info."""
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if not credentials:
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None

        token = credentials.credentials
        claims = await self.auth_client.validate_token(token)
        
        if not claims:
            if self.auto_error:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token or expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None

        # Inject user info into request state
        request.state.user = claims
        request.state.user_id = claims.get("sub")
        request.state.scopes = claims.get("scp", [])
        
        return credentials
