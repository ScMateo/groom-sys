import { z } from "zod";

// Coincide con las restricciones de AdminLoginRequest en el backend.
export const adminLoginSchema = z.object({
  username: z.string().trim().min(3, "Debe tener al menos 3 caracteres"),
  password: z.string().min(4, "Debe tener al menos 4 caracteres"),
});

export type AdminLoginFormValues = z.infer<typeof adminLoginSchema>;
