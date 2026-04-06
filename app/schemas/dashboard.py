from pydantic import BaseModel
from typing import List, Dict
from decimal import Decimal
from app.schemas.record import RecordResponse

class CategorySummary(BaseModel):
    category: str
    total: Decimal

class DashboardSummary(BaseModel):
    total_income: Decimal
    total_expense: Decimal
    net_balance: Decimal
    income_by_category: List[CategorySummary]
    expense_by_category: List[CategorySummary]
    recent_transactions: List[RecordResponse]