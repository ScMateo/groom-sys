from pydantic import BaseModel, EmailStr, Field
from uuid import UUID

class PetCreate(BaseModel):
    client_name: str = Field(..., min_length=2, max_length=100)
    client_email: EmailStr
    client_phone: str = Field(..., pattern=r"^3\d{9}$")
    pet_name: str = Field(..., min_length=1, max_length=50)
    pet_species: str = Field(..., min_length=2, max_length=30)

class PetResponse(BaseModel):
    pet_id: UUID
    client_email: EmailStr
    pet_name: str
    pet_species: str

    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    code: str
    message: str