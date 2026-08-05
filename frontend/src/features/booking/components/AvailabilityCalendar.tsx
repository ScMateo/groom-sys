import clsx from "clsx";
import { getDate, getDay, getDaysInMonth, isBefore, startOfDay } from "date-fns";

import { ChevronLeftIcon, ChevronRightIcon } from "../../../components/common/icons";
import { MONTH_NAMES, WEEKDAYS, formatDateKey } from "../utils/date";

interface AvailabilityCalendarProps {
  year: number;
  month: number;
  selectedDate: string | null;
  onSelectDate: (date: Date, isSunday: boolean, isAvailable: boolean) => void;
  onPrevMonth: () => void;
  onNextMonth: () => void;
  prevDisabled?: boolean;
  nextDisabled?: boolean;
}

function AvailabilityCalendar({
  year,
  month,
  selectedDate,
  onSelectDate,
  onPrevMonth,
  onNextMonth,
  prevDisabled = false,
  nextDisabled = false,
}: AvailabilityCalendarProps) {
  const today = startOfDay(new Date());
  const daysInMonth = getDaysInMonth(new Date(year, month, 1));
  const startOffset = getDay(new Date(year, month, 1)); // día de la semana en que empieza el mes (0=domingo)

  // Arreglo de celdas espacios vacíos hasta el día 1, luego un elemento por cada día del mes.
  const cells: (Date | null)[] = [
    ...Array.from({ length: startOffset }, () => null),
    ...Array.from({ length: daysInMonth }, (_, index) => new Date(year, month, index + 1)),
  ];

  return (
    <div>
      <div className="mb-3 flex items-center justify-between">
        <button
          type="button"
          aria-label="Mes anterior"
          onClick={onPrevMonth}
          disabled={prevDisabled}
          className="border border-slate-300 px-2 py-1 text-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          <ChevronLeftIcon className="h-4 w-4" />
        </button>

        <p className="text-sm text-slate-800">
          {MONTH_NAMES[month]} {year}
        </p>

        <button
          type="button"
          aria-label="Mes siguiente"
          onClick={onNextMonth}
          disabled={nextDisabled}
          className="border border-slate-300 px-2 py-1 text-sm disabled:cursor-not-allowed disabled:opacity-50"
        >
          <ChevronRightIcon className="h-4 w-4" />
        </button>
      </div>

      <div className="grid grid-cols-7 text-center text-xs text-slate-600">
        {WEEKDAYS.map((day) => (
          <span key={day}>{day}</span>
        ))}
      </div>

      <div className="mt-2 grid grid-cols-7 gap-y-1">
        {cells.map((date, index) => {
          if (!date) {
            return <span key={`empty-${index}`} />;
          }

          const dateKey = formatDateKey(date);
          const isSunday = getDay(date) === 0;
          const isPast = isBefore(date, today);
          const isAvailable = !isSunday && !isPast; // no se atiende domingos ni días que ya pasaron
          const isSelected = selectedDate === dateKey;
          const isBlocked = !isAvailable;

          return (
            <div key={dateKey} className="flex justify-center">
              <button
                type="button"
                onClick={() => onSelectDate(date, isSunday, isAvailable)}
                disabled={isBlocked && !isSunday}
                className={clsx(
                  "flex h-8 w-8 items-center justify-center border border-slate-300 text-sm",
                  isSelected && "bg-slate-200",
                  !isSelected && isBlocked && "cursor-not-allowed opacity-40"
                )}
              >
                {getDate(date)}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default AvailabilityCalendar;
