import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useNavigate } from "react-router-dom";

import Button from "../../../components/ui/Button";
import Input from "../../../components/ui/Input";
import { checkEmail } from "../api/clientsApi";
import { emailCheckSchema, type EmailCheckFormValues } from "../schemas/emailCheckSchema";
import type { RequestStatus } from "../../../types/request-status";
import AdminLoginModal from "../../admin/components/AdminLoginModal";

function EmailCheckPage() {
  const navigate = useNavigate();
  const [status, setStatus] = useState<RequestStatus>("idle");
  const [submitError, setSubmitError] = useState("");
  const [isAdminModalOpen, setIsAdminModalOpen] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<EmailCheckFormValues>({
    resolver: zodResolver(emailCheckSchema),
    mode: "onChange",
  });

  const onSubmit = handleSubmit(async ({ email }) => {
    setStatus("loading");
    setSubmitError("");

    try {
      const result = await checkEmail(email);

      if (result.exists && result.client) {
        navigate("/booking", { state: result.client });
        return;
      }

      navigate("/register", { state: { email } });
    } catch {
      setStatus("error");
      setSubmitError("No se pudo verificar el correo. Intenta nuevamente.");
    }
  });

  return (
    <main className="min-h-screen bg-brand-beige p-4">
      <button
        type="button"
        onClick={() => setIsAdminModalOpen(true)}
        className="mb-4 border border-brand-teal bg-brand-teal px-4 py-2 text-sm text-white"
      >
        Admin
      </button>

      <div className="mx-auto w-full max-w-md border border-brand-teal-light bg-white p-6">
        <h1 className="text-xl text-brand-teal">Bienvenido</h1>
        <p className="mt-1 text-sm text-slate-700">Ingresa tu correo para continuar</p>

        <form className="mt-4 space-y-4" noValidate onSubmit={onSubmit}>
          <Input
            label="Tu correo"
            type="email"
            placeholder="daniel@example.com"
            error={errors.email?.message}
            {...register("email")}
          />

          {status === "error" && submitError && (
            <p className="text-sm text-brand-teal">{submitError}</p>
          )}

          <Button type="submit" className="w-full" disabled={status === "loading"}>
            {status === "loading" ? "Verificando..." : "Continuar"}
          </Button>
        </form>
      </div>

      {isAdminModalOpen && <AdminLoginModal onClose={() => setIsAdminModalOpen(false)} />}
    </main>
  );
}

export default EmailCheckPage;
