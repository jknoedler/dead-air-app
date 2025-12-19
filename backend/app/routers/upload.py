from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/{platform}")
async def upload_media(platform: str, file: UploadFile = File(...), caption: str = ""):
    # Placeholder: validate platform, forward file to platform service
    # For now just acknowledge receipt
    return JSONResponse(content={"msg": f"Received file for {platform}"}, status_code=status.HTTP_200_OK)
