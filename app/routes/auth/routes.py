from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import EmailStr
from app.schemas.user_schema import UserCreate
from app.schemas.auth_schema import (
    LoginRequest,
    ResetPasswordRequest
)
from app.database import get_db

from .service import (
    signup,
    login,
    forgot_password,
    
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/signup")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return signup(user, db)


@router.post("/login")
def login_user(payload: LoginRequest, db: Session = Depends(get_db)):
    return login(payload, db)


@router.post("/forgot-password")
def forgot_password_api(email: EmailStr, db: Session = Depends(get_db)):
    return forgot_password(email, db)


# @router.post("/reset-password")
# def reset_password_api(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
#     return reset_password(payload, db)