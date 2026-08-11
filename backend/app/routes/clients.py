from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.client import ClientModel
from app.schemas.client import ClientCheckRequest, ClientCheckResponse, ClientCreate, ClientResponse

router = APIRouter(prefix="/api/clients", tags=["Clients"])

@router.post("/check-email", response_model=ClientCheckResponse)
def check_email(payload: ClientCheckRequest, db: Session = Depends(get_db)):
    """
    Paso 1: Revisa si el email ya existe.
    Si existe, retorna exists=True y los datos del cliente.
    """
    client = db.query(ClientModel).filter(ClientModel.email == payload.email).first()
    
    if client:
        return ClientCheckResponse(
            exists=True,
            message="Este correo ya se encuentra registrado",
            client=client
        )
    
    return ClientCheckResponse(
        exists=False,
        message="Correo no registrado",
        client=None
    )

@router.post("", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(client_in: ClientCreate, db: Session = Depends(get_db)):
    """
    Paso 2 (Opcional): Registrar cliente si el email no existia.
    """
    existing_client = db.query(ClientModel).filter(ClientModel.email == client_in.email).first()
    if existing_client:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El cliente ya existe."
        )

    new_client = ClientModel(
        name=client_in.name,
        email=client_in.email,
        phone=client_in.phone
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client