import { api } from "./client";
import type { ValidationResponse } from "../types";

export async function validateSolution(
  instance: Record<string, unknown>,
  solution: Record<string, unknown>,
): Promise<ValidationResponse> {
  const { data } = await api.post<ValidationResponse>("/validate", { instance, solution });
  return data;
}
