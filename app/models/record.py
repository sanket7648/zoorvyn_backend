from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Numeric, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum
from app.db.session import Base

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), nullable=False) # e.g., 99999999.99
    transaction_type = Column(Enum(TransactionType), nullable=False, index=True)
    category = Column(String, index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)
    notes = Column(Text, nullable=True)
    
    # Link the record to the user who created it
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Establish relationship to the User model
    owner = relationship("User", back_populates="records")