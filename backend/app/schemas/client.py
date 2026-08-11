from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional

class ClientCheckRequest(BaseModel):
    email: EmailStr

class ClientCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., pattern=r"^3\d{9}$")

class ClientResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    phone: str

    class Config:
        from_attributes = True

class ClientCheckResponse(BaseModel):
    exists: bool
    message: str
    client: Optional[ClientResponse] = None