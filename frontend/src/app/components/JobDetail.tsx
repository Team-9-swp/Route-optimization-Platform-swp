import { useEffect, useState } from "react";
import { ArrowLeft, CheckCircle2, Download, RotateCcw, MapPin, XCircle, Loader2 } from "lucide-react";
import { getJob } from "../../api/jobs";
import type { Job } from "../../types";
import type { Page } from "../App";

interface VehicleRoute {
  id: number;
  route: number[];
  time: number[];
}

interface LoaderRoute {
  id: number;
  route: number[];
}

const TABS = ["Routes", "Validation", "Raw JSON"] as const;
type Tab = (typeof TABS)[number];

interface Props {
  id: string;
  navigate: (p: Page) => void;
}

function formatRoute(route: number[]): string {
  return ["Depot", ...route.filter((n) => n !== 0).map(String), "Depot"].join(" → ");
}

interface InputOrder {
  id: number;
  x: number;
  y: number;
}

interface InputData {
  depot?: { x: number; y: number };
  orders?: InputOrder[];
}

const VEHICLE_COLORS = ["#2563EB", "#16A34A", "#CA8A04", "#9333EA", "#DC2626", "#0891B2"];

function RouteMap({ inputData, vehicles }: { inputData?: Record<string, unknown>; vehicles: VehicleRoute[] }) {
  const data = inputData as InputData | undefined;
  const depot = data?.depot;
  const orders = data?.orders ?? [];

  if (!depot || vehicles.length === 0) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500 text-sm">
        No route data available for the map.
      </div>
    );
  }

  const orderById = new Map(orders.map((o) => [o.id, o]));
  const points: { x: number; y: number }[] = [depot, ...orders];
  const xs = points.map((p) => p.x);
  const ys = points.map((p) => p.y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);
  const padX = Math.max((maxX - minX) * 0.1, 5);
  const padY = Math.max((maxY - minY) * 0.1, 5);
  const vbMinX = minX - padX;
  const vbMaxX = maxX + padX;
  const vbMinY = minY - padY;
  const vbMaxY = maxY + padY;
  const width = vbMaxX - vbMinX;
  const height = vbMaxY - vbMinY;

  function toSvg(point: { x: number; y: number }) {
    return {
      cx: point.x - vbMinX,
      cy: vbMaxY - point.y,
    };
  }

  const depotPt = toSvg(depot);

  return (
    <svg className="absolute inset-0 w-full h-full" viewBox={`0 0 ${width} ${height}`} preserveAspectRatio="xMidYMid meet">
      {vehicles.map((vehicle, vi) => {
        const coords = [depot, ...vehicle.route.filter((id) => id !== 0).map((id) => orderById.get(id)).filter(Boolean) as InputOrder[], depot];
        const pts = coords.map(toSvg);
        const pointsAttr = pts.map((p) => `${p.cx},${p.cy}`).join(" ");
        const color = VEHICLE_COLORS[vi % VEHICLE_COLORS.length];
        return (
          <g key={vehicle.id}>
            <polyline points={pointsAttr} fill="none" stroke={color} strokeWidth={Math.max(width / 120, 1.5)} opacity={0.8} strokeDasharray="6,3" />
          </g>
        );
      })}
      {orders.map((order) => {
        const pt = toSvg(order);
        return (
          <g key={order.id}>
            <circle cx={pt.cx} cy={pt.cy} r={Math.max(width / 80, 3)} fill="#CA8A04" />
            <text x={pt.cx} y={pt.cy - Math.max(width / 80, 4)} fontSize={Math.max(width / 40, 10)} fill="#374151" textAnchor="middle">
              {order.id}
            </text>
          </g>
        );
      })}
      <g>
        <circle cx={depotPt.cx} cy={depotPt.cy} r={Math.max(width / 60, 5)} fill="#2563EB" />
        <circle cx={depotPt.cx} cy={depotPt.cy} r={Math.max(width / 35, 8)} fill="#2563EB" fillOpacity={0.15} />
        <text x={depotPt.cx} y={depotPt.cy - Math.max(width / 35, 9)} fontSize={Math.max(width / 40, 10)} fill="#2563EB" textAnchor="middle" fontWeight={600}>
          Depot
        </text>
      </g>
    </svg>
  );
}

export function JobDetail({ id, navigate }: Props) {
  const [job, setJob] = useState<Job | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>("Routes");

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const data = await getJob(id);
        if (!cancelled) {
          setJob(data);
          setIsLoading(false);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : "Job not found");
          setIsLoading(false);
        }
      }
    }
    load();
    const interval = setInterval(() => {
      if (job?.status === "completed" || job?.status === "failed") {
        clearInterval(interval);
        return;
      }
      load();
    }, 1000);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, [id, job?.status]);

  if (isLoading) return <p className="p-6 text-gray-600">Loading job…</p>;
  if (error || !job) return <p className="p-6 text-red-600">{error || "Job not found"}</p>;

  const vehicles = (job.result?.vehicles as VehicleRoute[] | undefined) ?? [];
  const loaders = (job.result?.loaders as LoaderRoute[] | undefined) ?? [];
  const validation = job.validation_report;
  const isCompleted = job.status === "completed";
  const isFailed = job.status === "failed";

  return (
    <div className="min-h-screen" style={{ background: "#F9FAFB" }}>
      <div className="max-w-6xl mx-auto px-6 py-8">
        <button
          onClick={() => navigate({ name: "dashboard" })}
          className="inline-flex items-center gap-1.5 mb-5 text-sm font-medium hover:underline"
          style={{ color: "#2563EB", background: "none", border: "none", cursor: "pointer", padding: 0 }}
        >
          <ArrowLeft size={15} />
          Dashboard
        </button>

        {/* Header card */}
        <div
          className="rounded-xl p-6 mb-5"
          style={{ background: "#fff", border: "1px solid #E5E7EB", boxShadow: "0 1px 4px rgba(0,0,0,0.05)" }}
        >
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-3 mb-1">
                <h1 style={{ color: "#111827", fontSize: 22, fontWeight: 600, margin: 0 }}>
                  {job.name || "Untitled job"}
                </h1>
                {isCompleted && (
                  <span
                    className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium"
                    style={{ background: "#DCFCE7", color: "#15803D" }}
                  >
                    <CheckCircle2 size={12} />
                    Completed
                  </span>
                )}
                {isFailed && (
                  <span
                    className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium"
                    style={{ background: "#FEE2E2", color: "#B91C1C" }}
                  >
                    <XCircle size={12} />
                    Failed
                  </span>
                )}
                {job.status === "running" && (
                  <span
                    className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium"
                    style={{ background: "#DBEAFE", color: "#1D4ED8" }}
                  >
                    <Loader2 size={12} className="animate-spin" />
                    Running
                  </span>
                )}
                {job.status === "pending" && (
                  <span
                    className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium"
                    style={{ background: "#FEF9C3", color: "#A16207" }}
                  >
                    Pending
                  </span>
                )}
              </div>
              <p
                style={{
                  color: "#9CA3AF",
                  fontFamily: "'JetBrains Mono', monospace",
                  fontSize: 12,
                  marginBottom: 16,
                }}
              >
                {job.job_id}
              </p>
              <div className="flex gap-8">
                {[
                  { label: "Seed", value: String(job.seed ?? "—") },
                  { label: "Objective", value: job.objective_value?.toString() ?? "—" },
                  { label: "Validation", value: job.validation_status ?? "—" },
                ].map((item) => (
                  <div key={item.label}>
                    <p style={{ fontSize: 12, color: "#6B7280", margin: "0 0 2px 0", fontWeight: 500 }}>{item.label}</p>
                    <p
                      style={{
                        fontSize: 16,
                        fontWeight: 600,
                        color: item.label === "Validation" && item.value === "passed" ? "#15803D" : "#111827",
                        margin: 0,
                      }}
                    >
                      {item.value}
                    </p>
                  </div>
                ))}
              </div>
            </div>
            <div className="flex gap-2">
              <button
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors hover:bg-gray-50"
                style={{ border: "1px solid #E5E7EB", color: "#374151", background: "#fff", cursor: "pointer" }}
                onClick={() => {
                  const blob = new Blob([JSON.stringify(job, null, 2)], { type: "application/json" });
                  const url = URL.createObjectURL(blob);
                  const a = document.createElement("a");
                  a.href = url;
                  a.download = `${job.job_id}.json`;
                  a.click();
                  URL.revokeObjectURL(url);
                }}
              >
                <Download size={14} />
                Download JSON
              </button>
              <button
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors hover:bg-blue-50"
                style={{ border: "1px solid #BFDBFE", color: "#2563EB", background: "#EFF6FF", cursor: "pointer" }}
                onClick={() => navigate({ name: "new-job" })}
              >
                <RotateCcw size={14} />
                Re-run
              </button>
            </div>
          </div>
        </div>

        {/* Route map */}
        <div
          className="rounded-xl mb-5 relative overflow-hidden flex items-center justify-center"
          style={{ background: "#F0F4FF", border: "1px solid #DBEAFE", height: 280, boxShadow: "0 1px 4px rgba(0,0,0,0.05)" }}
        >
          <svg className="absolute inset-0 w-full h-full" style={{ opacity: 0.15 }} xmlns="http://www.w3.org/2000/svg">
            <defs>
              <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#2563EB" strokeWidth="0.5" />
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" />
          </svg>
          <RouteMap inputData={job.input_data} vehicles={vehicles} />
          <div
            className="absolute top-3 right-3 flex items-center gap-1.5 px-2.5 py-1 rounded-md"
            style={{ background: "#fff", border: "1px solid #E5E7EB", fontSize: 12, color: "#6B7280" }}
          >
            <MapPin size={12} style={{ color: "#2563EB" }} />
            Route Map
          </div>
        </div>

        {/* Tabs */}
        <div
          className="rounded-xl overflow-hidden"
          style={{ background: "#fff", border: "1px solid #E5E7EB", boxShadow: "0 1px 4px rgba(0,0,0,0.05)" }}
        >
          <div className="flex" style={{ borderBottom: "1px solid #F3F4F6" }}>
            {TABS.map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                style={{
                  border: "none",
                  borderBottom: activeTab === tab ? "2px solid #2563EB" : "2px solid transparent",
                  background: "none",
                  color: activeTab === tab ? "#2563EB" : "#6B7280",
                  cursor: "pointer",
                  padding: "12px 20px",
                  fontSize: 14,
                  fontWeight: activeTab === tab ? 600 : 400,
                  marginBottom: -1,
                }}
              >
                {tab}
              </button>
            ))}
          </div>

          <div style={{ padding: 24 }}>
            {activeTab === "Routes" && (
              <div>
                <h3 style={{ color: "#111827", fontSize: 14, fontWeight: 600, margin: "0 0 12px 0" }}>Vehicle Routes</h3>
                {vehicles.length === 0 ? (
                  <p style={{ fontSize: 13, color: "#6B7280" }}>No vehicle routes available.</p>
                ) : (
                  <table style={{ width: "100%", borderCollapse: "collapse", marginBottom: 24 }}>
                    <thead>
                      <tr style={{ borderBottom: "1px solid #F3F4F6" }}>
                        {["Vehicle", "Route", "Start Time"].map((col) => (
                          <th
                            key={col}
                            style={{
                              padding: "8px 12px",
                              textAlign: "left",
                              fontSize: 11,
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
                      {vehicles.map((row) => (
                        <tr key={row.id} className="hover:bg-gray-50">
                          <td style={{ padding: "10px 12px", fontSize: 13, fontWeight: 500, color: "#111827" }}>
                            V-{row.id}
                          </td>
                          <td
                            style={{
                              padding: "10px 12px",
                              fontSize: 12,
                              color: "#374151",
                              fontFamily: "'JetBrains Mono', monospace",
                            }}
                          >
                            {formatRoute(row.route)}
                          </td>
                          <td style={{ padding: "10px 12px", fontSize: 13, color: "#6B7280" }}>
                            {row.time?.[0] ?? "—"}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}

                <h3 style={{ color: "#111827", fontSize: 14, fontWeight: 600, margin: "0 0 12px 0" }}>Loader Routes</h3>
                {loaders.length === 0 ? (
                  <p style={{ fontSize: 13, color: "#6B7280" }}>No loader routes available.</p>
                ) : (
                  <table style={{ width: "100%", borderCollapse: "collapse" }}>
                    <thead>
                      <tr style={{ borderBottom: "1px solid #F3F4F6" }}>
                        {["Loader", "Route"].map((col) => (
                          <th
                            key={col}
                            style={{
                              padding: "8px 12px",
                              textAlign: "left",
                              fontSize: 11,
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
                      {loaders.map((row) => (
                        <tr key={row.id} className="hover:bg-gray-50">
                          <td style={{ padding: "10px 12px", fontSize: 13, fontWeight: 500, color: "#111827" }}>
                            L-{row.id}
                          </td>
                          <td
                            style={{
                              padding: "10px 12px",
                              fontSize: 12,
                              color: "#374151",
                              fontFamily: "'JetBrains Mono', monospace",
                            }}
                          >
                            {formatRoute(row.route)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            )}

            {activeTab === "Validation" && (
              <div>
                {validation?.passed ? (
                  <div
                    className="flex items-center gap-3 p-4 rounded-lg mb-4"
                    style={{ background: "#F0FDF4", border: "1px solid #BBF7D0" }}
                  >
                    <CheckCircle2 size={20} style={{ color: "#15803D" }} />
                    <div>
                      <p style={{ fontSize: 15, fontWeight: 600, color: "#15803D", margin: 0 }}>Validation Passed</p>
                      <p style={{ fontSize: 13, color: "#166534", margin: "2px 0 0 0" }}>
                        Objective value: <strong>{(validation.objective_value as number | undefined) ?? "—"}</strong>
                      </p>
                    </div>
                  </div>
                ) : (
                  <div
                    className="flex items-center gap-3 p-4 rounded-lg mb-4"
                    style={{ background: "#FEF2F2", border: "1px solid #FECACA" }}
                  >
                    <XCircle size={20} style={{ color: "#DC2626" }} />
                    <div>
                      <p style={{ fontSize: 15, fontWeight: 600, color: "#DC2626", margin: 0 }}>Validation Failed</p>
                    </div>
                  </div>
                )}
                {validation && Array.isArray(validation.violations) && validation.violations.length > 0 ? (
                  <>
                    <p style={{ fontSize: 13, fontWeight: 600, color: "#111827", margin: "0 0 8px 0" }}>Violations:</p>
                    <ul style={{ margin: 0, paddingLeft: 18 }}>
                      {validation.violations.map((v: string, i: number) => (
                        <li key={i} style={{ fontSize: 13, color: "#991B1B", marginBottom: 4 }}>
                          {v}
                        </li>
                      ))}
                    </ul>
                  </>
                ) : (
                  <p style={{ fontSize: 13, color: "#6B7280" }}>
                    {validation ? "No constraint violations detected." : "No validation report available."}
                  </p>
                )}
              </div>
            )}

            {activeTab === "Raw JSON" && (
              <pre
                style={{
                  background: "#1E293B",
                  color: "#E2E8F0",
                  padding: 20,
                  borderRadius: 8,
                  fontSize: 12.5,
                  lineHeight: 1.6,
                  overflow: "auto",
                  maxHeight: 380,
                  fontFamily: "'JetBrains Mono', monospace",
                  margin: 0,
                }}
              >
                {JSON.stringify(job.result ?? job, null, 2)}
              </pre>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
