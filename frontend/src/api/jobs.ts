import { api } from "./client";
import type { Job, JobListResponse, SolveResponse } from "../types";

export async function submitJob(
  instance: Record<string, unknown>,
  options: { seed?: number; name?: string; autoValidate?: boolean; timeLimit?: number } = {},
): Promise<SolveResponse> {
  const params = new URLSearchParams();
  if (options.seed !== undefined) params.set("seed", String(options.seed));
  if (options.name) params.set("name", options.name);
  if (options.autoValidate) params.set("auto_validate", "true");
  if (options.timeLimit !== undefined) params.set("time_limit", String(options.timeLimit));
  const { data } = await api.post<SolveResponse>(`/solve?${params.toString()}`, instance);
  return data;
}

export async function getJob(jobId: string): Promise<Job> {
  const { data } = await api.get<Job>(`/jobs/${jobId}`);
  return data;
}

export async function listJobs(): Promise<JobListResponse> {
  const { data } = await api.get<JobListResponse>("/jobs");
  return data;
}
