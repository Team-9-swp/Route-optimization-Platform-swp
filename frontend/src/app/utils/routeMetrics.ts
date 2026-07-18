export interface RoutePoint {
  x: number;
  y: number;
}

export interface RouteOrder extends RoutePoint {
  id: number;
  volume?: number;
  time_window?: unknown;
  vehicle_service_time?: number;
  loader_cnt?: number;
  loader_service_time?: number;
  optional?: boolean;
}

export interface VehicleRoute {
  id: number;
  route: number[];
  time?: number[];
}

export interface LoaderRoute {
  id: number;
  route: number[];
}

export interface RouteInputData {
  depot?: RoutePoint;
  orders?: RouteOrder[];
}

export interface ViewBox {
  x: number;
  y: number;
  w: number;
  h: number;
}

const VEHICLE_COLORS = ["#2563EB", "#16A34A", "#CA8A04", "#9333EA", "#DC2626", "#0891B2", "#DB2777", "#65A30D"];
const LOADER_COLORS = ["#7C3AED", "#EA580C", "#0D9488", "#4F46E5", "#BE123C", "#15803D"];

export function isFinitePoint(value: unknown): value is RoutePoint {
  if (!value || typeof value !== "object") return false;
  const point = value as RoutePoint;
  return Number.isFinite(point.x) && Number.isFinite(point.y);
}

export function getRouteOrderIds(route?: number[]): number[] {
  return Array.isArray(route) ? route.filter((id) => id !== 0 && Number.isFinite(id)) : [];
}

export function getRoutePoints(
  route: number[] | undefined,
  depot: RoutePoint | undefined,
  orderById: Map<number, RouteOrder>,
): RoutePoint[] {
  const orders = getRouteOrderIds(route)
    .map((id) => orderById.get(id))
    .filter((order): order is RouteOrder => isFinitePoint(order));
  if (!isFinitePoint(depot)) return orders;
  return [depot, ...orders, depot];
}

export function calculateCoordinateRouteLength(
  route: number[] | undefined,
  depot: RoutePoint | undefined,
  orderById: Map<number, RouteOrder>,
): number {
  if (!isFinitePoint(depot)) return 0;
  const points = getRoutePoints(route, depot, orderById);
  if (points.length < 2) return 0;
  let length = 0;
  for (let i = 1; i < points.length; i += 1) {
    length += Math.hypot(points[i].x - points[i - 1].x, points[i].y - points[i - 1].y);
  }
  return Number.isFinite(length) ? length : 0;
}

export function formatCoordinateLength(value: number): string {
  return `${Number.isFinite(value) ? value.toFixed(2) : "0.00"} units`;
}

export function formatExecutionTime(startedAt?: string, finishedAt?: string): string {
  if (!startedAt || !finishedAt) return "—";
  const duration = (Date.parse(finishedAt) - Date.parse(startedAt)) / 1000;
  if (!Number.isFinite(duration) || duration < 0) return "—";
  if (duration < 60) return `${duration.toFixed(1)} s`;
  return `${Math.floor(duration / 60)} min ${Math.round(duration % 60)} s`;
}

export function getLoadersForVehicleRoute(vehicleRoute: number[] | undefined, loaders: LoaderRoute[]): LoaderRoute[] {
  const orders = new Set(getRouteOrderIds(vehicleRoute));
  return loaders.filter((loader) => getRouteOrderIds(loader.route).some((id) => orders.has(id)));
}

export function getStableVehicleColor(_vehicleId: number, originalVehicleIndex: number): string {
  return VEHICLE_COLORS[Math.abs(originalVehicleIndex) % VEHICLE_COLORS.length];
}

export function getStableLoaderColor(_loaderId: number, originalLoaderIndex: number): string {
  return LOADER_COLORS[Math.abs(originalLoaderIndex) % LOADER_COLORS.length];
}

export function calculateViewBoxForPoints(
  points: RoutePoint[],
  fallback: ViewBox,
  padding = 44,
): ViewBox {
  const valid = points.filter(isFinitePoint);
  if (valid.length === 0) return fallback;
  const xs = valid.map((point) => point.x);
  const ys = valid.map((point) => point.y);
  const minX = Math.min(...xs);
  const maxX = Math.max(...xs);
  const minY = Math.min(...ys);
  const maxY = Math.max(...ys);
  const rawW = Math.max(maxX - minX, 1);
  const rawH = Math.max(maxY - minY, 1);
  const aspect = fallback.w / fallback.h;
  let w = rawW + padding * 2;
  let h = rawH + padding * 2;
  if (w / h > aspect) h = w / aspect;
  else w = h * aspect;
  return { x: (minX + maxX - w) / 2, y: (minY + maxY - h) / 2, w, h };
}
