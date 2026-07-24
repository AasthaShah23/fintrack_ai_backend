from fastapi import Depends
from sqlalchemy.orm import Session, joinedload
from app.db.user import User
from app.dependencies import get_current_user
from app.database import get_db

from datetime import datetime, timezone
from app.db.transaction import Transaction, TransactionType
from app.db.user_categories import UserCategory
from app.db.categories import Category
from sqlalchemy import func, case
from app.schemas.dashboard_schema import DashboardSummary, ExpenseTrend, CategoryExpense, IncomeVsExpense, LatestTransaction, DashboardResponse, DashboardCharts, DashboardWidgets


def get_dashboard_summary(db: Session, user_id: int) -> DashboardSummary:
    now = datetime.now(timezone.utc)

    first_day = datetime(
        now.year,
        now.month,
        1,
        tzinfo=timezone.utc
    )

    # Monthly Income
    monthly_income = (
        db.query(
            func.coalesce(func.sum(Transaction.amount), 0)
        )
        .filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.income,
            Transaction.is_delete == False,
            Transaction.transaction_date >= first_day
        )
        .scalar()
    )

    # Monthly Expense
    monthly_expense = (
        db.query(
            func.coalesce(func.sum(Transaction.amount), 0)
        )
        .filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.expense,
            Transaction.is_delete == False,
            Transaction.transaction_date >= first_day
        )
        .scalar()
    )

    # Total Income
    total_income = (
        db.query(
            func.coalesce(func.sum(Transaction.amount), 0)
        )
        .filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.income,
            Transaction.is_delete == False
        )
        .scalar()
    )

    # Total Expense
    total_expense = (
        db.query(
            func.coalesce(func.sum(Transaction.amount), 0)
        )
        .filter(
            Transaction.user_id == user_id,
            Transaction.type == TransactionType.expense,
            Transaction.is_delete == False
        )
        .scalar()
    )

    # Total Budget
    total_budget = (
        db.query(
            func.coalesce(func.sum(UserCategory.monthly_budget), 0)
        )
        .filter(
            UserCategory.user_id == user_id,
            UserCategory.is_active == True
        )
        .scalar()
    )

    return DashboardSummary(
        total_balance=total_income - total_expense,
        monthly_income=monthly_income,
        monthly_expense=monthly_expense,
        savings=monthly_income - monthly_expense,
        budget_remaining=total_budget - monthly_expense,
    )

def get_expense_trend(
        db: Session,
        user_id: int
    )-> list[ExpenseTrend]:

        expense_trend = (
            db.query(
                func.date_trunc(
                    "month",
                    Transaction.transaction_date
                ).label("month"),

                func.sum(
                    Transaction.amount
                ).label("expense")
            )
            .filter(
                Transaction.user_id == user_id,
                Transaction.type == TransactionType.expense,
                Transaction.is_delete == False
            )
            .group_by(
                func.date_trunc(
                    "month",
                    Transaction.transaction_date
                )
            )
            .order_by(
                func.date_trunc(
                    "month",
                    Transaction.transaction_date
                ).desc()
            )
            .limit(6)
            .all()
        )

        return [
        ExpenseTrend(
            month=row.month.strftime("%b"),
            expense=row.expense,
        )
        for row in expense_trend
    ]

# get function to get category wise expense
def get_category_expense_trend(
        db: Session,
        user_id: int
    )-> list[CategoryExpense]:

        now = datetime.now(timezone.utc)

        first_day = datetime(
            now.year,
            now.month,
            1,
            tzinfo=timezone.utc
        )

        expenses = (
            db.query(
                Category.id,
                Category.name,
                Category.color,
                func.sum(Transaction.amount).label("amount")
            )
            .join(
                Category,
                Category.id == Transaction.category_id
            )
            .filter(
                Transaction.user_id == user_id,
                Transaction.type == TransactionType.expense,
                Transaction.is_delete == False,
                Transaction.transaction_date >= first_day
            )
            .group_by(
                Category.id,
                Category.name,
                Category.color
            )
            .order_by(
                func.sum(Transaction.amount).desc()
            )
            .all()
        )

        return [
            CategoryExpense(
                category=row.name,
                amount=row.amount,
                color=row.color
            )
            for row in expenses
        ]

def get_income_vs_expense(
        db: Session,
        user_id: int
    )-> list[IncomeVsExpense]:
    result = (
        db.query(
            func.date_trunc(
                "month",
                Transaction.transaction_date
            ).label("month"),

            func.sum(
                case(
                    (
                        Transaction.type == TransactionType.income,
                        Transaction.amount
                    ),
                    else_=0
                )
            ).label("income"),

            func.sum(
                case(
                    (
                        Transaction.type == TransactionType.expense,
                        Transaction.amount
                    ),
                    else_=0
                )
            ).label("expense"),
        )
        .filter(
            Transaction.user_id == user_id,
            Transaction.is_delete == False
        )
        .group_by(
            func.date_trunc(
                "month",
                Transaction.transaction_date
            )
        )
        .order_by(
            func.date_trunc(
                "month",
                Transaction.transaction_date
            ).desc()
        )
        .limit(6)
        .all()
    )

    result.reverse()

    return [
         IncomeVsExpense(
            month=row.month.strftime("%b"),
            income=row.income,
            expense=row.expense
       )
        for row in result
    ]

def get_latest_transactions(
        db: Session,
        user_id: int,
        limit: int = 5
    )-> list[LatestTransaction]:
    transactions = (
        db.query(
            Transaction
        )
        .options(joinedload(Transaction.category))
        .filter(
            Transaction.user_id == user_id,
            Transaction.is_delete == False
        )
        .order_by(Transaction.transaction_date.desc())
        .limit(limit)
        .all()
    )
    

    return [
        LatestTransaction(
            id=transaction.id,
            amount=transaction.amount,
            date=transaction.transaction_date,
            type=transaction.type,
            category=transaction.category.name
        )
        for transaction in transactions
    ]

# Get Dashboard summary
def get_dashboard_service(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardResponse:

    user_id = current_user.id

    return DashboardResponse(
        summary=get_dashboard_summary(db, user_id),
        charts=DashboardCharts(
            expense_trend=get_expense_trend(db, user_id),
            category_expense=get_category_expense_trend(db, user_id),
            income_vs_expense=get_income_vs_expense(db, user_id),
        ),
        widgets=DashboardWidgets(
            latest_transactions=get_latest_transactions(db, user_id),
        ),
    )