"""Okta client implementation."""

from typing import Optional
from okta.client import Client as OktaClient
from app.infrastructure.config.settings import get_settings

settings = get_settings()

class OktaAuthClient:
    """Okta authentication client."""
    
    def __init__(self):
        self.client = OktaClient({
            'orgUrl': str(settings.okta.org_url),
            'token': settings.okta.api_token.get_secret_value(),
        })
        self.issuer = str(settings.okta.issuer)
        self.audience = settings.okta.audience

    async def get_user(self, user_id: str) -> Optional[dict]:
        """Get user from Okta."""
        try:
            user, resp = await self.client.get_user(user_id)
            if resp.status_code == 200:
                return user.profile
            return None
        except Exception:
            return None

    async def update_user(self, user_id: str, profile: dict) -> bool:
        """Update user in Okta."""
        try:
            user, resp = await self.client.get_user(user_id)
            if resp.status_code != 200:
                return False
            
            user.profile = {**user.profile, **profile}
            _, resp = await self.client.update_user(user)
            return resp.status_code == 200
        except Exception:
            return False

    async def validate_token(self, token: str) -> Optional[dict]:
        """Validate JWT token from Okta."""
        try:
            jwt = await self.client.jwt.validate_token(
                token,
                self.issuer,
                self.audience,
            )
            return jwt.claims if jwt else None
        except Exception:
            return None
