from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.auth import get_current_user
from app.models.report import Report

from app.database.database import get_db
from app.models.user import User
from app.schemas.login_schema import LoginRequest
from app.schemas.user_schema import (
    UserCreate,
    ProfileUpdate,
    PasswordUpdate
)

from app.utils.security import (
    hash_password,
    verify_password
)

from app.utils.auth import create_access_token

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
security = HTTPBearer()

@router.post("/signup")
def signup(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }

@router.post("/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        return {
            "message": "User not found"
        }

    if not verify_password(
        user.password,
        existing_user.password
    ):
        return {
            "message": "Incorrect password"
        }

    token = create_access_token(
        {"sub": existing_user.email}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/profile")
def get_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    current_user = get_current_user(
        token,
        db
    )

    if not current_user:
        return {
            "message":"Invalid token"
        }

    total_reports = db.query(
        Report
    ).filter(
        Report.user_id == current_user.id
    ).count()

    return {
        "username": current_user.username,
        "email": current_user.email,
        "total_reports": total_reports
    }

@router.put("/profile")
def update_profile(
    profile: ProfileUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    current_user = get_current_user(
        token,
        db
    )

    if not current_user:
        return {
            "message": "Invalid token"
        }

    current_user.username = profile.username
    current_user.email = profile.email

    db.commit()
    db.refresh(current_user)

    return {
        "message": "Profile updated successfully",
        "username": current_user.username,
        "email": current_user.email
    }

@router.put("/change-password")
def change_password(
    password_data: PasswordUpdate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    current_user = get_current_user(
        token,
        db
    )

    if not verify_password(
        password_data.old_password,
        current_user.password
    ):
        return {
            "message":"Old password incorrect"
        }

    current_user.password = hash_password(
        password_data.new_password
    )

    db.commit()

    return {
        "message":"Password changed successfully"
    }
@router.get("/all-users")
def get_all_users(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    current_user = get_current_user(
        token,
        db
    )

    if not current_user:
        return {
            "message":"Invalid token"
        }

    if current_user.role != "admin":
        return {
            "message":"Access denied. Admin only"
        }

    users = db.query(User).all()

    result = []

    for user in users:
        result.append(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        )

    return result