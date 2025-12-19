# cron_sync.py
import asyncio
from app.services.sync_engine import sync_user_content
from app.database import engine
from app.models import User
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

async def run_sync():
    """ Runs a single pass of the sync for all users. Perfect for Cron. """
    print("Starting Cron Sync Pass...")
    async with AsyncSession(engine) as session:
        statement = select(User.id)
        result = await session.execute(statement)
        user_ids = result.scalars().all()
    
    for uid in user_ids:
        try:
            await sync_user_content(uid)
        except Exception as e:
            print(f"Error syncing user {uid}: {e}")
    print("Cron Sync Pass Complete.")

if __name__ == "__main__":
    asyncio.run(run_sync())
