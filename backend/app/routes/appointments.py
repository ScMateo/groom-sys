from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date
from app.core.database import get_db
from app.models.appointment import AppointmentModel
from app.models.pet import PetModel
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse,
    AvailabilityResponse,
    TimeSlot,
)

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])

# Horarios de trabajo en formato HH:MM
WORK_SLOTS = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

@router.get("/availability", response_model=AvailabilityResponse)
def get_availability(
    target_date: date = Query(..., alias="date", description="Fecha a consultar (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    # 1. Consultar en la BD las horas reservadas para la fecha indicada
    existing_appointments = db.query(AppointmentModel.time_slot).filter(
        AppointmentModel.appt_date == target_date,
        AppointmentModel.status != "CANCELLED"
    ).all()

    # Extraer los slots ocupados
    booked_slots = {app.time_slot for app in existing_appointments}

    # 2. Armar la disponibilidad de cada slot
    slots = [
        TimeSlot(
            time=slot,
            available=(slot not in booked_slots)
        )
        for slot in WORK_SLOTS
    ]

    return AvailabilityResponse(date=target_date, slots=slots)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=AppointmentResponse)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    # 1. Verificar que la mascota exista
    pet = db.query(PetModel).filter(PetModel.id == payload.pet_id).first()
    if not pet:
        raise HTTPException(status_code=400, detail="La mascota no existe")

    # 2. Verificar que el horario no esté ya reservado
    existing = db.query(AppointmentModel).filter(
        AppointmentModel.appt_date == payload.appt_date,
        AppointmentModel.time_slot == payload.time_slot,
        AppointmentModel.status != "CANCELLED",
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="El horario ya está reservado")

    # 3. Armar la nueva cita
    appointment = AppointmentModel(
        pet_id=payload.pet_id,
        appt_date=payload.appt_date,
        time_slot=payload.time_slot,
        status="confirmada",
    )

    # 4. Guardar en la BD (respaldo ante condición de carrera con el mismo horario)
    try:
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="El horario ya está reservado")

    # 5. Responder con los datos de la cita creada
    return {
        "appointment_id": appointment.id,
        "pet_id": appointment.pet_id,
        "appt_date": appointment.appt_date,
        "time_slot": appointment.time_slot,
        "status": appointment.status,
    }