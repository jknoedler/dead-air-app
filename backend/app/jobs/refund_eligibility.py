# backend/app/jobs/refund_eligibility.py

from datetime import datetime, timedelta
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import engine
from ..models import DailyActivity

async def check_refund_eligibility():
    """
    Nightly job that runs at midnight.
    Checks if users posted in the last 24 hours.
    If not, marks 'eligible_for_refund' as False.
    """
    print("Running tonight's refund eligibility check...")
    async with AsyncSession(engine) as session:
        # Get yesterday's date
        yesterday = datetime.utcnow().date() - timedelta(days=1)
        yesterday_dt = datetime.combine(yesterday, datetime.min.time())
        
        # This is a simplified check.
        # In real world, we'd check the streak for all active users.
        statement = select(DailyActivity).where(DailyActivity.date == yesterday_dt)
        result = await session.execute(statement)
        activities = result.scalars().all()
        
        for activity in activities:
            if not activity.posted:
                activity.eligible_for_refund = False
        
        await session.commit()
    print("Refund eligibility check complete.")
