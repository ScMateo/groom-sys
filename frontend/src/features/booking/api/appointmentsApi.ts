import { apiClient } from "../../../api/client";

export interface TimeSlot {
  time: string;
  available: boolean;
}

interface DayAvailabilityResponse {
  date: string;
  slots: TimeSlot[];
}

export async function fetchDayAvailability(date: string): Promise<TimeSlot[]> {
  // GET /api/appointments/availability?date=... devuelve los horarios del día y si están libres.
  const response = await apiClient.get("/api/appointments/availability", {
    params: { date },
  });
  const availability: DayAvailabilityResponse = response.data;

  return availability.slots;
}

export interface CreateAppointmentInput {
  petId: string;
  date: string;
  time: string;
}

export interface CreateAppointmentResponse {
  appointment_id: string;
  pet_id: string;
  appt_date: string;
  time_slot: string;
  status: string;
}

export async function createAppointment(
  input: CreateAppointmentInput
): Promise<CreateAppointmentResponse> {
  // reserva la cita para la mascota, fecha y hora elegidas.
  const response = await apiClient.post("/api/appointments", {
    pet_id: input.petId,
    appt_date: input.date,
    time_slot: input.time,
  });

  return response.data;
}
