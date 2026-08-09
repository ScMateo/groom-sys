from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.models.appointment import AppointmentModel
from app.models.pet import PetModel
from app.schemas.appointment import (
    AppointmentCreate,
    AppointmentResponse,
    AvailabilityResponse,
    DailyAppointmentResponse,
    TimeSlot,
)

router = APIRouter(prefix="/api/appointments", tags=["Appointments"])

WORK_SLOTS = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]


@router.get("/availability", response_model=AvailabilityResponse)
def get_availability(
    target_date: date = Query(..., alias="date", description="Fecha a consultar (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    existing_appointments = db.query(AppointmentModel.time_slot).filter(
        AppointmentModel.appt_date == target_date,
        AppointmentModel.status != "CANCELLED"
    ).all()

    booked_slots = {app.time_slot for app in existing_appointments}

    slots = [
        TimeSlot(
            time=slot,
            available=(slot not in booked_slots)
        )
        for slot in WORK_SLOTS
    ]

    return AvailabilityResponse(date=target_date, slots=slots)


@router.get("/daily", response_model=List[DailyAppointmentResponse])
def get_daily_appointments(
    target_date: date = Query(..., alias="date", description="Fecha a consultar (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    Obtiene la agenda diaria con un JOIN optimizado entre Citas, Mascotas y Clientes
    para la vista del Dashboard.
    """
    appointments = (
        db.query(AppointmentModel)
        .options(
            joinedload(AppointmentModel.pet).joinedload(PetModel.client)
        )
        .filter(
            AppointmentModel.appt_date == target_date,
            AppointmentModel.status != "CANCELLED"
        )
        .order_by(AppointmentModel.time_slot.asc())
        .all()
    )

    return appointments


@router.post("", status_code=status.HTTP_201_CREATED, response_model=AppointmentResponse)
def create_appointment(
    payload: AppointmentCreate, 
    db: Session = Depends(get_db)
):
    if payload.time_slot not in WORK_SLOTS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El horario seleccionado esta fuera del rango de atencion"
        )

    pet = db.query(PetModel).filter(PetModel.id == payload.pet_id).first()
    if not pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="La mascota especificada no existe"
        )

    existing = db.query(AppointmentModel).filter(
        AppointmentModel.appt_date == payload.appt_date,
        AppointmentModel.time_slot == payload.time_slot,
        AppointmentModel.status != "CANCELLED",
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="El horario ya se encuentra reservado"
        )

    appointment = AppointmentModel(
        pet_id=payload.pet_id,
        appt_date=payload.appt_date,
        time_slot=payload.time_slot,
        status="CONFIRMED",
    )

    try:
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="El horario ya fue reservado por otro usuario en este instante"
        )

    return appointment