import { forwardRef, useId } from "react";
import type { InputProps } from "./Input.types";

const Input = forwardRef<HTMLInputElement, InputProps>(function Input(
  { label, error, id, className, ...props },
  ref
) {
  const generatedId = useId();
  const inputId = id ?? generatedId;

  return (
    <div className="w-full">
      <label htmlFor={inputId} className="mb-1 block text-sm text-slate-800">
        {label}
      </label>

      <input
        id={inputId}
        ref={ref}
        aria-invalid={Boolean(error)}
        className={`w-full border border-slate-300 bg-white px-3 py-2 text-sm text-slate-800 focus:border-brand-teal focus:outline-none ${
          className ?? ""
        }`}
        {...props}
      />

      {error && <p className="mt-1 text-xs text-slate-600">{error}</p>}
    </div>
  );
});

export default Input;
