# backend/app/services/scrapers/tiktok_scraper.py

import httpx
import re
import json

class TikTokScraper:
    """
    Service to fetch TikTok videos without watermarks.
    """
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def get_no_watermark_url(self, video_url: str) -> str:
        """
        Parses a TikTok video URL and returns the direct download link for the non-watermarked version.
        """
        async with httpx.AsyncClient(headers=self.headers, follow_redirects=True) as client:
            # 1. Fetch the video page
            response = await client.get(video_url)
            if response.status_code != 200:
                print(f"Failed to fetch TikTok page: {response.status_code}")
                return None

            # 2. Extract the video ID (Aweme ID)
            # Pattern for URLs like tiktok.com/@user/video/123...
            video_id_match = re.search(r'video/(\d+)', str(response.url))
            if not video_id_match:
                print("Could not find video ID in URL")
                return None
            
            video_id = video_id_match.group(1)

            # 3. Call the internal API to get video metadata
            # This is a common internal endpoint used by scrapers
            api_url = f"https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={video_id}"
            api_response = await client.get(api_url)
            
            if api_response.status_code != 200:
                print(f"Failed to fetch metadata from TikTok API: {api_response.status_code}")
                return None

            data = api_response.json()
            
            # 4. Extract the clean video URL
            try:
                # The 'play_addr' within 'video' usually contains multiple URLs
                # We want the 'url_list' which typically has the no-watermark link at index 0
                video_list = data["aweme_list"][0]["video"]["play_addr"]["url_list"]
                return video_list[0]
            except (KeyError, IndexError):
                print("Could not find clean video URL in metadata")
                return None

    async def download_video(self, url: str, destination_path: str):
        """
        Downloads the video from the provided URL to the local filesystem.
        """
        async with httpx.AsyncClient(headers=self.headers) as client:
            response = await client.get(url)
            if response.status_code == 200:
                with open(destination_path, 'wb') as f:
                    f.write(response.content)
                return True
            return False
