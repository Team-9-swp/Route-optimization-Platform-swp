import { useEffect, useState } from "react";
import { Eye, Plus, Clock, CheckCircle2, XCircle, Loader2 } from "lucide-react";
import { listJobs } from "../../api/jobs";
import type { Job, JobStatus } from "../../types";
import type { Page } from "../App";

const statusConfig: Record<JobStatus, { label: string; bg: string; color: string; icon: React.ReactNode }> = {
  completed: { label: "Completed", bg: "#DCFCE7", color: "#15803D", icon: <CheckCircle2 size={12} /> },
  running: { label: "Running", bg: "#DBEAFE", color: "#1D4ED8", icon: <Loader2 size={12} className="animate-spin" /> },
  pending: { label: "Pending", bg: "#FEF9C3", color: "#A16207", icon: <Clock size={12} /> },
  failed: { label: "Failed", bg: "#FEE2E2", color: "#B91C1C", icon: <XCircle size={12} /> },
};

function StatusBadge({ status }: { status: JobStatus }) {
  const cfg = statusConfig[status] ?? statusConfig.pending;
  return (
    <span
      className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium"
      style={{ background: cfg.bg, color: cfg.color }}
    >
      {cfg.icon}
      {cfg.label}
    </span>
  );
}

interface Props {
  navigate: (p: Page) => void;
}

export function Dashboard({ navigate }: Props) {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const response = await listJobs();
        if (!cancelled) setJobs(response.items);
      } catch (err) {
        if (!cancelled) setError(err instanceof Error ? err.message : "Failed to load jobs");
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }
    load();
    const interval = setInterval(load, 2000);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, []);

  const completedCount = jobs.filter((j) => j.status === "completed").length;
  const runningCount = jobs.filter((j) => j.status === "running").length;
  const failedCount = jobs.filter((j) => j.status === "failed").length;

  if (isLoading) return <p className="p-6 text-gray-600">Loading jobs…</p>;
  if (error) return <p className="p-6 text-red-600">{error}</p>;

  return (
    <div className="min-h-screen" style={{ background: "#F9FAFB" }}>
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="flex items-center justify-between mb-6">
          <h1 style={{ color: "#111827", fontSize: 24, fontWeight: 600, margin: 0 }}>Jobs</h1>
          <button
            onClick={() => navigate({ name: "new-job" })}
            className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all hover:opacity-90 active:scale-95"
            style={{ background: "#2563EB", color: "#fff", border: "none", cursor: "pointer" }}
          >
            <Plus size={16} />
            New Job
          </button>
        </div>

        <div
          className="rounded-xl overflow-hidden"
          style={{ background: "#fff", border: "1px solid #E5E7EB", boxShadow: "0 1px 4px rgba(0,0,0,0.05)" }}
        >
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ borderBottom: "1px solid #F3F4F6" }}>
                {["ID", "Name", "Status", "Created", "Objective", "Actions"].map((col) => (
                  <th
                    key={col}
                    style={{
                      padding: "12px 16px",
                      textAlign: "left",
                      fontSize: 12,
                      fontWeight: 600,
                      color: "#6B7280",
                      textTransform: "uppercase",
                      letterSpacing: "0.05em",
                    }}
                  >
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {jobs.map((job, i) => (
                <tr
                  key={job.job_id}
                  style={{ borderBottom: i < jobs.length - 1 ? "1px solid #F9FAFB" : "none" }}
                  className="hover:bg-gray-50 transition-colors"
                >
                  <td style={{ padding: "14px 16px" }}>
                    <span
                      className="font-mono text-xs"
                      style={{ color: "#6B7280", background: "#F3F4F6", padding: "2px 6px", borderRadius: 4 }}
                    >
                      {job.job_id.slice(0, 8)}…
                    </span>
                  </td>
                  <td style={{ padding: "14px 16px", fontSize: 14, color: "#111827" }}>
                    {job.name || <span style={{ color: "#D1D5DB" }}>—</span>}
                  </td>
                  <td style={{ padding: "14px 16px" }}>
                    <StatusBadge status={job.status} />
                  </td>
                  <td style={{ padding: "14px 16px", fontSize: 13, color: "#6B7280" }}>
                    {new Date(job.created_at).toLocaleString()}
                  </td>
                  <td style={{ padding: "14px 16px", fontSize: 14, color: "#111827" }}>
                    {job.objective_value ?? <span style={{ color: "#D1D5DB" }}>—</span>}
                  </td>
                  <td style={{ padding: "14px 16px" }}>
                    <button
                      onClick={() => {
                        if (job.status === "completed") navigate({ name: "job-detail", id: job.job_id });
                      }}
                      disabled={job.status !== "completed"}
                      aria-label={job.status === "completed" ? `View job ${job.job_id}` : `Job ${job.job_id} is not completed yet`}
                      title={job.status === "completed" ? "View completed job" : "Available when the solver has completed"}
                      className="flex items-center gap-1 text-sm font-medium enabled:hover:underline disabled:opacity-40"
                      style={{ color: "#2563EB", background: "none", border: "none", cursor: job.status === "completed" ? "pointer" : "not-allowed", padding: 0 }}
                    >
                      <Eye size={14} />
                      View
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="grid grid-cols-4 gap-4 mt-6">
          {[
            { label: "Total Jobs", value: String(jobs.length), color: "#6B7280" },
            { label: "Completed", value: String(completedCount), color: "#15803D" },
            { label: "Running", value: String(runningCount), color: "#1D4ED8" },
            { label: "Failed", value: String(failedCount), color: "#B91C1C" },
          ].map((stat) => (
            <div
              key={stat.label}
              className="rounded-xl p-4"
              style={{ background: "#fff", border: "1px solid #E5E7EB" }}
            >
              <p style={{ fontSize: 12, color: "#6B7280", margin: "0 0 4px 0", fontWeight: 500 }}>{stat.label}</p>
              <p style={{ fontSize: 24, fontWeight: 600, color: stat.color, margin: 0 }}>{stat.value}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
