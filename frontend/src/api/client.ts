import axios from "axios";

// Instancia única de axios que usan todas las llamadas al backend.
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
  headers: {
    "Content-Type": "application/json",
  },
});
