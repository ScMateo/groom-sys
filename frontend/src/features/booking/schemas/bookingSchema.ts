import { z } from "zod";

// Reglas de validación del formulario de reserva (el cliente ya fue identificado antes).
export const bookingSchema = z.object({
  petName: z.string().trim().min(2, "El nombre debe tener al menos 2 caracteres"),
});

export type BookingFormValues = z.infer<typeof bookingSchema>;
