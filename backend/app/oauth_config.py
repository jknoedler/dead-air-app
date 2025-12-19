# backend/app/oauth_config.py

import os
from authlib.integrations.starlette_client import OAuth

oauth = OAuth()

# TikTok
oauth.register(
    name='tiktok',
    client_id=os.getenv('TIKTOK_CLIENT_KEY'),
    client_secret=os.getenv('TIKTOK_CLIENT_SECRET'),
    access_token_url='https://open-api.tiktok.com/oauth/access_token/',
    authorize_url='https://www.tiktok.com/auth/authorize/',
    api_base_url='https://open-api.tiktok.com/',
    client_kwargs={'scope': 'user.info.basic,video.list,video.upload'},
)

# YouTube (Google)
oauth.register(
    name='youtube',
    client_id=os.getenv('YOUTUBE_CLIENT_ID'),
    client_secret=os.getenv('YOUTUBE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile https://www.googleapis.com/auth/youtube.upload'},
)

# Instagram (Facebook)
oauth.register(
    name='instagram',
    client_id=os.getenv('INSTAGRAM_CLIENT_ID'),
    client_secret=os.getenv('INSTAGRAM_CLIENT_SECRET'),
    access_token_url='https://api.instagram.com/oauth/access_token',
    authorize_url='https://api.instagram.com/oauth/authorize',
    api_base_url='https://graph.instagram.com/',
    client_kwargs={'scope': 'user_profile,user_media'},
)
