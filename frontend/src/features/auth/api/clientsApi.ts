import { apiClient } from "../../../api/client";

export interface ClientData {
  id: string;
  name: string;
  email: string;
  phone: string;
}

export interface CheckEmailResponse {
  exists: boolean;
  message: string;
  client: ClientData | null;
}

export interface CreateClientInput {
  name: string;
  email: string;
  phone: string;
}

export async function checkEmail(email: string): Promise<CheckEmailResponse> {
  const response = await apiClient.post("/api/clients/check-email", { email });
  return response.data;
}

export async function createClient(input: CreateClientInput): Promise<ClientData> {
  const response = await apiClient.post("/api/clients", input);
  return response.data;
}
