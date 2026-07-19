from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.category_schema import CategoryCreate, CategoryResponse, CategoryUpdate

from app.db.categories import Category

def get_categories(db: Session):

    categories = (
        db.query(Category)
        .filter(Category.is_delete == False)
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
    existing_category = (
        db.query(Category)
        .filter(Category.name == payload.name)
        .first()
    )

    if existing_category:

        # Category already exists and is active
        if not existing_category.is_delete:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category already exists."
            )

        # Restore the soft-deleted category
        existing_category.is_delete = False
        existing_category.color = payload.color
        existing_category.tag = payload.tag

        try:
            db.commit()
            db.refresh(existing_category)

        except Exception:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating category"
            )

        return {
            "message": "Category created successfully.",
            "data": CategoryResponse.model_validate(existing_category)
        }
    
    # create a new category if it doesn't exist
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

# create a service for updating a category
def update_category_service(db: Session, category_id: int, payload: CategoryUpdate):
    category = (
        db.query(Category)
        .filter(
            Category.id == category_id,
            Category.is_delete == False
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    update_category = payload.model_dump(exclude_unset=True)

    for key, value in update_category.items():
        setattr(category, key, value)

    try:
        db.commit()
        db.refresh(category)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating category"
        )

    return {
        "message": "Category updated successfully.",
        "data": CategoryResponse.model_validate(category)
    }

# create a service for deleting a category
def delete_category_service(db: Session, category_id: int):
    category = (
        db.query(Category)
        .filter(
            Category.id == category_id,
            Category.is_delete == False
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    if category.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete system category"
        )

    if category.is_delete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category is already deleted"
        )

    try:
        category.is_delete = True

        db.commit()
        db.refresh(category)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting category"
        )

    return {
        "message": "Category deleted successfully."
    }