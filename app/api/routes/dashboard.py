from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.models.record import FinancialRecord, TransactionType
from app.models.user import User
from app.schemas.dashboard import DashboardSummary
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard Summary"])

@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) # All authenticated users can view
):
    # 1. Calculate Total Income
    total_income = db.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.transaction_type == TransactionType.INCOME
    ).scalar() or 0

    # 2. Calculate Total Expense
    total_expense = db.query(func.sum(FinancialRecord.amount)).filter(
        FinancialRecord.transaction_type == TransactionType.EXPENSE
    ).scalar() or 0

    # 3. Calculate Net Balance
    net_balance = total_income - total_expense

    # 4. Category-wise Totals (Group By)
    # Income by category
    income_categories = db.query(
        FinancialRecord.category, 
        func.sum(FinancialRecord.amount).label("total")
    ).filter(
        FinancialRecord.transaction_type == TransactionType.INCOME
    ).group_by(FinancialRecord.category).all()

    # Expense by category
    expense_categories = db.query(
        FinancialRecord.category, 
        func.sum(FinancialRecord.amount).label("total")
    ).filter(
        FinancialRecord.transaction_type == TransactionType.EXPENSE
    ).group_by(FinancialRecord.category).all()

    # 5. Recent Activity (Last 5 records)
    recent_records = db.query(FinancialRecord).order_by(
        FinancialRecord.date.desc(), 
        FinancialRecord.created_at.desc()
    ).limit(5).all()

    # Format the response mapping to our Pydantic schema
    return DashboardSummary(
        total_income=total_income,
        total_expense=total_expense,
        net_balance=net_balance,
        income_by_category=[{"category": c[0], "total": c[1]} for c in income_categories],
        expense_by_category=[{"category": c[0], "total": c[1]} for c in expense_categories],
        recent_transactions=recent_records
    )