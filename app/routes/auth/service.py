from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.user import User
from app.schemas.user_schema import UserCreate
from app.schemas.auth_schema import LoginRequest

from app.core.hash_password import get_password_hash
from app.core.hash_password import verify_password
from app.core.security import create_access_token



def signup(
    user: UserCreate,
    db: Session
):

    existing_email = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    existing_phone = (
        db.query(User)
        .filter(User.phone_number == user.phone_number)
        .first()
    )

    if existing_phone:
        raise HTTPException(
            status_code=400,
            detail="Phone number already registered"
        )

    hashed_password = get_password_hash(user.password)

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "data": {
            "id": new_user.id,
            "firstName": new_user.first_name,
            "lastName": new_user.last_name,
            "email": new_user.email,
            "phoneNumber": new_user.phone_number
        }
    }

def login(payload: LoginRequest, db: Session):
     existing_user = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )

     if not existing_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

     if not verify_password(payload.password, existing_user.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid email or password"
        )

     token = create_access_token(
    {
        "sub": str(existing_user.id),
        "email": existing_user.email
    }
)

     return {
        "message": "User login successfully",
        "accessToken": token,
        "data": {
            "id": existing_user.id,
            "firstName": existing_user.first_name,
            "lastName": existing_user.last_name,
            "email": existing_user.email,
            "phoneNumber": existing_user.phone_number
        }
    }


def forgot_password(
    email: EmailStr,
    db: Session
):
    existing_email = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if not existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email is not registered"
        )

    hashed_password = get_password_hash(user.password)

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone_number=user.phone_number,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Email sent successfully",
        "data": {
            "id": new_user.id,
            "firstName": new_user.first_name,
            "lastName": new_user.last_name,
            "email": new_user.email,
            "phoneNumber": new_user.phone_number
        }
    }