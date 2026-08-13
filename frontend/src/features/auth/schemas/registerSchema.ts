import { z } from "zod";

// Reglas de validación del formulario de registro de un nuevo cliente.
export const registerSchema = z.object({
  name: z.string().trim().min(2, "El nombre debe tener al menos 2 caracteres"),
  phone: z
    .string()
    .trim()
    .regex(/^3\d{9}$/, "El teléfono debe ser un celular válido (10 dígitos, inicia en 3)"),
});

export type RegisterFormValues = z.infer<typeof registerSchema>;
