from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.schemas.transaction_schema import TransactionCreate, TransactionResponse, TransactionUpdate, GetTransactionResponse

from app.db.transaction import Transaction
from app.db.categories import Category
from app.db.user import User
from app.db.user_categories import UserCategory

# Creating a transaction
def create_transactions_service(db: Session, payload: TransactionCreate, current_user: User):
    category = (
        db.query(Category)
        .filter(
            Category.id == payload.category_id,
            Category.is_delete == False
        )
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    new_transaction = Transaction(
        user_id=current_user.id,
        category_id=payload.category_id,
        amount=payload.amount,
        type=payload.type,
        remark=payload.remark,
        transaction_date=payload.transaction_date,
        transaction_method=payload.transaction_method,
    )

    try:
        db.add(new_transaction)
        db.commit()
        db.refresh(new_transaction)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating transaction"
        )

    return {
        "message": "Transaction created successfully.",
        "data": TransactionResponse.model_validate(new_transaction)
    }

# Updating a transaction
def update_transactions_service(db: Session, transaction_id: int, payload: TransactionUpdate):
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.is_delete == False
        )
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    update_transaction = payload.model_dump(exclude_unset=True)

    for key, value in update_transaction.items():
        setattr(transaction, key, value)

    try:
        db.commit()
        db.refresh(transaction)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating transaction"
        )

    return {
        "message": "Transaction updated successfully.",
        "data": TransactionResponse.model_validate(transaction)
    }

# Deleting a transaction
def delete_transactions_service(db: Session, transaction_id: int):
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id,
            Transaction.is_delete == False
        )
        .first()
    )

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )

    if transaction.is_delete:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction is already deleted"
        )

    try:
        transaction.is_delete = True

        db.commit()
        db.refresh(transaction)

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting transaction"
        )

    return {
        "message": "Transaction deleted successfully."
    }

# Get all transactions
def get_transactions_service(db: Session, current_user: User):

    user_transactions = (
        db.query(Transaction)
        .options(joinedload(UserCategory.category))
        .filter(
            UserCategory.user_id == current_user.id,
            UserCategory.is_active == True
        )
        .all()
    )

    return {
        "message": "Transactions fetched successfully.",
        "data": [
            GetTransactionResponse.model_validate(transaction)
            for transaction in user_transactions
        ]
    }