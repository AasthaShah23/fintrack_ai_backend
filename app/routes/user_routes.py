from fastapi import APIRouter
from app.schemas.user_schema import UserCreate

router = APIRouter()

@router.post("/register")
def register(user: UserCreate):
    return {
        "message": "User registered",
        "data": user
    }