from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.client import ClientModel
from app.models.pet import PetModel
from app.schemas.pet import PetCreate

router = APIRouter(prefix="/api/pets", tags=["Pets"])

@router.post("", status_code=status.HTTP_200_OK)
def find_or_create_pet(pet_in: PetCreate, db: Session = Depends(get_db)):
   
    client = None
    if pet_in.client_id:
        client = db.query(ClientModel).filter(ClientModel.id == pet_in.client_id).first()
    elif pet_in.client_email:
        client = db.query(ClientModel).filter(ClientModel.email == pet_in.client_email).first()

   
    if not client:
        if pet_in.client_name and pet_in.client_email and pet_in.client_phone:
            client = ClientModel(
                name=pet_in.client_name,
                email=pet_in.client_email,
                phone=pet_in.client_phone
            )
            db.add(client)
            db.flush()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cliente no encontrado y datos insuficientes para crearlo."
            )

   
    existing_pet = db.query(PetModel).filter(
        PetModel.client_id == client.id,
        PetModel.name == pet_in.pet_name
    ).first()

   
    if existing_pet:
        return {
            "message": "Mascota existente recuperada con exito",
            "pet_id": str(existing_pet.id),
            "client_id": str(client.id),
            "is_new": False
        }

    
    new_pet = PetModel(
        client_id=client.id,
        name=pet_in.pet_name,
        species=pet_in.pet_species
    )
    db.add(new_pet)
    db.commit()
    db.refresh(new_pet)

    return {
        "message": "Mascota registrada exitosamente",
        "pet_id": str(new_pet.id),
        "client_id": str(client.id),
        "is_new": True
    }

@router.get("", status_code=status.HTTP_200_OK)
def get_pets_by_email(email: str, db: Session = Depends(get_db)):
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El parametro 'email' es obligatorio."
        )

    client = db.query(ClientModel).filter(ClientModel.email == email).first()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontro ningun cliente registrado con ese correo electronico."
        )

    pets = db.query(PetModel).filter(PetModel.client_id == client.id).all()

    return {
        "client": {
            "id": str(client.id),
            "name": client.name,
            "email": client.email,
            "phone": client.phone
        },
        "pets": [
            {
                "id": str(pet.id),
                "name": pet.name,
                "species": pet.species,
                "created_at": pet.created_at
            }
            for pet in pets
        ]
    }