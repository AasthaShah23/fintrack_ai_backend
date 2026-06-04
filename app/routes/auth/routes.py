from fastapi import APIRouter
from app.schemas.user_schema import UserCreate
from .service import register, loginUser

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserCreate)
def create_new_user(user: UserCreate):
      return register(user)

@router.post("/login")
def login():
    return loginUser()