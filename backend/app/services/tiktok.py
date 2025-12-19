# backend/app/services/tiktok.py

import httpx
from .base import SocialPlatformService
from .scrapers.tiktok_scraper import TikTokScraper

class TikTokService(SocialPlatformService):
    def __init__(self, client_id: str, client_secret: str):
        super().__init__("tiktok", client_id, client_secret)
        self.api_base = "https://open-api.tiktok.com/"
        self.scraper = TikTokScraper()

    async def get_auth_url(self, redirect_uri: str) -> str:
        # Authlib handles this, but here's the manual way if needed
        return f"{self.api_base}platform/oauth/connect/?client_key={self.client_id}&scope=user.info.basic,video.list,video.upload&response_type=code&redirect_uri={redirect_uri}"

    async def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base}oauth/access_token/",
                data={
                    "client_key": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                }
            )
            return response.json()

    async def get_latest_video(self, open_id: str, access_token: str) -> dict:
        """Fetches the latest video from the user's feed."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_base}video/list/",
                json={
                    "open_id": open_id,
                    "access_token": access_token,
                    "cursor": 0,
                    "count": 1
                }
            )
            data = response.json()
            if data.get("data", {}).get("videos"):
                return data["data"]["videos"][0]
            return None

    async def download_video_no_watermark(self, video_data: dict) -> str:
        """
        Fetches the clean video URL and downloads it to a temporary location.
        """
        video_url = video_data.get("share_url") # The public link to the video
        if not video_url:
            return None

        clean_url = await self.scraper.get_no_watermark_url(video_url)
        if not clean_url:
            return None

        video_id = video_data.get("id")
        dest_path = f"/tmp/tiktok_{video_id}_clean.mp4"
        
        success = await self.scraper.download_video(clean_url, dest_path)
        return dest_path if success else None

    async def upload_video(self, video_path: str, caption: str, access_token: str) -> str:
        # TikTok doesn't typically allow direct file uploads via the open-api for standard users
        # without special permissions, but we stub it here.
        return "tiktok-post-id-123"
