from datetime import date
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


# 1. Un horario puntual del dia y su disponibilidad
class TimeSlot(BaseModel):
    time: str
    available: bool


# 2. Respuesta de disponibilidad por fecha
class AvailabilityResponse(BaseModel):
    date: date
    slots: List[TimeSlot]


# 3. Payload de entrada para agendar una cita
class AppointmentCreate(BaseModel):
    pet_id: UUID
    appt_date: date
    time_slot: str


# 4. Respuesta basica de cita creada
class AppointmentResponse(BaseModel):
    id: UUID
    pet_id: UUID
    appt_date: date
    time_slot: str
    status: str

    model_config = ConfigDict(from_attributes=True)


# 5. Esquemas anidados para el Dashboard (JOIN)
class ClientSummary(BaseModel):
    id: UUID
    name: str  # <--- Corregido: 'name' en lugar de 'full_name'
    phone: Optional[str] = None
    email: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PetSummary(BaseModel):
    id: UUID
    name: str
    species: str
    client: ClientSummary

    model_config = ConfigDict(from_attributes=True)


class DailyAppointmentResponse(BaseModel):
    id: UUID
    appt_date: date
    time_slot: str
    status: str
    pet: PetSummary

    model_config = ConfigDict(from_attributes=True)