from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.user import User
from app.dependencies import get_current_user
from app.schemas.transaction_schema import TransactionCreate, TransactionUpdate

from app.database import get_db

from .service import (
    get_transactions_service,
    create_transactions_service,
    update_transactions_service,
    delete_transactions_service
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

# Create an transaction
@router.post("/", dependencies=[Depends(get_current_user)])
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_transactions_service(db, payload, current_user)

# Update the transaction based on id
@router.put("/{transaction_id}", dependencies=[Depends(get_current_user)])
def update_transaction(transaction_id: int, payload: TransactionUpdate, db: Session = Depends(get_db)):
    return update_transactions_service(db, transaction_id, payload)

# Delete the transaction based on id
@router.delete("/{transaction_id}", dependencies=[Depends(get_current_user)])
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    return delete_transactions_service(db, transaction_id)

# Get all transactions
@router.get("/", dependencies=[Depends(get_current_user)])
def get_transaction_list(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_transactions_service(db, current_user)