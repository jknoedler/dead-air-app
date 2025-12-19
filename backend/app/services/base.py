# backend/app/services/base.py

from abc import ABC, abstractmethod
import httpx

class SocialPlatformService(ABC):
    def __init__(self, platform_name: str, client_id: str, client_secret: str):
        self.platform_name = platform_name
        self.client_id = client_id
        self.client_secret = client_secret

    @abstractmethod
    async def get_auth_url(self, redirect_uri: str) -> str:
        pass

    @abstractmethod
    async def exchange_code_for_token(self, code: str, redirect_uri: str) -> dict:
        pass

    @abstractmethod
    async def upload_video(self, video_path: str, caption: str, access_token: str) -> str:
        """Returns the platform post ID"""
        pass
