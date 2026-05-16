from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.utils.auth import verify_token

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

security = HTTPBearer()


@router.get("/")
def get_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    email = verify_token(token)

    if not email:
        return {"message": "Invalid token"}

    return {
        "message": "Protected route accessed",
        "email": email
    }