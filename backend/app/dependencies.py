# backend/dependencies.py

from fastapi import Depends, HTTPException, status
# Placeholder for actual authentication logic

async def get_current_user():
    # TODO: implement JWT verification and retrieve user from DB
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
