from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional

class PetCreate(BaseModel):
    client_id: Optional[UUID] = None
    client_name: Optional[str] = Field(None, min_length=2, max_length=100)
    client_email: Optional[EmailStr] = None
    client_phone: Optional[str] = Field(None, pattern=r"^3\d{9}$")
    
    pet_name: str = Field(..., min_length=1, max_length=50)
    # Validacion estricta para especie: Perro o Gato
    pet_species: str = Field(..., pattern=r"^(Perro|Gato)$")

class PetResponse(BaseModel):
    id: UUID
    name: str
    species: str
    client_id: UUID

    class Config:
        from_attributes = True