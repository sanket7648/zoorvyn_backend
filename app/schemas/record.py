from pydantic import BaseModel, condecimal, Field
from datetime import date, datetime
from typing import Optional
from app.models.record import TransactionType

class RecordBase(BaseModel):
    amount: condecimal(gt=0, max_digits=10, decimal_places=2) # Amount must be > 0
    transaction_type: TransactionType
    category: str = Field(..., min_length=1)
    date: date
    notes: Optional[str] = None

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    amount: Optional[condecimal(gt=0, max_digits=10, decimal_places=2)] = None
    category: Optional[str] = None
    notes: Optional[str] = None

class RecordResponse(RecordBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True