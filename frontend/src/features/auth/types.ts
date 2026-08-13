// Datos del cliente ya identificado (existente o recién creado) que se pasan entre pantallas via router state.
export interface ClientState {
  id: string;
  name: string;
  email: string;
  phone: string;
}
