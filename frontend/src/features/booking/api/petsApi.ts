import { apiClient } from "../../../api/client";

export type PetSpecies = "dog" | "cat";

// El backend guarda la especie en español, así que la traducimos antes de enviarla.
export const SPECIES_LABEL: Record<PetSpecies, string> = {
  dog: "Perro",
  cat: "Gato",
};

export interface CreatePetInput {
  clientName: string;
  clientEmail: string;
  clientPhone: string;
  petName: string;
  species: PetSpecies;
}

export interface CreatePetResponse {
  pet_id: string;
  client_email: string;
  pet_name: string;
  pet_species: string;
}

export async function createPet(input: CreatePetInput): Promise<CreatePetResponse> {
  // verifica si existe el cliente y su mascota.
  const response = await apiClient.post("/api/pets", {
    client_name: input.clientName,
    client_email: input.clientEmail,
    client_phone: input.clientPhone,
    pet_name: input.petName,
    pet_species: SPECIES_LABEL[input.species],
  });

  return response.data;
}
