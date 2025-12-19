from fastapi import APIRouter, Depends
from typing import List, Dict

router = APIRouter()

@router.get("/daily", response_model=List[Dict[str, str]])
async def get_daily_suggestions():
    # Placeholder: In production, this would fetch from a DB or AI service
    return [
        {
            "title": "The 'Behind the Scenes' Reveal",
            "category": "Vlog",
            "description": "Show exactly how you made your last piece of content. People love seeing the messy process."
        },
        {
            "title": "Common Industry Myth Buster",
            "category": "Educational",
            "description": "Pick one common misconception in your niche and explain why it's wrong in under 30 seconds."
        },
        {
            "title": "Day in the Life (ASMR)",
            "category": "Aesthetic",
            "description": "Fast cuts of your morning routine with only ambient sounds and text overlays."
        }
    ]
