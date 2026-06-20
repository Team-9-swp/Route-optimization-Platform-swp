import { useState } from "react";
import { CheckCircle2, XCircle, Loader2, AlertTriangle } from "lucide-react";
import { validateSolution } from "../../api/validate";
import type { ValidationResponse } from "../../types";

const INSTANCE_PLACEHOLDER = JSON.stringify(
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

const SOLUTION_PLACEHOLDER = JSON.stringify(
  {
    vehicles: [
      { id: 1, route: [0, 1, 2, 0], time: [0, 8, 18, 30] },
    ],
    loaders: [],
  },
  null,
  2,
);

export function Validate() {
  const [instanceJson, setInstanceJson] = useState("");
  const [solutionJson, setSolutionJson] = useState("");
  const [validating, setValidating] = useState(false);
  const [result, setResult] = useState<ValidationResponse | null>(null);
  const [parseError, setParseError] = useState("");

  async function handleValidate() {
    setParseError("");
    setResult(null);
    if (!instanceJson.trim() || !solutionJson.trim()) {
      setParseError("Both Instance JSON and Solution JSON are required.");
      return;
    }
    let instance: Record<string, unknown>;
    let solution: Record<string, unknown>;
    try {
      instance = JSON.parse(instanceJson);
    } catch {
      setParseError("Instance JSON is not valid JSON.");
      return;
    }
    try {
      solution = JSON.parse(solutionJson);
    } catch {
      setParseError("Solution JSON is not valid JSON.");
      return;
    }
    setValidating(true);
    try {
      const data = await validateSolution(instance, solution);
      setResult(data);
    } catch (err) {
      setParseError(err instanceof Error ? err.message : "Validation failed");
    } finally {
      setValidating(false);
    }
  }

  return (
    <div className="min-h-screen" style={{ background: "#F9FAFB" }}>
      <div className="max-w-5xl mx-auto px-6 py-8">
        <h1 style={{ color: "#111827", fontSize: 24, fontWeight: 600, marginBottom: 24 }}>
          Validate Solution
        </h1>

        <div
          className="rounded-xl p-8"
          style={{ background: "#fff", border: "1px solid #E5E7EB", boxShadow: "0 1px 4px rgba(0,0,0,0.05)" }}
        >
          <div className="grid grid-cols-2 gap-5 mb-6">
            {[
              { label: "Instance JSON", value: instanceJson, onChange: setInstanceJson, placeholder: INSTANCE_PLACEHOLDER },
              { label: "Solution JSON", value: solutionJson, onChange: setSolutionJson, placeholder: SOLUTION_PLACEHOLDER },
            ].map((field) => (
              <div key={field.label}>
                <label style={{ display: "block", marginBottom: 6, fontSize: 14, fontWeight: 600, color: "#111827" }}>
                  {field.label}
                </label>
                <textarea
                  rows={8}
                  value={field.value}
                  onChange={(e) => field.onChange(e.target.value)}
                  placeholder={field.placeholder}
                  className="w-full rounded-lg border resize-y focus:outline-none focus:ring-2"
                  style={{
                    border: "1px solid #E5E7EB",
                    padding: "10px 12px",
                    color: "#111827",
                    background: "#F9FAFB",
                    fontFamily: "'JetBrains Mono', monospace",
                    fontSize: 12,
                    lineHeight: 1.6,
                  }}
                />
              </div>
            ))}
          </div>

          <div className="flex justify-center mb-2">
            <button
              onClick={handleValidate}
              disabled={validating}
              className="flex items-center gap-2 px-8 py-2.5 rounded-lg text-sm font-medium transition-all hover:opacity-90 active:scale-95 disabled:opacity-70"
              style={{ background: "#2563EB", color: "#fff", border: "none", cursor: validating ? "not-allowed" : "pointer" }}
            >
              {validating && <Loader2 size={15} className="animate-spin" />}
              {validating ? "Validating…" : "Validate"}
            </button>
          </div>

          {parseError && (
            <div className="flex items-center gap-2 mt-3 justify-center">
              <AlertTriangle size={14} style={{ color: "#DC2626" }} />
              <p style={{ fontSize: 13, color: "#DC2626", margin: 0 }}>{parseError}</p>
            </div>
          )}
        </div>

        {result?.passed && (
          <div className="rounded-xl p-6 mt-5" style={{ background: "#F0FDF4", border: "1px solid #BBF7D0" }}>
            <div className="flex items-start gap-4">
              <CheckCircle2 size={28} style={{ color: "#15803D", flexShrink: 0 }} />
              <div>
                <p style={{ fontSize: 18, fontWeight: 600, color: "#15803D", margin: "0 0 4px 0" }}>Passed</p>
                <p style={{ fontSize: 14, color: "#166534", margin: "0 0 2px 0" }}>
                  Objective value: <strong>{result.objective_value ?? "—"}</strong>
                </p>
                <p style={{ fontSize: 13, color: "#166534", margin: 0 }}>No constraint violations detected.</p>
              </div>
            </div>
          </div>
        )}

        {result && !result.passed && (
          <div className="rounded-xl p-6 mt-5" style={{ background: "#FEF2F2", border: "1px solid #FECACA" }}>
            <div className="flex items-start gap-4">
              <XCircle size={28} style={{ color: "#DC2626", flexShrink: 0 }} />
              <div>
                <p style={{ fontSize: 18, fontWeight: 600, color: "#DC2626", margin: "0 0 8px 0" }}>Failed</p>
                {result.violations.length > 0 ? (
                  <>
                    <p style={{ fontSize: 13, fontWeight: 600, color: "#991B1B", margin: "0 0 6px 0" }}>Violations:</p>
                    <ul style={{ margin: 0, paddingLeft: 18 }}>
                      {result.violations.map((v, i) => (
                        <li key={i} style={{ fontSize: 13, color: "#991B1B", marginBottom: 4 }}>
                          {v}
                        </li>
                      ))}
                    </ul>
                  </>
                ) : (
                  <p style={{ fontSize: 13, color: "#991B1B", margin: 0 }}>Validation failed with no detailed violations.</p>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
