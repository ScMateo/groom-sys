import { z } from "zod";

// Regla de validación del formulario de verificación de correo.
export const emailCheckSchema = z.object({
  email: z.string().trim().email("Correo inválido"),
});

export type EmailCheckFormValues = z.infer<typeof emailCheckSchema>;
