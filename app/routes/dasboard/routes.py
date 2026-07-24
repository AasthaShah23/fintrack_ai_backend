from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.user import User
from app.dependencies import get_current_user

from app.database import get_db

from .service import (
    get_dashboard_service,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# Get dashboard summary
@router.get("/", dependencies=[Depends(get_current_user)])
def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_dashboard_service(db, current_user)