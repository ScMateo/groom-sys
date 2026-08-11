from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.admin import AdminModel
from app.models.appointment import AppointmentModel
from app.models.pet import PetModel
from app.models.client import ClientModel
from app.schemas.admin import AdminLoginRequest, AdminLoginResponse

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.post("/login", response_model=AdminLoginResponse)
def admin_login(payload: AdminLoginRequest, db: Session = Depends(get_db)):
    """
    Valida el usuario y contrasena del administrador.
    """
    admin = db.query(AdminModel).filter(AdminModel.username == payload.username).first()
    
    # NOTA: En produccion idealmente usas passlib/bcrypt para verificar el hash.
    # Aqui comparamos la credencial para validar el flujo.
    if not admin or admin.password_hash != payload.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Informacion de acceso invalida"
        )

    return AdminLoginResponse(
        message="Autenticacion exitosa",
        authenticated=True,
        username=admin.username
    )


@router.get("/weekly-appointments", status_code=status.HTTP_200_OK)
def get_weekly_appointments(
    start_date: date = date.today(),
    db: Session = Depends(get_db)
):
    """
    Retorna la lista de citas agendadas para los siguientes 7 dias
    a partir de start_date (por defecto hoy).
    """
    end_date = start_date + timedelta(days=7)

    appointments = (
        db.query(AppointmentModel, PetModel, ClientModel)
        .join(PetModel, AppointmentModel.pet_id == PetModel.id)
        .join(ClientModel, PetModel.client_id == ClientModel.id)
        .filter(
            AppointmentModel.appt_date >= start_date,
            AppointmentModel.appt_date < end_date,
            AppointmentModel.status == "BOOKED"
        )
        .order_by(AppointmentModel.appt_date.asc(), AppointmentModel.time_slot.asc())
        .all()
    )

    result = []
    for appt, pet, client in appointments:
        result.append({
            "appointment_id": str(appt.id),
            "date": str(appt.appt_date),
            "time_slot": str(appt.time_slot),
            "pet_name": pet.name,
            "pet_species": pet.species,
            "client_name": client.name,
            "client_phone": client.phone,
            "client_email": client.email
        })

    return {
        "start_date": str(start_date),
        "end_date": str(end_date),
        "total_appointments": len(result),
        "appointments": result
    }