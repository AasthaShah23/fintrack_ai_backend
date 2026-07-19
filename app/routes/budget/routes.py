from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.user import User
from app.dependencies import get_current_user
from app.schemas.budget_schema import CreateBudgetRequest

from app.database import get_db

from .service import (
    set_monthly_budget_service,
    update_monthly_budget_service,
    delete_monthly_budget_service,
    get_monthly_budget_service
)

router = APIRouter(
    prefix="/budget",
    tags=["Monthly Budget"]
)

# Set monthly budget category wise
@router.post("/{category_id}", dependencies=[Depends(get_current_user)])
def set_monthly_budget(category_id: int, payload: CreateBudgetRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return set_monthly_budget_service(category_id, db, payload, current_user)

# Update monthly budget category wise
@router.put("/{category_id}", dependencies=[Depends(get_current_user)])
def update_monthly_budget(category_id: int, payload: CreateBudgetRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_monthly_budget_service(category_id, db, payload, current_user)

# Delete monthly budget category wise
@router.delete("/{category_id}", dependencies=[Depends(get_current_user)])
def delete_monthly_budget(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_monthly_budget_service(category_id, db, current_user)

# Get monthly budget category wise listing
@router.get("/", dependencies=[Depends(get_current_user)])
def get_monthly_budget(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_monthly_budget_service(db, current_user)