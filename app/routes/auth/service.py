from app.schemas.user_schema import UserCreate

def register(user: UserCreate):
    return {
        "message": "User registered",
        "data": user
    }