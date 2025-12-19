# backend/app/services/youtube.py

import httpx
from .base import SocialPlatformService

class YouTubeService(SocialPlatformService):
    def __init__(self, client_id: str, client_secret: str):
        super().__init__("youtube", client_id, client_secret)
        self.api_base = "https://www.googleapis.com/youtube/v3/"

    async def get_auth_url(self, redirect_uri: str) -> str:
        return f"https://accounts.google.com/o/oauth2/v2/auth?client_id={self.client_id}&redirect_uri={redirect_uri}&response_type=code&scope=https://www.googleapis.com/auth/youtube.upload&access_type=offline&prompt=consent"

    async def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://oauth2.googleapis.com/token",
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "grant_type": "authorization_code",
                    "redirect_uri": redirect_uri,
                }
            )
            return response.json()

    async def upload_video(self, video_path: str, caption: str, access_token: str) -> str:
        """
        Uploads a video to YouTube as a Short.
        """
        # YouTube Shorts are just videos with #Shorts in the description or title
        # and a vertical aspect ratio.
        async with httpx.AsyncClient() as client:
            # This is a simplified version of the upload process
            # Real implementation involves a multi-part upload or resumable upload
            headers = {"Authorization": f"Bearer {access_token}"}
            metadata = {
                "snippet": {
                    "title": caption[:100],
                    "description": f"{caption} #Shorts",
                    "categoryId": "22" # People & Blogs
                },
                "status": {
                    "privacyStatus": "public",
                    "selfDeclaredMadeForKids": False
                }
            }
            # Mocking the upload call for now
            print(f"Uploading {video_path} to YouTube Shorts...")
            return "youtube-video-id-xyz"
