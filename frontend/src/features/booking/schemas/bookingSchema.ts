import { z } from "zod";

// Reglas de validación del formulario de reserva.
export const bookingSchema = z.object({
  clientName: z.string().trim().min(2, "El nombre debe tener al menos 2 caracteres"),
  clientEmail: z.string().trim().email("Correo inválido"),
  clientPhone: z
    .string()
    .trim()
    .regex(/^3\d{9}$/, "El teléfono debe ser un celular válido (10 dígitos, inicia en 3)"),
  petName: z.string().trim().min(2, "El nombre debe tener al menos 2 caracteres"),
});

export type BookingFormValues = z.infer<typeof bookingSchema>;
