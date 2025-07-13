"""Okta webhook handlers."""

from fastapi import APIRouter, Request, HTTPException, Depends
from app.application.services.user_service import UserService
from app.infrastructure.auth.okta_client import OktaAuthClient
from app.domain.entities.user import User

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
okta_client = OktaAuthClient()

@router.post("/okta")
async def handle_okta_webhook(
    request: Request,
    user_service: UserService = Depends()
) -> dict:
    """Handle Okta webhook events."""
    # Verify Okta webhook signature
    auth_header = request.headers.get("Authorization")
    if not auth_header or not await okta_client.validate_token(auth_header.split(" ")[1]):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    payload = await request.json()
    event_type = payload.get("eventType")
    
    if not event_type:
        raise HTTPException(status_code=400, detail="Missing eventType")

    user_id = payload.get("target", {}).get("id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Missing user ID")

    try:
        if event_type == "user.lifecycle.create":
            # New user created in Okta
            okta_profile = await okta_client.get_user(user_id)
            if okta_profile:
                user = User(
                    id=user_id,
                    email=okta_profile.get("email"),
                    first_name=okta_profile.get("firstName"),
                    last_name=okta_profile.get("lastName"),
                    okta_id=user_id
                )
                await user_service.create_user(user)
                
        elif event_type == "user.lifecycle.delete":
            # User deleted in Okta
            await user_service.delete_user(user_id)
            
        elif event_type == "user.profile.update":
            # User profile updated in Okta
            okta_profile = await okta_client.get_user(user_id)
            if okta_profile:
                user = await user_service.get_user_by_okta_id(user_id)
                if user:
                    user.email = okta_profile.get("email", user.email)
                    user.first_name = okta_profile.get("firstName", user.first_name)
                    user.last_name = okta_profile.get("lastName", user.last_name)
                    await user_service.update_user(user)

        return {"status": "success", "event": event_type}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
