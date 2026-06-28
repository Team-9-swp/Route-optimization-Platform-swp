import { useCallback, useEffect, useRef, useState } from "react";
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
const LOADER_COLORS = ["#DB2777", "#7C3AED", "#EA580C", "#0D9488", "#65A30D", "#4F46E5"];

const VIEW_W = 800;
const VIEW_H = 560;
const PADDING = 40;

function useDisplayTransform(inputData?: Record<string, unknown>) {
  const data = inputData as InputData | undefined;
  const depot = data?.depot;
  const orders = data?.orders ?? [];

  if (!depot || orders.length === 0) {
    return null;
  }

  const points = [depot, ...orders];
  const xs = points.map((p) => p.x);
  const ys = points.map((p) => p.y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);

  const dataW = Math.max(maxX - minX, 1);
  const dataH = Math.max(maxY - minY, 1);
  const scale = Math.min((VIEW_W - PADDING * 2) / dataW, (VIEW_H - PADDING * 2) / dataH);
  const offsetX = PADDING + (VIEW_W - PADDING * 2 - dataW * scale) / 2;
  const offsetY = PADDING + (VIEW_H - PADDING * 2 - dataH * scale) / 2;

  function toSvg(point: { x: number; y: number }) {
    return {
      cx: offsetX + (point.x - minX) * scale,
      cy: offsetY + (maxY - point.y) * scale,
    };
  }

  return { depot, orders, orderById: new Map(orders.map((o) => [o.id, o])), toSvg, scale };
}

interface ViewBox {
  x: number;
  y: number;
  w: number;
  h: number;
}

const MIN_VIEW_W = 140;
const MAX_VIEW_W = VIEW_W * 6;

function RouteMap({
  inputData,
  vehicles,
  loaders,
  visibleVehicleIds,
  visibleLoaderIds,
}: {
  inputData?: Record<string, unknown>;
  vehicles: VehicleRoute[];
  loaders: LoaderRoute[];
  visibleVehicleIds: Set<number>;
  visibleLoaderIds: Set<number>;
}) {
  const transform = useDisplayTransform(inputData);
  const containerRef = useRef<HTMLDivElement>(null);
  const svgRef = useRef<SVGSVGElement>(null);
  const [viewBox, setViewBox] = useState<ViewBox>({ x: 0, y: 0, w: VIEW_W, h: VIEW_H });
  const isDragging = useRef(false);
  const dragStart = useRef({ x: 0, y: 0, vbX: 0, vbY: 0 });

  useEffect(() => {
    setViewBox({ x: 0, y: 0, w: VIEW_W, h: VIEW_H });
  }, [inputData]);

  const clampViewBox = useCallback((vb: ViewBox): ViewBox => {
    const aspect = VIEW_H / VIEW_W;
    const w = Math.min(Math.max(vb.w, MIN_VIEW_W), MAX_VIEW_W);
    const h = w * aspect;
    const x = Math.min(Math.max(vb.x, -w * 0.5), VIEW_W - w * 0.5);
    const y = Math.min(Math.max(vb.y, -h * 0.5), VIEW_H - h * 0.5);
    return { x, y, w, h };
  }, []);

  const zoom = useCallback(
    (factor: number, centerX?: number, centerY?: number) => {
      setViewBox((prev) => {
        const cx = centerX ?? prev.x + prev.w / 2;
        const cy = centerY ?? prev.y + prev.h / 2;
        const newW = prev.w * factor;
        const newH = newW * (VIEW_H / VIEW_W);
        return clampViewBox({
          x: cx - (newW * (cx - prev.x)) / prev.w,
          y: cy - (newH * (cy - prev.y)) / prev.h,
          w: newW,
          h: newH,
        });
      });
    },
    [clampViewBox]
  );

  const resetView = useCallback(() => {
    setViewBox({ x: 0, y: 0, w: VIEW_W, h: VIEW_H });
  }, []);

  const scrollLockedRef = useRef(false);
  const originalBodyOverflow = useRef("");
  const originalHtmlOverflow = useRef("");
  const originalPaddingRight = useRef("");

  const lockScroll = useCallback(() => {
    if (scrollLockedRef.current) return;
    scrollLockedRef.current = true;
    originalBodyOverflow.current = document.body.style.overflow;
    originalHtmlOverflow.current = document.documentElement.style.overflow;
    originalPaddingRight.current = document.body.style.paddingRight;
    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
    if (scrollbarWidth > 0) {
      document.body.style.paddingRight = `${scrollbarWidth}px`;
    }
    document.body.style.overflow = "hidden";
    document.documentElement.style.overflow = "hidden";
  }, []);

  const unlockScroll = useCallback(() => {
    if (!scrollLockedRef.current) return;
    scrollLockedRef.current = false;
    document.body.style.overflow = originalBodyOverflow.current;
    document.documentElement.style.overflow = originalHtmlOverflow.current;
    document.body.style.paddingRight = originalPaddingRight.current;
  }, []);

  useEffect(() => {
    return () => {
      if (scrollLockedRef.current) {
        document.body.style.overflow = originalBodyOverflow.current;
        document.documentElement.style.overflow = originalHtmlOverflow.current;
        document.body.style.paddingRight = originalPaddingRight.current;
      }
    };
  }, []);

  const handleWheel = useCallback(
    (e: React.WheelEvent) => {
      e.preventDefault();
      const svg = svgRef.current;
      if (!svg) return;
      const rect = svg.getBoundingClientRect();
      const pt = svg.createSVGPoint();
      pt.x = e.clientX - rect.left;
      pt.y = e.clientY - rect.top;
      const ctm = svg.getScreenCTM();
      if (!ctm) return;
      const svgP = pt.matrixTransform(ctm.inverse());
      const factor = e.deltaY > 0 ? 1.1 : 0.9;
      zoom(factor, svgP.x, svgP.y);
    },
    [zoom]
  );

  const handleMouseDown = useCallback(
    (e: React.MouseEvent) => {
      isDragging.current = true;
      dragStart.current = { x: e.clientX, y: e.clientY, vbX: viewBox.x, vbY: viewBox.y };
    },
    [viewBox]
  );

  const handleMouseMove = useCallback(
    (e: React.MouseEvent) => {
      if (!isDragging.current) return;
      const svg = svgRef.current;
      if (!svg) return;
      const rect = svg.getBoundingClientRect();
      const scaleX = viewBox.w / rect.width;
      const scaleY = viewBox.h / rect.height;
      setViewBox((prev) =>
        clampViewBox({
          ...prev,
          x: dragStart.current.vbX - (e.clientX - dragStart.current.x) * scaleX,
          y: dragStart.current.vbY - (e.clientY - dragStart.current.y) * scaleY,
        })
      );
    },
    [viewBox, clampViewBox]
  );

  const handleMouseUp = useCallback(() => {
    isDragging.current = false;
  }, []);

  const visibleVehicles = vehicles.filter((v) => visibleVehicleIds.has(v.id));
  const visibleLoaders = loaders.filter((l) => visibleLoaderIds.has(l.id));

  if (!transform || (visibleVehicles.length === 0 && visibleLoaders.length === 0)) {
    return (
      <div className="flex items-center justify-center h-full text-gray-500 text-sm">
        No route data available for the selected layer.
      </div>
    );
  }

  const { depot, orders, orderById, toSvg } = transform;
  const depotPt = toSvg(depot);

  const btnStyle = {
    background: "#fff",
    border: "1px solid #E5E7EB",
    borderRadius: 4,
    color: "#374151",
    cursor: "pointer",
    fontSize: 12,
    fontWeight: 600,
    padding: "4px 10px",
  };

  return (
    <div
      ref={containerRef}
      className="w-full h-full relative"
      style={{ touchAction: "none", overscrollBehavior: "contain" }}
      onMouseEnter={lockScroll}
      onMouseLeave={unlockScroll}
    >
      <svg
        ref={svgRef}
        className="w-full h-full cursor-grab active:cursor-grabbing"
        viewBox={`${viewBox.x} ${viewBox.y} ${viewBox.w} ${viewBox.h}`}
        preserveAspectRatio="xMidYMid meet"
        onWheel={handleWheel}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      >
        <defs>
          <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#2563EB" strokeWidth="0.5" />
          </pattern>
        </defs>
        <rect x={viewBox.x} y={viewBox.y} width={viewBox.w} height={viewBox.h} fill="url(#grid)" opacity={0.15} />

        {visibleVehicles.map((vehicle, vi) => {
          const coords = [depot, ...vehicle.route.filter((id) => id !== 0).map((id) => orderById.get(id)).filter(Boolean) as InputOrder[], depot];
          const pts = coords.map(toSvg);
          const pointsAttr = pts.map((p) => `${p.cx},${p.cy}`).join(" ");
          const color = VEHICLE_COLORS[vi % VEHICLE_COLORS.length];
          return (
            <g key={`v-${vehicle.id}`}>
              <polyline points={pointsAttr} fill="none" stroke={color} strokeWidth={2} opacity={0.85} strokeDasharray="5,3" />
            </g>
          );
        })}

        {visibleLoaders.map((loader, li) => {
          const loaderOrders = loader.route
            .filter((id) => id !== 0)
            .map((id) => orderById.get(id))
            .filter(Boolean) as InputOrder[];
          if (loaderOrders.length === 0) return null;
          const coords = [...loaderOrders, loaderOrders[0]];
          const pts = coords.map(toSvg);
          const pointsAttr = pts.map((p) => `${p.cx},${p.cy}`).join(" ");
          const color = LOADER_COLORS[li % LOADER_COLORS.length];
          return (
            <g key={`l-${loader.id}`}>
              <polyline points={pointsAttr} fill="none" stroke={color} strokeWidth={2} opacity={0.85} />
            </g>
          );
        })}

        {orders.map((order) => {
          const pt = toSvg(order);
          return (
            <g key={`o-${order.id}`}>
              <circle cx={pt.cx} cy={pt.cy} r={3.5} fill="#CA8A04" stroke="#fff" strokeWidth={1} />
              <text x={pt.cx} y={pt.cy - 6} fontSize={10} fill="#374151" textAnchor="middle" fontWeight={500}>
                {order.id}
              </text>
            </g>
          );
        })}

        <g>
          <circle cx={depotPt.cx} cy={depotPt.cy} r={6} fill="#2563EB" stroke="#fff" strokeWidth={1.5} />
          <circle cx={depotPt.cx} cy={depotPt.cy} r={10} fill="#2563EB" fillOpacity={0.15} />
          <text x={depotPt.cx} y={depotPt.cy - 13} fontSize={10} fill="#2563EB" textAnchor="middle" fontWeight={600}>
            Depot
          </text>
        </g>
      </svg>

      <div className="absolute top-3 right-3 flex items-center gap-1">
        <button style={btnStyle} onClick={() => zoom(1.1)} title="Zoom out">-</button>
        <button style={btnStyle} onClick={resetView} title="Reset view">Reset</button>
        <button style={btnStyle} onClick={() => zoom(0.9)} title="Zoom in">+</button>
      </div>

      <div className="pointer-events-none absolute bottom-3 left-3 text-[10px] text-gray-400">
        Scroll to zoom · Drag to pan
      </div>
    </div>
  );
}

function RouteFilter({
  vehicles,
  loaders,
  visibleVehicleIds,
  visibleLoaderIds,
  onToggleVehicle,
  onToggleLoader,
}: {
  vehicles: VehicleRoute[];
  loaders: LoaderRoute[];
  visibleVehicleIds: Set<number>;
  visibleLoaderIds: Set<number>;
  onToggleVehicle: (id: number | "all", checked: boolean) => void;
  onToggleLoader: (id: number | "all", checked: boolean) => void;
}) {
  const vehicleAll = vehicles.length > 0 && vehicles.every((v) => visibleVehicleIds.has(v.id));
  const vehicleSome = vehicles.some((v) => visibleVehicleIds.has(v.id)) && !vehicleAll;
  const loaderAll = loaders.length > 0 && loaders.every((l) => visibleLoaderIds.has(l.id));
  const loaderSome = loaders.some((l) => visibleLoaderIds.has(l.id)) && !loaderAll;

  const groupTitleStyle = { fontSize: 11, fontWeight: 600, color: "#111827", margin: "0 0 4px 0" };
  const labelStyle = { display: "flex", alignItems: "center", gap: 6, fontSize: 11, color: "#374151", cursor: "pointer", marginBottom: 2 };

  return (
    <div
      data-route-filter
      onWheel={(e) => e.stopPropagation()}
      style={{
        background: "rgba(255,255,255,0.95)",
        border: "1px solid #E5E7EB",
        borderRadius: 6,
        padding: "8px 10px",
        fontSize: 11,
        maxHeight: 180,
        overflow: "auto",
        maxWidth: 170,
      }}
    >
      <p style={{ fontWeight: 600, margin: "0 0 6px 0", color: "#111827" }}>Routes</p>

      {vehicles.length > 0 && (
        <div style={{ marginBottom: 8 }}>
          <p style={groupTitleStyle}>Vehicles</p>
          <label style={labelStyle}>
            <input
              type="checkbox"
              checked={vehicleAll}
              ref={(el) => {
                if (el) el.indeterminate = vehicleSome;
              }}
              onChange={(e) => onToggleVehicle("all", e.target.checked)}
            />
            All vehicles
          </label>
          {vehicles.map((v, i) => (
            <label key={v.id} style={{ ...labelStyle, paddingLeft: 12 }}>
              <input
                type="checkbox"
                checked={visibleVehicleIds.has(v.id)}
                onChange={(e) => onToggleVehicle(v.id, e.target.checked)}
              />
              <span
                style={{
                  width: 10,
                  height: 10,
                  borderRadius: "50%",
                  background: VEHICLE_COLORS[i % VEHICLE_COLORS.length],
                  flexShrink: 0,
                }}
              />
              V-{v.id}
            </label>
          ))}
        </div>
      )}

      {loaders.length > 0 && (
        <div>
          <p style={groupTitleStyle}>Loaders</p>
          <label style={labelStyle}>
            <input
              type="checkbox"
              checked={loaderAll}
              ref={(el) => {
                if (el) el.indeterminate = loaderSome;
              }}
              onChange={(e) => onToggleLoader("all", e.target.checked)}
            />
            All loaders
          </label>
          {loaders.map((l, i) => (
            <label key={l.id} style={{ ...labelStyle, paddingLeft: 12 }}>
              <input
                type="checkbox"
                checked={visibleLoaderIds.has(l.id)}
                onChange={(e) => onToggleLoader(l.id, e.target.checked)}
              />
              <span
                style={{
                  width: 10,
                  height: 10,
                  borderRadius: "50%",
                  background: LOADER_COLORS[i % LOADER_COLORS.length],
                  flexShrink: 0,
                }}
              />
              L-{l.id}
            </label>
          ))}
        </div>
      )}
    </div>
  );
}

function MapRouteList({
  vehicles,
  loaders,
  visibleVehicleIds,
  visibleLoaderIds,
}: {
  vehicles: VehicleRoute[];
  loaders: LoaderRoute[];
  visibleVehicleIds: Set<number>;
  visibleLoaderIds: Set<number>;
}) {
  const visibleVehicles = vehicles.filter((v) => visibleVehicleIds.has(v.id));
  const visibleLoaders = loaders.filter((l) => visibleLoaderIds.has(l.id));
  return (
    <div
      style={{
        background: "rgba(255,255,255,0.95)",
        border: "1px solid #E5E7EB",
        borderRadius: 6,
        padding: "8px 10px",
        maxHeight: 120,
        overflow: "auto",
        maxWidth: 180,
      }}
    >
      <p style={{ fontSize: 11, fontWeight: 600, color: "#111827", margin: "0 0 6px 0" }}>Routes</p>
      {visibleVehicles.map((v, i) => (
        <div key={`rlv-${v.id}`} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 11, color: "#374151", marginBottom: 3 }}>
          <div style={{ width: 10, height: 10, borderRadius: "50%", background: VEHICLE_COLORS[i % VEHICLE_COLORS.length] }} />
          <span>V-{v.id}: {v.route.filter((id) => id !== 0).length} orders</span>
        </div>
      ))}
      {visibleLoaders.map((l, i) => (
        <div key={`rll-${l.id}`} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 11, color: "#374151", marginBottom: 3 }}>
          <div style={{ width: 10, height: 10, borderRadius: "50%", background: LOADER_COLORS[i % LOADER_COLORS.length] }} />
          <span>L-{l.id}: {l.route.filter((id) => id !== 0).length} orders</span>
        </div>
      ))}
    </div>
  );
}

export function JobDetail({ id, navigate }: Props) {
  const [job, setJob] = useState<Job | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>("Routes");
  const [visibleVehicleIds, setVisibleVehicleIds] = useState<Set<number>>(new Set());
  const [visibleLoaderIds, setVisibleLoaderIds] = useState<Set<number>>(new Set());

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

  // Initialise route filters when a job is loaded.
  useEffect(() => {
    if (job) {
      const vehicles = (job.result?.vehicles as VehicleRoute[] | undefined) ?? [];
      const loaders = (job.result?.loaders as LoaderRoute[] | undefined) ?? [];
      setVisibleVehicleIds(new Set(vehicles.map((v) => v.id)));
      setVisibleLoaderIds(new Set(loaders.map((l) => l.id)));
    }
  }, [job?.job_id]);

  const handleToggleVehicle = useCallback((id: number | "all", checked: boolean) => {
    if (id === "all") {
      const vehicles = (job?.result?.vehicles as VehicleRoute[] | undefined) ?? [];
      setVisibleVehicleIds(checked ? new Set(vehicles.map((v) => v.id)) : new Set());
    } else {
      setVisibleVehicleIds((prev) => {
        const next = new Set(prev);
        if (checked) next.add(id);
        else next.delete(id);
        return next;
      });
    }
  }, [job]);

  const handleToggleLoader = useCallback((id: number | "all", checked: boolean) => {
    if (id === "all") {
      const loaders = (job?.result?.loaders as LoaderRoute[] | undefined) ?? [];
      setVisibleLoaderIds(checked ? new Set(loaders.map((l) => l.id)) : new Set());
    } else {
      setVisibleLoaderIds((prev) => {
        const next = new Set(prev);
        if (checked) next.add(id);
        else next.delete(id);
        return next;
      });
    }
  }, [job]);

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

        {/* Skipped optional orders */}
        {job.unserved_optional && job.unserved_optional.length > 0 && (
          <div
            className="mt-4 rounded-lg p-4 mb-5"
            style={{ background: "#FFFBEB", border: "1px solid #FDE68A" }}
          >
            <h3 style={{ color: "#92400E", fontSize: 14, fontWeight: 600, margin: "0 0 6px 0" }}>
              Skipped optional orders
            </h3>
            <p style={{ color: "#B45309", fontSize: 13, margin: 0 }}>
              {job.unserved_optional.join(", ")}
            </p>
          </div>
        )}
        {job.unserved_optional && job.unserved_optional.length === 0 && (
          <div className="mt-4 text-sm text-gray-600 mb-5">No optional orders were skipped.</div>
        )}

        {/* Route map */}
        <div
          className="rounded-xl mb-5 relative overflow-hidden"
          style={{ background: "#F0F4FF", border: "1px solid #DBEAFE", height: 420, boxShadow: "0 1px 4px rgba(0,0,0,0.05)" }}
        >
          <RouteMap
            inputData={job.input_data}
            vehicles={vehicles}
            loaders={loaders}
            visibleVehicleIds={visibleVehicleIds}
            visibleLoaderIds={visibleLoaderIds}
          />

          <div className="absolute top-3 left-3">
            <RouteFilter
              vehicles={vehicles}
              loaders={loaders}
              visibleVehicleIds={visibleVehicleIds}
              visibleLoaderIds={visibleLoaderIds}
              onToggleVehicle={handleToggleVehicle}
              onToggleLoader={handleToggleLoader}
            />
          </div>

          <div
            className="absolute top-3 right-3 flex items-center gap-2 px-2.5 py-1 rounded-md"
            style={{ background: "#fff", border: "1px solid #E5E7EB", fontSize: 12, color: "#6B7280" }}
          >
            <MapPin size={12} style={{ color: "#2563EB" }} />
            Route Map
          </div>

          <div className="absolute bottom-3 right-3">
            <MapRouteList
              vehicles={vehicles}
              loaders={loaders}
              visibleVehicleIds={visibleVehicleIds}
              visibleLoaderIds={visibleLoaderIds}
            />
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
