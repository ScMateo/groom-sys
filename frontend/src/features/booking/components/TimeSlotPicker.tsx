import clsx from "clsx";

import type { TimeSlot } from "../api/appointmentsApi";

interface TimeSlotPickerProps {
  slots: TimeSlot[];
  selectedTime: string | null;
  onSelectTime: (time: string) => void;
}

function TimeSlotPicker({ slots, selectedTime, onSelectTime }: TimeSlotPickerProps) {
  // Pinta un botón por cada horario 
  return (
    <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
      {slots.map(({ time, available }) => {
        const isSelected = selectedTime === time;

        return (
          <button
            key={time}
            type="button"
            aria-pressed={isSelected}
            disabled={!available}
            onClick={() => onSelectTime(time)}
            className={clsx(
              "border border-slate-300 px-2 py-2 text-sm",
              isSelected && "bg-slate-200",
              !available && "cursor-not-allowed opacity-40"
            )}
          >
            {time}
          </button>
        );
      })}
    </div>
  );
}

export default TimeSlotPicker;
