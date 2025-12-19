from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/user/{user_id}/checkin")
async def daily_checkin(user_id: int):
    # TODO: Record daily activity in DB (opened = True)
    return JSONResponse(content={"msg": f"User {user_id} checked in"}, status_code=status.HTTP_200_OK)

@router.get("/user/{user_id}/activity")
async def get_activity(user_id: int):
    # TODO: Retrieve activity summary from DB
    return {"user_id": user_id, "activity": "placeholder"}
