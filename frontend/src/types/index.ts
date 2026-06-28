export type JobStatus = "pending" | "running" | "completed" | "failed";
export type ValidationStatus = "pending" | "passed" | "failed";

export interface Job {
  job_id: string;
  status: JobStatus;
  name?: string;
  created_at: string;
  input_data?: Record<string, unknown>;
  seed?: number;
  started_at?: string;
  finished_at?: string;
  result?: Record<string, unknown>;
  error?: string;
  objective_value?: number;
  validation_status?: ValidationStatus;
  validation_report?: Record<string, unknown>;
  unserved_optional?: number[];
}

export interface JobListResponse {
  items: Job[];
  total: number;
  page: number;
  page_size: number;
}

export interface SolveResponse {
  job_id: string;
  status: JobStatus;
  created_at: string;
  name?: string;
}

export interface ValidationResponse {
  passed: boolean;
  objective_value?: number;
  violations: string[];
  report: Record<string, unknown>;
}
