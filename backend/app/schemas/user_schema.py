from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class ProfileUpdate(BaseModel):
    username: str
    email: str


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str    