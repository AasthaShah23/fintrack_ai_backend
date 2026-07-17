from unicodedata import category

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.db.user_categories import UserCategory
from app.db.user import User
from app.schemas.budget_schema import CreateBudgetRequest, BudgetResponse, GetBudgetResponse

from app.db.categories import Category

# create a service for setting monthly budget category wise
def set_monthly_budget_service(category_id: int, db: Session, payload: CreateBudgetRequest, current_user: User):

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
    
    if payload.budget < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Budget amount cannot be negative"
        )
    
    existing_user_category =  (
        db.query(UserCategory)
        .filter(
            UserCategory.user_id == current_user.id,
            UserCategory.category_id == category_id
        )
        .first()
    )

    if existing_user_category:

        # Active record already exists
        if existing_user_category.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Monthly budget for this category already exists. Please update it instead."
            )

        # Restore soft-deleted record
        existing_user_category.is_active = True
        existing_user_category.monthly_budget = payload.budget

        db.commit()
        db.refresh(existing_user_category)

        return {
            "message": "Monthly budget set successfully.",
            "data": BudgetResponse.model_validate(existing_user_category)
        }
    
    
    
    user_category = UserCategory(
        user_id=current_user.id,
        category_id= category_id,
        monthly_budget=payload.budget
    )
    
    try:
        db.add(user_category)
        db.commit()
        db.refresh(user_category)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error setting monthly budget"
        )

    return {
        "message": "Monthly budget set successfully.",
        "data": BudgetResponse.model_validate(user_category)
    }

# Update monthly budget category wise
def update_monthly_budget_service(category_id: int, db: Session, payload: CreateBudgetRequest, current_user: User):

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
    
    user_category = (
        db.query(UserCategory)
        .filter(
            UserCategory.user_id == current_user.id,
            UserCategory.category_id == category_id
        )
        .first()
    )

    if not user_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monthly budget for this category not found. Please set the monthly budget first."
        )

    user_category.monthly_budget = payload.budget

    try:
        db.commit()
        db.refresh(user_category)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating monthly budget"
        )

    return {
        "message": "Monthly budget updated successfully.",
        "data": BudgetResponse.model_validate(user_category)
    }

# Delete monthly budget category wise
def delete_monthly_budget_service(category_id: int, db: Session, current_user: User):

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
    
    user_category = (
        db.query(UserCategory)
        .filter(
            UserCategory.user_id == current_user.id,
            UserCategory.category_id == category_id
        )
        .first()
    )

    if not user_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monthly budget for this category not found."
        )

    try:
        user_category.is_active = False

        db.commit()
        db.refresh(category)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting monthly budget"
        )

    return {
        "message": "Monthly budget deleted successfully."
    }

# Get monthly budget category wise listing
def get_monthly_budget_service(
    db: Session,
    current_user: User
):
    user_categories = (
        db.query(UserCategory)
        .options(joinedload(UserCategory.category))
        .filter(
            UserCategory.user_id == current_user.id,
            UserCategory.is_active == True
        )
        .all()
    )

    return {
        "message": "Monthly budget fetched successfully.",
        "data": [
            GetBudgetResponse.model_validate(user_category)
            for user_category in user_categories
        ]
    }