from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.utils.security import hash_password

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):


    
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)


    return {
        "message": "User created successfully",
        "user_id": new_user.id
    }