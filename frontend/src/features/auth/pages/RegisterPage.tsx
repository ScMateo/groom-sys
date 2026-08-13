import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Navigate, useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

import Button from "../../../components/ui/Button";
import Input from "../../../components/ui/Input";
import { createClient } from "../api/clientsApi";
import { registerSchema, type RegisterFormValues } from "../schemas/registerSchema";
import type { RequestStatus } from "../../../types/request-status";

interface LocationState {
  email: string;
}

// Forma en la que el backend devuelve los errores (ver API_CONTRACT.md).
interface ApiErrorResponse {
  code?: string;
  message?: string;
}

function RegisterPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const state = location.state as LocationState | null;

  const [status, setStatus] = useState<RequestStatus>("idle");
  const [submitError, setSubmitError] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    mode: "onChange",
  });

  // Si se llega a esta ruta sin pasar por la verificación de correo, se regresa al inicio.
  if (!state?.email) {
    return <Navigate to="/" replace />;
  }

  const onSubmit = handleSubmit(async ({ name, phone }) => {
    setStatus("loading");
    setSubmitError("");

    try {
      const client = await createClient({ name, email: state.email, phone });
      navigate("/booking", { state: client });
    } catch (error) {
      setStatus("error");

      if (axios.isAxiosError(error)) {
        const apiError: ApiErrorResponse | undefined = error.response?.data;
        setSubmitError(apiError?.message ?? "No se pudo crear el usuario. Intenta nuevamente.");
        return;
      }

      setSubmitError("No se pudo crear el usuario. Intenta nuevamente.");
    }
  });

  return (
    <main className="min-h-screen bg-brand-beige p-4">
      <div className="mx-auto w-full max-w-md border border-brand-teal-light bg-white p-6">
        <h1 className="text-xl text-brand-teal">Crea tu cuenta</h1>
        <p className="mt-1 text-sm text-slate-700">
          No encontramos una cuenta con <span className="text-brand-teal">{state.email}</span>, completa
          tus datos para continuar.
        </p>

        <form className="mt-4 space-y-4" noValidate onSubmit={onSubmit}>
          <Input
            label="Tu nombre"
            placeholder="Daniel Rojas"
            error={errors.name?.message}
            {...register("name")}
          />
          <Input
            label="Tu teléfono"
            placeholder="312340000"
            error={errors.phone?.message}
            {...register("phone")}
          />

          {status === "error" && submitError && (
            <p className="text-sm text-brand-teal">{submitError}</p>
          )}

          <Button type="submit" className="w-full" disabled={status === "loading"}>
            {status === "loading" ? "Creando cuenta..." : "Crear cuenta y continuar"}
          </Button>
        </form>
      </div>
    </main>
  );
}

export default RegisterPage;
