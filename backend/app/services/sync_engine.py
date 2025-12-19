import asyncio
import os
from datetime import datetime, timedelta
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import engine, get_session
from ..models import User, UserPlatformToken, Post, DailyActivity
from .tiktok import TikTokService
from .youtube import YouTubeService

# Initialize services (typically you'd pass config here)
tiktok_service = TikTokService(os.getenv("TIKTOK_CLIENT_KEY"), os.getenv("TIKTOK_CLIENT_SECRET"))
youtube_service = YouTubeService(os.getenv("YOUTUBE_CLIENT_ID"), os.getenv("YOUTUBE_CLIENT_SECRET"))

async def sync_user_content(user_id: int):
    async with AsyncSession(engine) as session:
        # 1. Get TikTok token
        statement = select(UserPlatformToken).where(
            UserPlatformToken.user_id == user_id,
            UserPlatformToken.platform == "tiktok"
        )
        result = await session.execute(statement)
        tiktok_token = result.scalar_one_or_none()
        
        if not tiktok_token:
            return

        # 2. Poll TikTok for latest video
        # In real world, we'd use tiktok_token.access_token and open_id
        video_data = await tiktok_service.get_latest_video("open_id_placeholder", tiktok_token.access_token)
        if not video_data:
            return

        video_id = video_data.get("id")
        
        # 3. Check if we already synced this
        check_stmt = select(Post).where(Post.user_id == user_id, Post.platform_post_id == video_id)
        check_res = await session.execute(check_stmt)
        if check_res.scalar_one_or_none():
            return # Already synced

        # 4. Sync to other platforms
        video_path = await tiktok_service.download_video_no_watermark(video_data)
        caption = video_data.get("title", "Check out my new TikTok!")

        # Async distribution
        # In a real app, you'd iterate over all platforms the user has connected
        yt_stmt = select(UserPlatformToken).where(
            UserPlatformToken.user_id == user_id,
            UserPlatformToken.platform == "youtube"
        )
        yt_res = await session.execute(yt_stmt)
        yt_token = yt_res.scalar_one_or_none()

        if yt_token:
            yt_post_id = await youtube_service.upload_video(video_path, caption, yt_token.access_token)
            
            # Record the cross-post
            new_post = Post(
                user_id=user_id,
                platform="youtube",
                platform_post_id=yt_post_id
            )
            session.add(new_post)
            
            # Mark daily activity
            today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            act_stmt = select(DailyActivity).where(DailyActivity.user_id == user_id, DailyActivity.date == today)
            act_res = await session.execute(act_stmt)
            activity = act_res.scalar_one_or_none()
            
            if not activity:
                activity = DailyActivity(user_id=user_id, date=today, opened=True, posted=True)
                session.add(activity)
            else:
                activity.posted = True
            
            await session.commit()
            print(f"Successfully synced video {video_id} to YouTube for user {user_id}")

class SyncManager:
    def __init__(self):
        self.running = False

    async def start(self):
        self.running = True
        print("Sync Engine started...")
        while self.running:
            # Iterate over all users with active TikTok connections
            async with AsyncSession(engine) as session:
                statement = select(User.id)
                result = await session.execute(statement)
                user_ids = result.scalars().all()
            
            for uid in user_ids:
                try:
                    await sync_user_content(uid)
                except Exception as e:
                    print(f"Error syncing content for user {uid}: {e}")
            
            await asyncio.sleep(300) # Wait 5 minutes before next polling cycle

    def stop(self):
        self.running = False
