from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    profile: Dict

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class OrganisationCreate(BaseModel):
    name: str

class OrganisationResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class RoleCreate(BaseModel):
    name: str
    org_id: int

class RoleResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class MemberCreate(BaseModel):
    org_id: int
    user_id: int
    role_id: int

class MemberResponse(BaseModel):
    id: int
    org_id: int
    user_id: int
    role_id: int

    class Config:
        orm_mode = True
