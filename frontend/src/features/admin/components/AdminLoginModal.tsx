import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import Button from "../../../components/ui/Button";
import Input from "../../../components/ui/Input";
import { adminLogin } from "../api/adminApi";
import { adminLoginSchema, type AdminLoginFormValues } from "../schemas/adminLoginSchema";
import type { RequestStatus } from "../../../types/request-status";

interface ApiErrorResponse {
  code?: string;
  message?: string;
}

interface AdminLoginModalProps {
  onClose: () => void;
}

function AdminLoginModal({ onClose }: AdminLoginModalProps) {
  const navigate = useNavigate();
  const [status, setStatus] = useState<RequestStatus>("idle");
  const [submitError, setSubmitError] = useState("");

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<AdminLoginFormValues>({
    resolver: zodResolver(adminLoginSchema),
    mode: "onChange",
  });

  const onSubmit = handleSubmit(async ({ username, password }) => {
    setStatus("loading");
    setSubmitError("");

    try {
      await adminLogin({ username, password });
      navigate("/admin");
    } catch (error) {
      setStatus("error");

      if (axios.isAxiosError(error)) {
        const apiError: ApiErrorResponse | undefined = error.response?.data;
        setSubmitError(apiError?.message ?? "Correo o contraseña incorrectos.");
        return;
      }

      setSubmitError("Correo o contraseña incorrectos.");
    }
  });

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 p-4">
      <div className="w-full max-w-sm border border-brand-teal-light bg-white p-6">
        <div className="flex items-start justify-between">
          <h2 className="text-xl text-brand-teal">Acceso administrador</h2>
          <button
            type="button"
            onClick={onClose}
            aria-label="Cerrar"
            className="text-slate-500 hover:text-slate-800"
          >
            ✕
          </button>
        </div>
        <p className="mt-1 text-sm text-slate-700">Ingresa tus credenciales de administrador</p>

        <form className="mt-4 space-y-4" noValidate onSubmit={onSubmit}>
          <Input
            label="Correo"
            type="email"
            placeholder="admin@example.com"
            error={errors.username?.message}
            {...register("username")}
          />
          <Input
            label="Contraseña"
            type="password"
            error={errors.password?.message}
            {...register("password")}
          />

          {status === "error" && submitError && (
            <p className="text-sm text-brand-teal">{submitError}</p>
          )}

          <Button type="submit" className="w-full" disabled={status === "loading"}>
            {status === "loading" ? "Ingresando..." : "Ingresar"}
          </Button>
        </form>
      </div>
    </div>
  );
}

export default AdminLoginModal;
