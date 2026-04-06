from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserResponse
from app.api.dependencies import RoleChecker

router = APIRouter(prefix="/users", tags=["User Management"])

# Only Admins can manage users
admin_only = RoleChecker([UserRole.ADMIN])

@router.get("/", response_model=List[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """Get a list of all registered users (Admin only)"""
    users = db.query(User).all()
    return users

@router.put("/{user_id}/status", response_model=UserResponse)
def change_user_status(
    user_id: int, 
    is_active: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only)
):
    """Activate or deactivate a user account (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Prevent admin from deactivating themselves
    if user.id == current_user.id and not is_active:
        raise HTTPException(status_code=400, detail="You cannot deactivate your own account.")

    user.is_active = is_active
    db.commit()
    db.refresh(user)
    return user