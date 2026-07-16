from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.user import User
from app.schemas.category_schema import CategoryCreate, CategoryResponse

from app.db.categories import Category

def get_categories(db: Session):

    categories = (
        db.query(Category)
        .order_by(Category.name.asc())
        .all()
    )

    return {
        "message": "Categories fetched successfully.",
        "data": [
            CategoryResponse.model_validate(category)
            for category in categories
        ]
    }

# create a service for creating a category
def create_category_service(db: Session, payload: CategoryCreate):
    new_category = Category(
        name=payload.name,
        color=payload.color,
        tag=payload.tag
    )

    try:
        db.add(new_category)
        db.commit()
        db.refresh(new_category)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating category"
        )

    return {
        "message": "Category created successfully.",
        "data": CategoryResponse.model_validate(new_category)
    }