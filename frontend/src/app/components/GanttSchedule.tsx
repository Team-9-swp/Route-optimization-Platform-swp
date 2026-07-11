import { useMemo } from "react";

export interface GanttVehicleRoute {
  id: number;
  route: number[];
  time: number[];
}

interface InputPoint {
  x: number;
  y: number;
}

interface InputOrder extends InputPoint {
  id: number;
  vehicle_service_time?: number;
}

interface InputData {
  depot?: InputPoint;
  orders?: InputOrder[];
  vehicle_speed?: number;
}

interface Props {
  vehicles: GanttVehicleRoute[];
  inputData?: Record<string, unknown>;
}

interface Visit {
  t: number;
  id: number;
}

interface VehicleTimeline {
  id: number;
  start: number;
  end: number;
  visits: Visit[];
}

const VEHICLE_COLORS = [
  "#2563EB",
  "#16A34A",
  "#CA8A04",
  "#9333EA",
  "#DC2626",
  "#0891B2",
  "#DB2777",
  "#65A30D",
];

function round2(n: number): number {
  return Math.round((n + Number.EPSILON) * 100) / 100;
}

function buildTimelines(
  vehicles: GanttVehicleRoute[],
  inputData?: InputData,
): VehicleTimeline[] {
  const speed = inputData?.vehicle_speed ?? 0;
  const depot = inputData?.depot;
  const orderMap = new Map<number, InputOrder>();
  for (const o of inputData?.orders ?? []) {
    orderMap.set(o.id, o);
  }

  const dist = (a: InputPoint | undefined, b: InputPoint | undefined): number => {
    if (!a || !b) return 0;
    return Math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2);
  };

  const result: VehicleTimeline[] = [];

  for (const v of vehicles) {
    const route = v.route ?? [];
    const times = v.time ?? [];
    const orderNodes = route.filter((n) => n !== 0);
    if (orderNodes.length === 0 || times.length === 0) continue;

    const visits: Visit[] = [];
    // Depot departure (mirrors the validator's reconstruction).
    const firstId = route[1] ?? orderNodes[0];
    const firstOrder = orderMap.get(firstId);
    const departLeg = speed > 0 ? round2(dist(depot, firstOrder) / speed) : 0;
    const departure = round2(times[0] - departLeg);
    visits.push({ t: departure, id: 0 });

    // Order visits: time[i] is the arrival at route[i + 1].
    for (let i = 0; i < times.length; i++) {
      const nodeId = route[i + 1];
      if (nodeId === undefined || nodeId === 0) continue;
      visits.push({ t: round2(times[i]), id: nodeId });
    }

    // Depot return.
    const lastId = route[route.length - 2] ?? orderNodes[orderNodes.length - 1];
    const lastOrder = orderMap.get(lastId);
    const returnLeg = speed > 0 ? round2(dist(lastOrder, depot) / speed) : 0;
    const service = lastOrder?.vehicle_service_time ?? 0;
    const ret = round2(times[times.length - 1] + returnLeg + service);
    visits.push({ t: ret, id: 0 });

    result.push({
      id: v.id,
      start: visits[0].t,
      end: visits[visits.length - 1].t,
      visits,
    });
  }

  return result;
}

function formatTime(t: number): string {
  if (!Number.isFinite(t)) return "—";
  return t.toFixed(t % 1 === 0 ? 0 : 1);
}

export function GanttSchedule({ vehicles, inputData }: Props) {
  const data = inputData as InputData | undefined;

  const timelines = useMemo(() => buildTimelines(vehicles, data), [vehicles, data]);

  if (timelines.length === 0) {
    return (
      <div className="flex items-center justify-center" style={{ height: 160, color: "#6B7280", fontSize: 13 }}>
        No schedule data available.
      </div>
    );
  }

  const globalStart = Math.min(...timelines.map((tl) => tl.start));
  const globalEnd = Math.max(...timelines.map((tl) => tl.end));
  const span = Math.max(globalEnd - globalStart, 1);

  // Layout constants.
  const labelW = 64;
  const padTop = 12;
  const rowH = 30;
  const barH = 16;
  const axisH = 34;
  const padRight = 16;
  const padLeft = 8;
  const contentW = 760;
  const plotW = contentW - labelW - padRight - padLeft;
  const plotX = labelW + padLeft;

  const ticks = 5;
  const tickValues = Array.from({ length: ticks + 1 }, (_, i) => globalStart + (span * i) / ticks);

  const innerH = padTop + timelines.length * rowH;
  const height = innerH + axisH;
  const width = contentW;

  const xOf = (t: number) => plotX + ((t - globalStart) / span) * plotW;

  return (
    <div style={{ width: "100%", overflowX: "auto" }}>
      <svg
        viewBox={`0 0 ${width} ${height}`}
        preserveAspectRatio="xMidYMid meet"
        style={{ width: "100%", minWidth: 560, display: "block" }}
        role="img"
        aria-label="Vehicle schedule Gantt chart"
      >
        {/* Vertical gridlines + time axis labels */}
        {tickValues.map((tv, i) => {
          const x = xOf(tv);
          return (
            <g key={`grid-${i}`}>
              <line
                x1={x}
                x2={x}
                y1={padTop - 4}
                y2={innerH}
                stroke="#E5E7EB"
                strokeWidth={1}
              />
              <text
                x={x}
                y={height - axisH + 18}
                fontSize={10}
                fill="#6B7280"
                textAnchor="middle"
              >
                {formatTime(tv)}
              </text>
            </g>
          );
        })}

        {/* Axis title */}
        <text
          x={plotX + plotW / 2}
          y={height - 4}
          fontSize={10}
          fill="#9CA3AF"
          textAnchor="middle"
        >
          Time
        </text>

        {timelines.map((tl, idx) => {
          const color = VEHICLE_COLORS[idx % VEHICLE_COLORS.length];
          const y = padTop + idx * rowH + (rowH - barH) / 2;
          const barX = xOf(tl.start);
          const barW = Math.max(xOf(tl.end) - barX, 2);
          return (
            <g key={`veh-${tl.id}`}>
              <text x={labelW} y={y + barH / 2 + 3} fontSize={11} fontWeight={600} fill="#374151" textAnchor="end">
                V-{tl.id}
              </text>
              {/* Full shift bar */}
              <rect x={barX} y={y} width={barW} height={barH} rx={3} fill={color} opacity={0.18} stroke={color} strokeWidth={1} />
              {/* Order visit markers */}
              {tl.visits.map((vis, vi) => {
                if (vis.id === 0) return null;
                const vx = xOf(vis.t);
                return (
                  <g key={`v-${tl.id}-${vi}`}>
                    <line x1={vx} x2={vx} y1={y} y2={y + barH} stroke={color} strokeWidth={1.5} />
                    <circle cx={vx} cy={y - 1} r={2.5} fill={color} />
                    <title>{`V-${tl.id} · order ${vis.id} @ t=${formatTime(vis.t)}`}</title>
                  </g>
                );
              })}
              {/* Shift duration label at the end */}
              <text x={barX + barW + 4} y={y + barH / 2 + 3} fontSize={10} fill="#9CA3AF">
                {formatTime(round2(tl.end - tl.start))}
              </text>
            </g>
          );
        })}
      </svg>

      <div style={{ display: "flex", gap: 16, flexWrap: "wrap", marginTop: 8, fontSize: 11, color: "#6B7280" }}>
        <span>
          <strong style={{ color: "#374151" }}>{timelines.length}</strong> vehicles · schedule window{" "}
          <strong style={{ color: "#374151" }}>{formatTime(globalStart)}–{formatTime(globalEnd)}</strong>
        </span>
        <span>Bars show each vehicle's depot-to-depot shift; ticks mark order arrival times (hover for details).</span>
      </div>

      <p style={{ fontSize: 11, color: "#9CA3AF", marginTop: 6, marginBottom: 0 }}>
        Note: loader timing is derived from the vehicle schedule and is not shown as a separate lane.
      </p>
    </div>
  );
}
