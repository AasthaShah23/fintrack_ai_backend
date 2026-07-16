from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.user import User
from app.dependencies import get_current_user
from app.schemas.category_schema import CategoryCreate

from app.database import get_db

from .service import (
    get_categories,
    create_category_service
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@router.get("/", dependencies=[Depends(get_current_user)])
def get_category_list(db: Session = Depends(get_db), _: User = Depends(get_current_user),):
    return get_categories(db)


# create an endpoint for creating an category
@router.post("/", dependencies=[Depends(get_current_user)])
def create_category(payload: CategoryCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user),):
    return create_category_service(db, payload)