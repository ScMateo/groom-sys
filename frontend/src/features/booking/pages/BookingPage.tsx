import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { addMonths, getMonth, getYear, isSameMonth, startOfMonth, subMonths } from "date-fns";
import axios from "axios";

import Button from "../../../components/ui/Button";
import Input from "../../../components/ui/Input";
import { ChevronLeftIcon } from "../../../components/common/icons";
import AvailabilityCalendar from "../components/AvailabilityCalendar";
import TimeSlotPicker from "../components/TimeSlotPicker";
import { createPet, type PetSpecies } from "../api/petsApi";
import { createAppointment, fetchDayAvailability, type TimeSlot } from "../api/appointmentsApi";
import { formatDateKey } from "../utils/date";
import { bookingSchema, type BookingFormValues } from "../schemas/bookingSchema";
import type { RequestStatus } from "../../../types/request-status";

// La página tiene 2 pasos: primero se llena el formulario y luego se elige fecha/hora.
type Step = "form" | "schedule";

// Lista de especies para no repetir el mismo botón dos veces en el JSX.
const SPECIES_OPTIONS: { value: PetSpecies; label: string }[] = [
  { value: "dog", label: "Perro" },
  { value: "cat", label: "Gato" },
];

// Forma en la que el backend devuelve los errores (ver API_CONTRACT.md).
interface ApiErrorResponse {
  code?: string;
  message?: string;
}

function BookingPage() {
  // En qué paso está el usuario: llenando el formulario o eligiendo fecha/hora.
  const [step, setStep] = useState<Step>("form");

  // Especie elegida (no es parte del formulario de react-hook-form, se maneja aparte).
  const [species, setSpecies] = useState<PetSpecies | null>(null);
  const [speciesTouched, setSpeciesTouched] = useState(false);

  // Mes que se muestra en el calendario y día/hora elegidos por el usuario.
  const [calendarDate, setCalendarDate] = useState(() => startOfMonth(new Date()));
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const [selectedTime, setSelectedTime] = useState<string | null>(null);
  const [showSundayNotice, setShowSundayNotice] = useState(false);

  // Horarios disponibles para el día elegido (se piden al backend).
  const [slots, setSlots] = useState<TimeSlot[] | null>(null);
  const [slotsFetchError, setSlotsFetchError] = useState(false);

  // Estado del envío final (crear mascota + crear cita).
  const [status, setStatus] = useState<RequestStatus>("idle");
  const [submitError, setSubmitError] = useState("");
  const [success, setSuccess] = useState(false);

  // react-hook-form maneja los inputs del formulario y bookingSchema (zod) los valida.
  const {
    register,
    handleSubmit,
    getValues,
    formState: { errors },
  } = useForm<BookingFormValues>({
    resolver: zodResolver(bookingSchema),
    mode: "onChange",
  });

  const year = getYear(calendarDate);
  const month = getMonth(calendarDate);
  const isCurrentMonth = isSameMonth(calendarDate, new Date());

  // Traduce los 2 estados (slots y slotsFetchError) a un solo estado para pintar la UI.
  function getSlotsStatus(): RequestStatus {
    if (!selectedDate) return "idle";
    if (slotsFetchError) return "error";
    if (slots) return "success";
    return "loading";
  }
  const slotsStatus = getSlotsStatus();

  // pedir al back los horarios de ese día.
  useEffect(() => {
    if (!selectedDate) return;

    setSlots(null);
    setSlotsFetchError(false);

    fetchDayAvailability(selectedDate)
      .then((data) => {
        setSlots(data);
      })
      .catch(() => {
        setSlotsFetchError(true);
      });
  }, [selectedDate]);

  const resetDateSelection = () => {
    setShowSundayNotice(false);
    setSelectedDate(null);
    setSelectedTime(null);
    setSlots(null);
    setSlotsFetchError(false);
  };

  const handlePrevMonth = () => {
    if (isCurrentMonth || status === "loading") return;
    resetDateSelection();
    setCalendarDate((prev) => subMonths(prev, 1));
  };

  const handleNextMonth = () => {
    if (status === "loading") return;
    resetDateSelection();
    setCalendarDate((prev) => addMonths(prev, 1));
  };

  const handleSelectDate = (date: Date, isSunday: boolean, isAvailable: boolean) => {
    if (status === "loading") return;

    if (isSunday) {
      setShowSundayNotice(true);
      return;
    }

    if (!isAvailable) return;

    setShowSundayNotice(false);
    setSubmitError("");
    setSelectedTime(null);
    setSelectedDate(formatDateKey(date));
  };

  const handleGoToSchedule = handleSubmit(() => {
    setSpeciesTouched(true);
    if (!species) return;
    setStep("schedule");
  });

  const handleBackToForm = () => {
    if (status === "loading") return;
    setStep("form");
  };

  // Al confirmar: 1) crea la mascota, 2) crea la cita con ese pet_id.
  const handleConfirmBooking = async () => {
    if (!species || !selectedDate || !selectedTime || status === "loading") return;

    const data = getValues();

    setStatus("loading");
    setSubmitError("");

    try {
      const pet = await createPet({
        clientName: data.clientName,
        clientEmail: data.clientEmail,
        clientPhone: data.clientPhone,
        petName: data.petName,
        species,
      });

      await createAppointment({ petId: pet.pet_id, date: selectedDate, time: selectedTime });

      setStatus("success");
      setSuccess(true);
    } catch (error) {
      setStatus("error");

      // Si otra persona reservó el mismo horario justo antes que nosotros (409),
      // avisamos y recargamos la lista de horarios para que elija otro.
      if (axios.isAxiosError(error)) {
        const apiError: ApiErrorResponse | undefined = error.response?.data;

        if (apiError?.code === "SLOT_TAKEN" || error.response?.status === 409) {
          setSubmitError(apiError?.message ?? "El horario seleccionado ya fue reservado. Elige otro.");
          setSelectedTime(null);
          fetchDayAvailability(selectedDate).then(setSlots).catch(() => {});
          return;
        }

        setSubmitError(apiError?.message ?? "No se pudo agendar la cita. Intenta nuevamente.");
        return;
      }

      setSubmitError("No se pudo agendar la cita. Intenta nuevamente.");
    }
  };

  const canConfirm = selectedDate !== null && selectedTime !== null && status !== "loading";

  // Texto del botón final según en qué punto del flujo esté el usuario.
  function getConfirmButtonLabel(): string {
    if (status === "loading") return "Agendando...";
    if (!selectedDate) return "Selecciona un día";
    if (!selectedTime) return "Selecciona una hora";
    return "Agendar cita";
  }

  if (success) {
    return (
      <main className="min-h-screen bg-brand-beige p-4">
        <div className="mx-auto w-full max-w-md border border-brand-teal-light bg-white p-6 text-center">
          <h1 className="text-xl text-brand-teal">¡Cita agendada!</h1>
          <p className="mt-2 text-sm text-slate-700">
            Te esperamos el {selectedDate} a las {selectedTime}.
          </p>
        </div>
      </main>
    );
  }

  if (step === "form") {
    return (
      <main className="min-h-screen bg-brand-beige p-4">
        <div className="mx-auto w-full max-w-md border border-brand-teal-light bg-white p-4">
          <h1 className="text-xl text-brand-teal">Agenda tu cita</h1>
          <p className="mt-1 text-sm text-slate-700">Cuéntanos de ti y de tu mascota</p>

          <form className="mt-4 space-y-4" noValidate onSubmit={handleGoToSchedule}>
            <Input
              label="Tu nombre"
              placeholder="Daniel Rojas"
              error={errors.clientName?.message}
              {...register("clientName")}
            />
            <Input
              label="Tu correo"
              type="email"
              placeholder="daniel@example.com"
              error={errors.clientEmail?.message}
              {...register("clientEmail")}
            />
            <Input
              label="Tu teléfono"
              placeholder="312340000"
              error={errors.clientPhone?.message}
              {...register("clientPhone")}
            />

            <div>
              <span className="mb-2 block text-sm text-slate-800">Tipo de mascota</span>
              <div className="grid grid-cols-2 gap-3">
                {SPECIES_OPTIONS.map((option) => (
                  <button
                    key={option.value}
                    type="button"
                    onClick={() => {
                      setSpecies(option.value);
                      setSpeciesTouched(true);
                    }}
                    aria-pressed={species === option.value}
                    className={
                      species === option.value
                        ? "border border-brand-teal bg-brand-teal-light px-3 py-3 text-left text-brand-teal"
                        : "border border-slate-300 px-3 py-3 text-left text-slate-700"
                    }
                  >
                    {option.label}
                  </button>
                ))}
              </div>
              {speciesTouched && !species && (
                <p className="mt-1 text-xs text-red-500">Selecciona el tipo de mascota.</p>
              )}
            </div>

            <Input
              label="Nombre de tu mascota"
              placeholder="TONy"
              error={errors.petName?.message}
              {...register("petName")}
            />

            <Button type="submit" className="w-full">
              Guardar
            </Button>
          </form>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-brand-beige p-4">
      <div className="mx-auto w-full max-w-3xl border border-brand-teal-light bg-white p-4">
        <button
          type="button"
          onClick={handleBackToForm}
          className="mb-4 inline-flex items-center gap-1 border border-brand-teal-light px-2 py-1 text-sm text-brand-teal"
        >
          <ChevronLeftIcon className="h-4 w-4" />
          Volver
        </button>

        <h1 className="text-xl text-brand-teal">Elige fecha y hora</h1>
        <p className="mt-1 text-sm text-slate-700">
          Mascota: <span>{getValues("petName")}</span>
        </p>

        <div className="mt-4 space-y-4 md:flex md:gap-6 md:space-y-0">
          <div className="md:flex-1">
            <span className="mb-2 block text-sm text-slate-800">Elige el día</span>
            <AvailabilityCalendar
              year={year}
              month={month}
              selectedDate={selectedDate}
              onSelectDate={handleSelectDate}
              onPrevMonth={handlePrevMonth}
              onNextMonth={handleNextMonth}
              prevDisabled={isCurrentMonth || status === "loading"}
              nextDisabled={status === "loading"}
            />
            {showSundayNotice && (
              <p className="mt-3 text-sm text-brand-teal">Los domingos no hay atención.</p>
            )}
          </div>

          {selectedDate && (
            <div className="mt-6 md:mt-0 md:flex-1">
              <span className="mb-2 block text-sm text-slate-800">Elige la hora</span>

              {slotsStatus === "loading" && (
                <div className="py-4 text-sm text-slate-700">Cargando horarios...</div>
              )}

              {slotsStatus === "error" && (
                <p className="text-sm text-brand-teal">
                  No se pudieron cargar los horarios. Intenta de nuevo.
                </p>
              )}

              {slotsStatus === "success" && slots && (
                <TimeSlotPicker
                  slots={slots}
                  selectedTime={selectedTime}
                  onSelectTime={setSelectedTime}
                />
              )}
            </div>
          )}
        </div>

        {status === "error" && submitError && (
          <p className="mt-4 text-sm text-brand-teal">{submitError}</p>
        )}

        <Button className="mt-6 w-full" disabled={!canConfirm} onClick={handleConfirmBooking}>
          {getConfirmButtonLabel()}
        </Button>
      </div>
    </main>
  );
}

export default BookingPage;
