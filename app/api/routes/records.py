from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.db.session import get_db
from app.models.record import FinancialRecord, TransactionType
from app.models.user import UserRole, User
from app.schemas.record import RecordCreate, RecordUpdate, RecordResponse
from app.api.dependencies import get_current_user, RoleChecker

router = APIRouter(prefix="/records", tags=["Financial Records"])

# Define our role checkers
admin_only = RoleChecker([UserRole.ADMIN])
admin_and_analyst = RoleChecker([UserRole.ADMIN, UserRole.ANALYST])

@router.post("/", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
def create_record(
    record_in: RecordCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only) # Only Admins can create
):
    new_record = FinancialRecord(
        **record_in.model_dump(),
        owner_id=current_user.id
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

@router.get("/", response_model=List[RecordResponse])
def get_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    transaction_type: Optional[TransactionType] = None,
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_and_analyst) # Admins & Analysts can view
):
    # Start building the SQLAlchemy query
    query = db.query(FinancialRecord)

    # Apply dynamic filters if they are provided
    if transaction_type:
        query = query.filter(FinancialRecord.transaction_type == transaction_type)
    if category:
        # Case-insensitive category search
        query = query.filter(FinancialRecord.category.ilike(f"%{category}%"))
    if start_date:
        query = query.filter(FinancialRecord.date >= start_date)
    if end_date:
        query = query.filter(FinancialRecord.date <= end_date)

    # Execute query with pagination
    records = query.order_by(FinancialRecord.date.desc()).offset(skip).limit(limit).all()
    return records

@router.get("/{record_id}", response_model=RecordResponse)
def get_record(
    record_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_and_analyst)
):
    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return record

@router.put("/{record_id}", response_model=RecordResponse)
def update_record(
    record_id: int, 
    record_update: RecordUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only) # Only Admins can update
):
    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    
    # Update only the fields that were provided
    update_data = record_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(record, key, value)
        
    db.commit()
    db.refresh(record)
    return record

@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(
    record_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only) # Only Admins can delete
):
    record = db.query(FinancialRecord).filter(FinancialRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    
    db.delete(record)
    db.commit()
    return None