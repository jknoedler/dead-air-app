# backend/app/routers/oauth_router.py

from fastapi import APIRouter, Depends, Request, HTTPException
from starlette.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from datetime import datetime, timedelta
from ..database import get_session
from ..oauth_config import oauth
from ..models import User, UserPlatformToken
from ..dependencies import get_current_user

router = APIRouter()

@router.get("/{platform}/login")
async def oauth_login(platform: str, request: Request, current_user: User = Depends(get_current_user)):
    client = oauth.create_client(platform)
    if not client:
        raise HTTPException(status_code=400, detail="Invalid platform")
    
    # In production, use your actual deployment URL
    redirect_uri = f"http://localhost:8000/api/oauth/{platform}/callback"
    return await client.authorize_redirect(request, redirect_uri)

@router.get("/{platform}/callback")
async def oauth_callback(
    platform: str, 
    request: Request, 
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user) # Assumes user is already logged in with JWT
):
    client = oauth.create_client(platform)
    if not client:
        raise HTTPException(status_code=400, detail="Invalid platform")
    
    token = await client.authorize_access_token(request)
    if not token:
        raise HTTPException(status_code=400, detail="Failed to obtain access token")

    # Store or update the token in the DB
    statement = select(UserPlatformToken).where(
        UserPlatformToken.user_id == current_user.id,
        UserPlatformToken.platform == platform
    )
    result = await session.execute(statement)
    platform_token = result.scalar_one_or_none()
    
    expires_at = None
    if 'expires_in' in token:
        expires_at = datetime.utcnow() + timedelta(seconds=token['expires_in'])

    if platform_token:
        platform_token.access_token = token['access_token']
        platform_token.refresh_token = token.get('refresh_token', platform_token.refresh_token)
        platform_token.expires_at = expires_at
    else:
        platform_token = UserPlatformToken(
            user_id=current_user.id,
            platform=platform,
            access_token=token['access_token'],
            refresh_token=token.get('refresh_token'),
            expires_at=expires_at
        )
        session.add(platform_token)
    
    await session.commit()
    
    # Redirect back to frontend
    return RedirectResponse(url="http://localhost:5173/dashboard?status=success")
