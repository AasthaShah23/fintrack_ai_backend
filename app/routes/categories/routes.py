from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.user import User
from app.dependencies import get_current_user
from app.schemas.category_schema import CategoryCreate, CategoryUpdate

from app.database import get_db

from .service import (
    get_categories,
    create_category_service,
    update_category_service,
    delete_category_service
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

# Get all categories
@router.get("/", dependencies=[Depends(get_current_user)])
def get_category_list(db: Session = Depends(get_db)):
    return get_categories(db)


# Create an category
@router.post("/", dependencies=[Depends(get_current_user)])
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    return create_category_service(db, payload)

# Update the category based on id
@router.put("/{category_id}", dependencies=[Depends(get_current_user)])
def update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    return update_category_service(db, category_id, payload)

# Delete the category based on id but only if the category has is_system = False
@router.delete("/{category_id}", dependencies=[Depends(get_current_user)])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    return delete_category_service(db, category_id)
