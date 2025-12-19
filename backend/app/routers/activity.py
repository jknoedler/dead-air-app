from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from ..database import get_session
from ..models import Post, User
from ..dependencies import get_current_user

router = APIRouter()

@router.get("/sync-status")
async def get_sync_status(
    current_user: User = Depends(get_current_user), 
    session: AsyncSession = Depends(get_session)
):
    statement = select(Post).where(Post.user_id == current_user.id).order_by(Post.posted_at.desc()).limit(10)
    result = await session.execute(statement)
    posts = result.scalars().all()
    return posts
