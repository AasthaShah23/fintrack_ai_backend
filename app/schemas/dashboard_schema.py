from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class DashboardSummary(BaseModel):
    total_balance: Decimal
    monthly_income: Decimal
    monthly_expense: Decimal
    savings: Decimal
    budget_remaining: Decimal


class ExpenseTrend(BaseModel):
    month: str
    expense: Decimal


class CategoryExpense(BaseModel):
    category: str
    amount: Decimal
    color: str


class IncomeVsExpense(BaseModel):
    month: str
    income: Decimal
    expense: Decimal


class LatestTransaction(BaseModel):
    id: int
    amount: Decimal
    date: datetime
    type: str
    category: str


class DashboardCharts(BaseModel):
    expense_trend: list[ExpenseTrend]
    category_expense: list[CategoryExpense]
    income_vs_expense: list[IncomeVsExpense]


class DashboardWidgets(BaseModel):
    latest_transactions: list[LatestTransaction]


class DashboardResponse(BaseModel):
    summary: DashboardSummary
    charts: DashboardCharts
    widgets: DashboardWidgets