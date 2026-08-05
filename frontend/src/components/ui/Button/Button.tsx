import type { ButtonProps } from "./Button.types";

function Button({ children, className, ...props }: ButtonProps) {
  return (
    <button
      className={`border border-brand-teal bg-brand-teal px-3 py-2 text-sm text-white disabled:cursor-not-allowed disabled:opacity-50 ${
        className ?? ""
      }`}
      {...props}
    >
      {children}
    </button>
  );
}

export default Button;