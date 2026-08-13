import { apiClient } from "../../../api/client";

export interface AdminLoginInput {
  username: string;
  password: string;
}

export interface AdminLoginResponse {
  message: string;
  authenticated: boolean;
  username: string;
}

export async function adminLogin(input: AdminLoginInput): Promise<AdminLoginResponse> {
  const response = await apiClient.post("/api/admin/login", input);
  return response.data;
}
