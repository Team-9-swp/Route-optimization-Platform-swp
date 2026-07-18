import { useMemo, useState } from "react";
import { Minus, Plus, RotateCcw, X } from "lucide-react";
import type { LoaderRoute } from "../utils/routeMetrics";

export interface GanttVehicleRoute {
  id: number;
  route: number[];
  time: number[];
}

interface InputPoint { x: number; y: number }
interface InputOrder extends InputPoint { id: number; vehicle_service_time?: number; loader_service_time?: number }
interface InputData { depot?: InputPoint; orders?: InputOrder[]; vehicle_speed?: number; loader_speed?: number }
interface Props { vehicles: GanttVehicleRoute[]; loaders: LoaderRoute[]; inputData?: Record<string, unknown> }
interface Visit { orderId: number; start: number; end: number }
interface Timeline { key: string; kind: "vehicle" | "loader"; id: number; start: number; end: number; visits: Visit[]; color: string }
interface HoverInfo { lane: string; orderId?: number; start: number; end?: number }

const VEHICLE_COLORS = ["#2563EB", "#16A34A", "#CA8A04", "#9333EA", "#DC2626", "#0891B2", "#DB2777", "#65A30D"];
const LOADER_COLORS = ["#7C3AED", "#EA580C", "#0D9488", "#4F46E5", "#BE123C", "#15803D"];
const finite = (value: unknown): value is number => typeof value === "number" && Number.isFinite(value);
const round2 = (value: number) => Math.round((value + Number.EPSILON) * 100) / 100;
const distance = (a?: InputPoint, b?: InputPoint) => a && b && finite(a.x) && finite(a.y) && finite(b.x) && finite(b.y) ? Math.hypot(a.x - b.x, a.y - b.y) : 0;
const formatTime = (value: number) => finite(value) ? value.toFixed(value % 1 === 0 ? 0 : 1) : "—";

function buildTimelines(vehicles: GanttVehicleRoute[], loaders: LoaderRoute[], input?: InputData): Timeline[] {
  const orderById = new Map((input?.orders ?? []).filter((order) => finite(order.id)).map((order) => [order.id, order]));
  const arrivalByOrder = new Map<number, number>();
  const timelines: Timeline[] = [];
  const vehicleSpeed = finite(input?.vehicle_speed) && input.vehicle_speed > 0 ? input.vehicle_speed : 0;

  vehicles.forEach((vehicle, index) => {
    const orderIds = (vehicle.route ?? []).filter((id) => id !== 0);
    const arrivals = (vehicle.time ?? []).filter(finite);
    const visits: Visit[] = [];
    orderIds.forEach((orderId, visitIndex) => {
      const arrival = arrivals[visitIndex];
      if (!finite(arrival)) return;
      if (!arrivalByOrder.has(orderId)) arrivalByOrder.set(orderId, arrival);
      const service = orderById.get(orderId)?.vehicle_service_time;
      visits.push({ orderId, start: arrival, end: round2(arrival + (finite(service) && service > 0 ? service : 0)) });
    });
    if (!visits.length) return;
    const firstOrder = orderById.get(visits[0].orderId);
    const lastOrder = orderById.get(visits[visits.length - 1].orderId);
    const departure = round2(visits[0].start - (vehicleSpeed ? distance(input?.depot, firstOrder) / vehicleSpeed : 0));
    const returnTime = vehicleSpeed ? distance(lastOrder, input?.depot) / vehicleSpeed : 0;
    const end = round2(visits[visits.length - 1].end + returnTime);
    timelines.push({ key: `vehicle-${vehicle.id}`, kind: "vehicle", id: vehicle.id, start: departure, end: Math.max(departure, end), visits, color: VEHICLE_COLORS[index % VEHICLE_COLORS.length] });
  });

  const loaderSpeed = finite(input?.loader_speed) && input.loader_speed > 0 ? input.loader_speed : 0;
  loaders.forEach((loader, index) => {
    const visits = (loader.route ?? []).map((orderId) => {
      const arrival = arrivalByOrder.get(orderId);
      const service = orderById.get(orderId)?.loader_service_time;
      if (!finite(arrival)) return null;
      return { orderId, start: arrival, end: round2(arrival + (finite(service) && service > 0 ? service : 0)) };
    }).filter((visit): visit is Visit => visit !== null);
    if (!visits.length) return;
    const firstOrder = orderById.get(visits[0].orderId);
    const lastOrder = orderById.get(visits[visits.length - 1].orderId);
    const returnTime = loaderSpeed ? distance(lastOrder, firstOrder) / loaderSpeed : 0;
    timelines.push({ key: `loader-${loader.id}`, kind: "loader", id: loader.id, start: visits[0].start, end: round2(visits[visits.length - 1].end + returnTime), visits, color: LOADER_COLORS[index % LOADER_COLORS.length] });
  });
  return timelines.filter((timeline) => finite(timeline.start) && finite(timeline.end));
}

export function GanttSchedule({ vehicles, loaders, inputData }: Props) {
  const data = inputData as InputData | undefined;
  const timelines = useMemo(() => buildTimelines(vehicles, loaders, data), [vehicles, loaders, data]);
  const [showVehicles, setShowVehicles] = useState(true);
  const [showLoaders, setShowLoaders] = useState(true);
  const [zoom, setZoom] = useState(1);
  const [selectedKey, setSelectedKey] = useState<string | null>(null);
  const [hover, setHover] = useState<HoverInfo | null>(null);
  const visible = timelines.filter((timeline) => timeline.kind === "vehicle" ? showVehicles : showLoaders);
  const selected = timelines.find((timeline) => timeline.key === selectedKey) ?? null;

  if (!timelines.length) return <div className="flex h-40 items-center justify-center text-sm text-gray-500">No schedule data available.</div>;

  const globalStart = Math.min(...visible.map((timeline) => timeline.start));
  const globalEnd = Math.max(...visible.map((timeline) => timeline.end));
  const span = visible.length ? Math.max(globalEnd - globalStart, 1) : 1;
  const labelWidth = 76;
  const rowHeight = 38;
  const plotStart = labelWidth + 10;
  const width = 820 * zoom;
  const plotWidth = width - plotStart - 52;
  const chartHeight = Math.max(visible.length * rowHeight + 56, 120);
  const xOf = (time: number) => plotStart + ((time - globalStart) / span) * plotWidth;
  const tickCount = Math.max(5, Math.round(5 * zoom));
  const ticks = Array.from({ length: tickCount + 1 }, (_, index) => globalStart + span * index / tickCount);

  return <div>
    <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
      <div className="flex flex-wrap gap-2 text-xs">
        <label className="flex items-center gap-1.5 rounded border border-gray-200 px-2.5 py-1.5"><input type="checkbox" checked={showVehicles} onChange={(event) => setShowVehicles(event.target.checked)} />Vehicles</label>
        <label className="flex items-center gap-1.5 rounded border border-gray-200 px-2.5 py-1.5"><input type="checkbox" checked={showLoaders} onChange={(event) => setShowLoaders(event.target.checked)} />Loaders</label>
      </div>
      <div className="flex items-center gap-1">
        <button className="rounded border border-gray-200 p-1.5 text-gray-600 disabled:opacity-40" title="Zoom out" aria-label="Zoom schedule out" disabled={zoom <= 1} onClick={() => setZoom((value) => Math.max(1, value - 0.5))}><Minus size={14} /></button>
        <span className="min-w-12 text-center text-xs text-gray-500">{Math.round(zoom * 100)}%</span>
        <button className="rounded border border-gray-200 p-1.5 text-gray-600 disabled:opacity-40" title="Zoom in" aria-label="Zoom schedule in" disabled={zoom >= 4} onClick={() => setZoom((value) => Math.min(4, value + 0.5))}><Plus size={14} /></button>
        <button className="rounded border border-gray-200 p-1.5 text-gray-600" title="Reset schedule view" aria-label="Reset schedule view" onClick={() => { setZoom(1); setSelectedKey(null); }}><RotateCcw size={14} /></button>
      </div>
    </div>

    {visible.length === 0 ? <div className="flex h-32 items-center justify-center rounded border border-gray-100 text-sm text-gray-500">Enable at least one schedule layer.</div> : <div className="relative overflow-x-auto rounded-lg border border-gray-200 bg-white">
      <svg viewBox={`0 0 ${width} ${chartHeight}`} style={{ width, minWidth: "100%", height: chartHeight, display: "block" }} role="img" aria-label="Interactive vehicle and loader schedule">
        {ticks.map((time, index) => { const x = xOf(time); return <g key={`tick-${index}`}><line x1={x} x2={x} y1={8} y2={chartHeight - 30} stroke="#E5E7EB" /><text x={x} y={chartHeight - 12} fontSize={10} fill="#6B7280" textAnchor="middle">{formatTime(time)}</text></g>; })}
        <text x={plotStart + plotWidth / 2} y={chartHeight - 1} fontSize={10} fill="#9CA3AF" textAnchor="middle">Time</text>
        {visible.map((timeline, index) => {
          const y = 12 + index * rowHeight;
          const selectedLane = selectedKey === timeline.key;
          const muted = selectedKey !== null && !selectedLane;
          const barX = xOf(timeline.start);
          const barWidth = Math.max(xOf(timeline.end) - barX, 2);
          const label = `${timeline.kind === "vehicle" ? "V" : "L"}-${timeline.id}`;
          return <g key={timeline.key} opacity={muted ? 0.25 : 1} role="button" tabIndex={0} aria-label={`${label} schedule${selectedLane ? ", selected" : ""}`} onClick={() => setSelectedKey((current) => current === timeline.key ? null : timeline.key)} onKeyDown={(event) => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); setSelectedKey((current) => current === timeline.key ? null : timeline.key); } }} onMouseEnter={() => setHover({ lane: label, start: timeline.start, end: timeline.end })} onMouseLeave={() => setHover(null)} onFocus={() => setHover({ lane: label, start: timeline.start, end: timeline.end })} onBlur={() => setHover(null)}>
            {selectedLane && <rect x={2} y={y - 5} width={width - 4} height={rowHeight - 2} rx={5} fill="#EFF6FF" stroke="#93C5FD" />}
            <text x={labelWidth} y={y + 15} fontSize={11} fontWeight={700} fill={timeline.color} textAnchor="end">{label}</text>
            <rect x={barX} y={y + 3} width={barWidth} height={18} rx={4} fill={timeline.color} fillOpacity={timeline.kind === "vehicle" ? 0.16 : 0.09} stroke={timeline.color} strokeWidth={selectedLane ? 2 : 1} strokeDasharray={timeline.kind === "loader" ? "4 3" : undefined} />
            {timeline.visits.map((visit, visitIndex) => {
              const startX = xOf(visit.start);
              const endX = xOf(visit.end);
              const serviceWidth = Math.max(endX - startX, timeline.kind === "loader" ? 4 : 2);
              return <g key={`${timeline.key}-${visitIndex}-${visit.orderId}`} tabIndex={0} role="img" aria-label={`${label}, order ${visit.orderId}, time ${formatTime(visit.start)}`} onMouseEnter={(event) => { event.stopPropagation(); setHover({ lane: label, orderId: visit.orderId, start: visit.start, end: visit.end }); }} onMouseLeave={() => setHover({ lane: label, start: timeline.start, end: timeline.end })} onFocus={() => setHover({ lane: label, orderId: visit.orderId, start: visit.start, end: visit.end })} onBlur={() => setHover(null)}>
                {timeline.kind === "loader" ? <rect x={startX} y={y + 3} width={serviceWidth} height={18} rx={2} fill={timeline.color} opacity={0.9} /> : <><line x1={startX} x2={startX} y1={y + 3} y2={y + 21} stroke={timeline.color} strokeWidth={2} /><circle cx={startX} cy={y + 2} r={selectedLane ? 7 : 3} fill={timeline.color} stroke={selectedLane ? "white" : "none"} strokeWidth={1.5} />{selectedLane && <text x={startX} y={y + 2} fill="white" fontSize={8} fontWeight={700} textAnchor="middle" dominantBaseline="central" pointerEvents="none">{visitIndex + 1}</text>}</>}
                <title>{`${label} · order ${visit.orderId} · ${formatTime(visit.start)}${visit.end > visit.start ? `–${formatTime(visit.end)}` : ""}`}</title>
              </g>;
            })}
            <text x={Math.min(barX + barWidth + 5, width - 32)} y={y + 16} fontSize={9} fill="#9CA3AF">{formatTime(round2(timeline.end - timeline.start))}</text>
          </g>;
        })}
      </svg>
      {hover && <div className="pointer-events-none sticky bottom-2 left-2 z-10 inline-block rounded border border-gray-200 bg-white px-2.5 py-1.5 text-xs text-gray-700 shadow"><strong>{hover.lane}</strong>{hover.orderId !== undefined && <span> · Order {hover.orderId}</span>}<span className="block">{hover.orderId === undefined ? "Schedule" : "Service"}: {formatTime(hover.start)}{hover.end !== undefined ? `–${formatTime(hover.end)}` : ""}</span></div>}
    </div>}

    <div className="mt-2 flex flex-wrap items-center gap-4 text-[11px] text-gray-500"><span><span className="mr-1 inline-block h-2 w-4 rounded bg-blue-600/20 ring-1 ring-blue-600" />Vehicle bar = depot-to-depot schedule</span><span><span className="mr-1 inline-block h-3 w-px bg-blue-600" /><span className="mr-1 inline-block h-1.5 w-1.5 rounded-full bg-blue-600" />Vertical mark = arrival at an order</span><span><span className="mr-1 inline-block h-2 w-4 rounded bg-purple-600 ring-1 ring-purple-600" />Loader block = service window</span><span>Click a lane to number its stops; hover or focus a mark for its order and time.</span></div>
    {selected && <div className="mt-3 rounded-lg border border-blue-100 bg-blue-50 p-3 text-xs text-gray-700"><div className="flex items-center justify-between"><strong>{selected.kind === "vehicle" ? "Vehicle" : "Loader"} {selected.kind === "vehicle" ? "V" : "L"}-{selected.id}</strong><button className="inline-flex items-center gap-1 rounded border border-blue-200 bg-white px-2 py-1 text-[11px] text-blue-700" onClick={() => setSelectedKey(null)}><X size={11} />Clear selection</button></div><p className="mb-0 mt-1">Schedule: {formatTime(selected.start)}–{formatTime(selected.end)} · {selected.visits.length} orders</p><p className="mb-0 mt-1 break-words">Stops: {selected.visits.map((visit, index) => `${index + 1} = order ${visit.orderId}`).join(" · ")}</p></div>}
    {timelines.some((timeline) => timeline.kind === "loader") && <p className="mb-0 mt-2 text-[11px] text-gray-400">Loader service windows are derived from saved vehicle arrival times and each order&apos;s loader service time; no additional backend timing fields are introduced.</p>}
  </div>;
}
