from pydantic import BaseModel
from datetime import date, time
from typing import List
from uuid import UUID


# 1. Un horario puntual del día y si está disponible
class TimeSlot(BaseModel):
    time: str        
    available: bool  


# 2. Disponibilidad de todos los horarios para una fecha
class AvailabilityResponse(BaseModel):
    date: date
    slots: List[TimeSlot]


# 3. Datos que llegan al crear una cita
class AppointmentCreate(BaseModel):
    pet_id: UUID
    appt_date: date
    time_slot: str


# 4. Datos que se devuelven tras crear la cita
class AppointmentResponse(BaseModel):
    appointment_id: UUID
    pet_id: UUID
    appt_date: date
    time_slot: str
    status: str