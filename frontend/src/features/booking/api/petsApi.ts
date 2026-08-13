import { apiClient } from "../../../api/client";

export type PetSpecies = "dog" | "cat";

// El backend guarda la especie en español, así que la traducimos antes de enviarla.
export const SPECIES_LABEL: Record<PetSpecies, string> = {
  dog: "Perro",
  cat: "Gato",
};

export interface CreatePetInput {
  clientId: string;
  petName: string;
  species: PetSpecies;
}

export interface CreatePetResponse {
  pet_id: string;
  client_id: string;
  is_new: boolean;
}

export async function createPet(input: CreatePetInput): Promise<CreatePetResponse> {
  // el cliente ya existe (verificado/creado en las pantallas previas), solo falta la mascota.
  const response = await apiClient.post("/api/pets", {
    client_id: input.clientId,
    pet_name: input.petName,
    pet_species: SPECIES_LABEL[input.species],
  });

  return response.data;
}

export interface ClientPet {
  id: string;
  name: string;
  species: string;
  created_at: string;
}

export async function fetchClientPets(email: string): Promise<ClientPet[]> {
  const response = await apiClient.get("/api/pets", { params: { email } });
  return response.data.pets;
}
