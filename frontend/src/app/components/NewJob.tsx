import { useState } from "react";
import { Upload, Loader2, AlertCircle } from "lucide-react";
import { submitJob } from "../../api/jobs";
import type { Page } from "../App";

const PLACEHOLDER_JSON = JSON.stringify(
  {
    vehicle_capacity: 100,
    vehicle_speed: 1,
    loader_speed: 1,
    vehicle_shift_size: 240,
    loader_shift_size: 240,
    depot: { x: 0, y: 0, load_time: 0 },
    orders: [
      {
        id: 1,
        x: 3,
        y: 4,
        volume: 10,
        time_window: [0, 120],
        vehicle_service_time: 5,
        loader_cnt: 0,
        loader_service_time: 0,
        optional: 0,
      },
      {
        id: 2,
        x: 7,
        y: 2,
        volume: 15,
        time_window: [0, 120],
        vehicle_service_time: 5,
        loader_cnt: 0,
        loader_service_time: 0,
        optional: 0,
      },
    ],
    weights: {
      vehicle_salary: 1,
      loader_salary: 1,
      fuel_cost: 1,
      loader_work: 1,
      optional_order_penalty: 1,
    },
  },
  null,
  2,
);

interface Props {
  navigate: (p: Page) => void;
}

export function NewJob({ navigate }: Props) {
  const [json, setJson] = useState("");
  const [name, setName] = useState("");
  const [seed, setSeed] = useState("42");
  const [autoValidate, setAutoValidate] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit() {
    setError("");
    if (!json.trim()) {
      setError("Please provide Instance JSON before running the solver.");
      return;
    }
    let instance: Record<string, unknown>;
    try {
      instance = JSON.parse(json);
    } catch {
      setError("Invalid JSON — please check the Instance JSON field.");
      return;
    }
    setSubmitting(true);
    try {
      const response = await submitJob(instance, {
        seed: Number(seed) || 42,
        name: name || undefined,
        autoValidate,
      });
      navigate({ name: "job-detail", id: response.job_id });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit job");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen" style={{ background: "#F9FAFB" }}>
      <div className="max-w-3xl mx-auto px-6 py-8">
        <h1 style={{ color: "#111827", fontSize: 24, fontWeight: 600, marginBottom: 24 }}>New Job</h1>

        <div
          className="rounded-xl p-8"
          style={{ background: "#fff", border: "1px solid #E5E7EB", boxShadow: "0 1px 4px rgba(0,0,0,0.05)" }}
        >
          <div className="mb-5">
            <label style={{ display: "block", marginBottom: 6, fontSize: 14, fontWeight: 600, color: "#111827" }}>
              Instance JSON
            </label>
            <textarea
              rows={12}
              value={json}
              onChange={(e) => setJson(e.target.value)}
              placeholder={PLACEHOLDER_JSON}
              className="w-full rounded-lg border resize-y focus:outline-none focus:ring-2"
              style={{
                border: error && !json.trim() ? "1px solid #DC2626" : "1px solid #E5E7EB",
                padding: "10px 12px",
                color: "#111827",
                background: "#F9FAFB",
                fontFamily: "'JetBrains Mono', monospace",
                fontSize: 12.5,
                lineHeight: 1.6,
              }}
            />
          </div>

          <div className="mb-6">
            <label style={{ display: "block", marginBottom: 6, fontSize: 14, fontWeight: 600, color: "#111827" }}>
              Upload JSON file
            </label>
            <label
              className="flex items-center gap-2 cursor-pointer rounded-lg px-4 py-3 border-2 border-dashed transition-colors"
              style={{ borderColor: "#D1D5DB", color: "#6B7280", fontSize: 14 }}
            >
              <Upload size={16} />
              <span>Click to upload or drag and drop</span>
              <input
                type="file"
                accept=".json"
                className="sr-only"
                onChange={(e) => {
                  const file = e.target.files?.[0];
                  if (!file) return;
                  const reader = new FileReader();
                  reader.onload = (ev) => setJson(ev.target?.result as string ?? "");
                  reader.readAsText(file);
                }}
              />
            </label>
          </div>

          <div className="grid grid-cols-2 gap-4 mb-5">
            <div>
              <label style={{ display: "block", marginBottom: 6, fontSize: 14, fontWeight: 600, color: "#111827" }}>
                Name <span style={{ color: "#9CA3AF", fontWeight: 400 }}>(optional)</span>
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Baseline run"
                className="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2"
                style={{ border: "1px solid #E5E7EB", background: "#F9FAFB", color: "#111827" }}
              />
            </div>
            <div>
              <label style={{ display: "block", marginBottom: 6, fontSize: 14, fontWeight: 600, color: "#111827" }}>
                Seed
              </label>
              <input
                type="number"
                value={seed}
                onChange={(e) => setSeed(e.target.value)}
                className="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2"
                style={{ border: "1px solid #E5E7EB", background: "#F9FAFB", color: "#111827" }}
              />
            </div>
          </div>

          <div className="flex items-center gap-2 mb-6">
            <input
              id="auto-validate"
              type="checkbox"
              checked={autoValidate}
              onChange={(e) => setAutoValidate(e.target.checked)}
              style={{ width: 16, height: 16, accentColor: "#2563EB", cursor: "pointer" }}
            />
            <label htmlFor="auto-validate" style={{ fontSize: 14, color: "#374151", cursor: "pointer" }}>
              Auto-validate after solve
            </label>
          </div>

          <button
            onClick={handleSubmit}
            disabled={submitting}
            className="flex items-center gap-2 px-6 py-2.5 rounded-lg text-sm font-medium transition-all hover:opacity-90 active:scale-95 disabled:opacity-70"
            style={{ background: "#2563EB", color: "#fff", border: "none", cursor: submitting ? "not-allowed" : "pointer" }}
          >
            {submitting && <Loader2 size={15} className="animate-spin" />}
            {submitting ? "Submitting…" : "Run Solver"}
          </button>

          {error && (
            <div className="flex items-start gap-2 mt-3">
              <AlertCircle size={15} style={{ color: "#DC2626", marginTop: 2, flexShrink: 0 }} />
              <p style={{ fontSize: 13, color: "#DC2626", margin: 0 }}>{error}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
