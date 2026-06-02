from app.schemas.user_schema import UserCreate
from app.core.security import create_access_token

def register(user: UserCreate):
    return {
        "message": "User registered",
        "data": user
    }

def loginUser():
    user_data = {
        "username": "Aastha Shah",
        "password": "Äastha@123"
    }
    token = create_access_token(user_data)

    return {
        "access_token": token
    }