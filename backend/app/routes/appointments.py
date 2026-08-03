from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.models.appointment import AppointmentModel
from app.schemas.appointment import AvailabilityResponse, TimeSlot

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