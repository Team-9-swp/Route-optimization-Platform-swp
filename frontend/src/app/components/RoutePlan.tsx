import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Maximize2, Route as RouteIcon, X } from "lucide-react";
import {
  calculateCoordinateRouteLength,
  calculateViewBoxForPoints,
  formatCoordinateLength,
  getLoadersForVehicleRoute,
  getRouteOrderIds,
  getRoutePoints,
  getStableLoaderColor,
  getStableVehicleColor,
  isFinitePoint,
  type LoaderRoute,
  type RouteInputData,
  type RouteOrder,
  type RoutePoint,
  type VehicleRoute,
  type ViewBox,
} from "../utils/routeMetrics";

interface Props {
  inputData?: Record<string, unknown>;
  vehicles: VehicleRoute[];
  loaders: LoaderRoute[];
  unservedOptional?: number[];
}

type SortMode = "id" | "length" | "orders";
interface DisplayPoint extends RoutePoint { source: RoutePoint }

const DEFAULT_VIEW: ViewBox = { x: -50, y: -50, w: 100, h: 70 };
const displayPoint = (point: RoutePoint): DisplayPoint => ({ x: point.x, y: -point.y, source: point });

function optionalValue(value: unknown): string | null {
  if (value === undefined || value === null || value === "") return null;
  if (typeof value === "number" && !Number.isFinite(value)) return null;
  if (Array.isArray(value)) return value.length ? value.join(" – ") : null;
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function OrderTooltip({ order, stop, total, unserved }: { order: RouteOrder; stop?: number; total?: number; unserved?: boolean }) {
  const fields: Array<[string, unknown]> = [
    ["Volume", order.volume],
    ["Time window", order.time_window],
    ["Vehicle service time", order.vehicle_service_time],
    ["Required loaders", order.loader_cnt],
    ["Loader service time", order.loader_service_time],
    ["Optional", order.optional],
  ];
  return (
    <div className="pointer-events-none absolute z-30 min-w-44 max-w-64 rounded-md border border-gray-200 bg-white p-2 text-xs text-gray-700 shadow-lg" style={{ left: 12, bottom: 12 }} role="tooltip">
      {stop !== undefined && total !== undefined && <p className="m-0 font-semibold text-blue-700">Stop: {stop} of {total}</p>}
      {unserved && <p className="m-0 font-semibold text-gray-700">Unserved optional order</p>}
      <p className="m-0"><strong>Order ID:</strong> {order.id}</p>
      <p className="m-0"><strong>Coordinates:</strong> ({order.x}, {order.y})</p>
      {fields.map(([label, value]) => {
        const text = optionalValue(value);
        return text === null ? null : <p className="m-0" key={label}><strong>{label}:</strong> {text}</p>;
      })}
    </div>
  );
}

export function RoutePlan({ inputData, vehicles, loaders, unservedOptional = [] }: Props) {
  const data = inputData as RouteInputData | undefined;
  const depot = isFinitePoint(data?.depot) ? data?.depot : undefined;
  const orders = useMemo(
    () => (Array.isArray(data?.orders) ? data.orders.filter((order) => Number.isFinite(order?.id) && isFinitePoint(order)) : []),
    [data?.orders],
  );
  const orderById = useMemo(() => new Map(orders.map((order) => [order.id, order])), [orders]);
  const vehicleColors = useMemo(() => new Map(vehicles.map((vehicle, index) => [vehicle.id, getStableVehicleColor(vehicle.id, index)])), [vehicles]);
  const loaderColors = useMemo(() => new Map(loaders.map((loader, index) => [loader.id, getStableLoaderColor(loader.id, index)])), [loaders]);
  const lengths = useMemo(() => new Map(vehicles.map((vehicle) => [vehicle.id, calculateCoordinateRouteLength(vehicle.route, depot, orderById)])), [vehicles, depot, orderById]);
  const loaderOrderSets = useMemo(() => new Map(loaders.map((loader) => [loader.id, new Set(getRouteOrderIds(loader.route))])), [loaders]);
  const [selectedVehicleId, setSelectedVehicleId] = useState<number | null>(null);
  const [selectedLoaderId, setSelectedLoaderId] = useState<number | null>(null);
  const [topThree, setTopThree] = useState(false);
  const [showLoaders, setShowLoaders] = useState(false);
  const [sortMode, setSortMode] = useState<SortMode>("id");
  const [hoveredOrder, setHoveredOrder] = useState<{ order: RouteOrder; stop?: number; total?: number; unserved?: boolean } | null>(null);

  const topIds = useMemo(() => new Set([...vehicles].sort((a, b) => (lengths.get(b.id) ?? 0) - (lengths.get(a.id) ?? 0)).slice(0, 3).map((vehicle) => vehicle.id)), [vehicles, lengths]);
  const visibleVehicles = useMemo(() => topThree ? vehicles.filter((vehicle) => topIds.has(vehicle.id)) : vehicles, [vehicles, topThree, topIds]);
  const visibleOrderIds = useMemo(() => new Set(visibleVehicles.flatMap((vehicle) => getRouteOrderIds(vehicle.route))), [visibleVehicles]);
  const visibleLoaders = useMemo(() => {
    if (!showLoaders) return [];
    return loaders.filter((loader) => [...(loaderOrderSets.get(loader.id) ?? [])].some((id) => visibleOrderIds.has(id)));
  }, [showLoaders, loaders, loaderOrderSets, visibleOrderIds]);
  const rankedIds = useMemo(() => new Map([...visibleVehicles].sort((a, b) => (lengths.get(b.id) ?? 0) - (lengths.get(a.id) ?? 0)).map((vehicle, index) => [vehicle.id, index + 1])), [visibleVehicles, lengths]);
  const sortedVehicles = useMemo(() => [...visibleVehicles].sort((a, b) => {
    if (sortMode === "length") return (lengths.get(b.id) ?? 0) - (lengths.get(a.id) ?? 0);
    if (sortMode === "orders") return getRouteOrderIds(b.route).length - getRouteOrderIds(a.route).length;
    return a.id - b.id;
  }), [visibleVehicles, sortMode, lengths]);
  const selectedVehicle = vehicles.find((vehicle) => vehicle.id === selectedVehicleId) ?? null;
  const selectedLoader = loaders.find((loader) => loader.id === selectedLoaderId) ?? null;
  const selectedIds = useMemo(() => getRouteOrderIds(selectedVehicle?.route), [selectedVehicle]);
  const selectedLoaderIds = useMemo(() => getRouteOrderIds(selectedLoader?.route), [selectedLoader]);
  const selectedIdSet = useMemo(() => new Set(selectedIds), [selectedIds]);
  const selectedLoaders = useMemo(() => selectedVehicle ? getLoadersForVehicleRoute(selectedVehicle.route, loaders) : [], [selectedVehicle, loaders]);

  const allDisplayPoints = useMemo(() => {
    const routePoints = visibleVehicles.flatMap((vehicle) => getRoutePoints(vehicle.route, depot, orderById));
    const loaderPoints = visibleLoaders.flatMap((loader) => getRouteOrderIds(loader.route).map((id) => orderById.get(id)).filter((order): order is RouteOrder => !!order));
    return [...routePoints, ...loaderPoints].filter(isFinitePoint).map(displayPoint);
  }, [visibleVehicles, visibleLoaders, depot, orderById]);
  const fitAllView = useMemo(() => calculateViewBoxForPoints(allDisplayPoints, DEFAULT_VIEW, 8), [allDisplayPoints]);
  const selectedDisplayPoints = useMemo(() => {
    if (selectedVehicle) return getRoutePoints(selectedVehicle.route, depot, orderById).map(displayPoint);
    if (selectedLoader) return selectedLoaderIds.map((id) => orderById.get(id)).filter((order): order is RouteOrder => !!order).map(displayPoint);
    return [];
  }, [selectedVehicle, selectedLoader, selectedLoaderIds, depot, orderById]);

  const [viewBox, setViewBox] = useState<ViewBox>(fitAllView);
  const svgRef = useRef<SVGSVGElement>(null);
  const drag = useRef<{ x: number; y: number; view: ViewBox } | null>(null);
  const fitAll = useCallback(() => setViewBox(fitAllView), [fitAllView]);
  const fitSelected = useCallback(() => {
    if (selectedDisplayPoints.length) setViewBox(calculateViewBoxForPoints(selectedDisplayPoints, fitAllView, 6));
  }, [selectedDisplayPoints, fitAllView]);

  useEffect(() => { fitAll(); }, [topThree, fitAll]);
  useEffect(() => { if (selectedVehicle || selectedLoader) fitSelected(); }, [selectedVehicleId, selectedLoaderId, selectedVehicle, selectedLoader, fitSelected]);
  useEffect(() => { if (selectedVehicleId !== null && !vehicles.some((vehicle) => vehicle.id === selectedVehicleId)) setSelectedVehicleId(null); }, [vehicles, selectedVehicleId]);
  useEffect(() => {
    if (topThree && selectedVehicleId !== null && !topIds.has(selectedVehicleId)) setSelectedVehicleId(null);
  }, [topThree, topIds, selectedVehicleId]);
  useEffect(() => {
    if (!showLoaders || (selectedLoaderId !== null && !visibleLoaders.some((loader) => loader.id === selectedLoaderId))) setSelectedLoaderId(null);
  }, [showLoaders, visibleLoaders, selectedLoaderId]);

  const selectVehicle = useCallback((id: number) => {
    setSelectedLoaderId(null);
    setSelectedVehicleId((current) => current === id ? null : id);
  }, []);
  const selectLoader = useCallback((id: number) => {
    setSelectedVehicleId(null);
    setSelectedLoaderId((current) => current === id ? null : id);
  }, []);
  const zoom = useCallback((factor: number, cx = viewBox.x + viewBox.w / 2, cy = viewBox.y + viewBox.h / 2) => {
    setViewBox((current) => {
      const w = Math.max(current.w * factor, 0.01);
      const h = Math.max(current.h * factor, 0.01);
      return { x: cx - (w * (cx - current.x)) / current.w, y: cy - (h * (cy - current.y)) / current.h, w, h };
    });
  }, [viewBox]);
  const handleWheel = useCallback((event: React.WheelEvent<SVGSVGElement>) => {
    event.preventDefault();
    const svg = svgRef.current;
    const matrix = svg?.getScreenCTM();
    if (!svg || !matrix) return;
    const point = svg.createSVGPoint();
    point.x = event.clientX;
    point.y = event.clientY;
    const position = point.matrixTransform(matrix.inverse());
    zoom(event.deltaY > 0 ? 1.12 : 0.88, position.x, position.y);
  }, [zoom]);
  const beginPan = (event: React.MouseEvent<SVGSVGElement>) => { drag.current = { x: event.clientX, y: event.clientY, view: viewBox }; };
  const pan = (event: React.MouseEvent<SVGSVGElement>) => {
    if (!drag.current || !svgRef.current) return;
    const rect = svgRef.current.getBoundingClientRect();
    setViewBox({ ...drag.current.view, x: drag.current.view.x - (event.clientX - drag.current.x) * drag.current.view.w / rect.width, y: drag.current.view.y - (event.clientY - drag.current.y) * drag.current.view.h / rect.height });
  };

  const routePointsAttr = (route: number[] | undefined, includeDepot = true) => {
    const points = includeDepot ? getRoutePoints(route, depot, orderById) : getRouteOrderIds(route).map((id) => orderById.get(id)).filter((order): order is RouteOrder => !!order);
    const closed = !includeDepot && points.length > 1 ? [...points, points[0]] : points;
    return closed.filter(isFinitePoint).map(displayPoint).map((point) => `${point.x},${point.y}`).join(" ");
  };

  const routeOwner = (orderId: number) => visibleVehicles.find((vehicle) => getRouteOrderIds(vehicle.route).includes(orderId));
  const hasData = !!depot || orders.length > 0;

  return (
    <section className="mb-5 rounded-xl border border-blue-100 bg-white p-4 shadow-sm" aria-labelledby="route-plan-title">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-2"><RouteIcon size={17} className="text-blue-600" /><h2 id="route-plan-title" className="m-0 text-base font-semibold text-gray-900">Route Plan</h2></div>
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <button className={`rounded-md border px-3 py-1.5 font-medium ${topThree ? "border-blue-600 bg-blue-50 text-blue-700" : "border-gray-200 bg-white text-gray-700"}`} aria-pressed={topThree} onClick={() => setTopThree((value) => !value)}>Top 3 longest</button>
          <label className="flex items-center gap-2 rounded-md border border-gray-200 bg-white px-3 py-1.5 text-gray-700"><input type="checkbox" checked={showLoaders} onChange={(event) => setShowLoaders(event.target.checked)} />Show loader routes</label>
          <button className="rounded-md border border-gray-200 bg-white px-3 py-1.5 font-medium text-gray-700" onClick={fitAll} title="Fit all active routes"><Maximize2 size={13} className="mr-1 inline" />Fit all</button>
          {(selectedVehicle || selectedLoader) && <button className="rounded-md border border-blue-200 bg-blue-50 px-3 py-1.5 font-medium text-blue-700" onClick={fitSelected}>Fit selected</button>}
        </div>
      </div>

      <div className={`grid min-w-0 grid-cols-1 gap-3 ${selectedVehicle || selectedLoader ? "lg:grid-cols-[minmax(180px,0.7fr)_minmax(0,2.2fr)_minmax(220px,0.9fr)]" : "lg:grid-cols-[minmax(190px,0.7fr)_minmax(0,2.7fr)]"}`}>
        <aside className="min-w-0 rounded-lg border border-gray-200 bg-white p-3">
          <div className="mb-2 flex items-center justify-between gap-2"><h3 className="m-0 text-sm font-semibold text-gray-900">Routes</h3><select className="min-w-0 rounded border border-gray-200 bg-white px-1 py-1 text-[11px] text-gray-700" aria-label="Sort routes" value={sortMode} onChange={(event) => setSortMode(event.target.value as SortMode)}><option value="id">Vehicle ID</option><option value="length">Longest first</option><option value="orders">Most orders</option></select></div>
          <div className="max-h-[440px] space-y-1 overflow-y-auto">
            {sortedVehicles.length === 0 && <p className="text-xs text-gray-500">No vehicle routes available.</p>}
            {sortedVehicles.map((vehicle) => {
              const selected = vehicle.id === selectedVehicleId;
              return <button key={vehicle.id} className={`flex w-full items-center gap-2 rounded-md border px-2 py-2 text-left ${selected ? "border-blue-500 bg-blue-50" : "border-transparent hover:bg-gray-50"}`} onClick={() => selectVehicle(vehicle.id)} aria-pressed={selected}>
                <span className="h-3 w-3 shrink-0 rounded-full" style={{ background: vehicleColors.get(vehicle.id) }} />
                <span className="min-w-0"><span className="block text-xs font-semibold text-gray-900">{topThree && `#${rankedIds.get(vehicle.id)} `}V-{vehicle.id}</span><span className="block text-[11px] text-gray-500">{getRouteOrderIds(vehicle.route).length} orders · {formatCoordinateLength(lengths.get(vehicle.id) ?? 0)}</span></span>
              </button>;
            })}
            {showLoaders && visibleLoaders.length > 0 && <p className="mb-1 mt-3 border-t border-gray-100 pt-2 text-[11px] font-semibold uppercase tracking-wide text-gray-500">Loader routes</p>}
            {showLoaders && visibleLoaders.map((loader) => {
              const selected = loader.id === selectedLoaderId;
              return <button key={`loader-list-${loader.id}`} className={`flex w-full items-center gap-2 rounded-md border px-2 py-2 text-left ${selected ? "border-purple-500 bg-purple-50" : "border-transparent hover:bg-gray-50"}`} onClick={() => selectLoader(loader.id)} aria-pressed={selected}>
                <span className="h-3 w-3 shrink-0 rounded-full" style={{ background: loaderColors.get(loader.id) }} />
                <span className="min-w-0"><span className="block text-xs font-semibold text-gray-900">L-{loader.id}</span><span className="block text-[11px] text-gray-500">{getRouteOrderIds(loader.route).length} service stops</span></span>
              </button>;
            })}
          </div>
        </aside>

        <div className="relative min-w-0 overflow-hidden rounded-lg border border-blue-100 bg-blue-50" style={{ height: 520 }}>
          {!hasData ? <div className="flex h-full items-center justify-center p-6 text-sm text-gray-500">No coordinate data available.</div> : <>
            <svg ref={svgRef} className="h-full w-full cursor-grab active:cursor-grabbing" viewBox={`${viewBox.x} ${viewBox.y} ${viewBox.w} ${viewBox.h}`} role="img" aria-label="Coordinate route plan" onWheel={handleWheel} onMouseDown={beginPan} onMouseMove={pan} onMouseUp={() => { drag.current = null; }} onMouseLeave={() => { drag.current = null; }}>
              <defs><pattern id="route-grid" width={Math.max(viewBox.w / 20, 1)} height={Math.max(viewBox.w / 20, 1)} patternUnits="userSpaceOnUse"><path d={`M ${Math.max(viewBox.w / 20, 1)} 0 L 0 0 0 ${Math.max(viewBox.w / 20, 1)}`} fill="none" stroke="#93C5FD" strokeWidth={viewBox.w / 1400} /></pattern></defs>
              <rect x={viewBox.x} y={viewBox.y} width={viewBox.w} height={viewBox.h} fill="url(#route-grid)" opacity={0.22} />
              {visibleLoaders.map((loader) => {
                const selected = loader.id === selectedLoaderId;
                const related = selectedLoader ? selected : !selectedVehicle || (loaderOrderSets.get(loader.id) && [...loaderOrderSets.get(loader.id)!].some((id) => selectedIdSet.has(id)));
                return <polyline key={`loader-${loader.id}`} points={routePointsAttr(loader.route, false)} fill="none" stroke={loaderColors.get(loader.id)} strokeWidth={selected ? 4 : 2} opacity={related ? (selected ? 1 : 0.85) : 0.1} vectorEffect="non-scaling-stroke" role="button" aria-label={`Select loader route L-${loader.id}`} onMouseDown={(event) => event.stopPropagation()} onClick={() => selectLoader(loader.id)}><title>Loader route L-{loader.id}: {getRouteOrderIds(loader.route).length} service stops</title></polyline>;
              })}
              {visibleVehicles.filter((vehicle) => vehicle.id !== selectedVehicleId).map((vehicle) => <polyline key={`vehicle-${vehicle.id}`} points={routePointsAttr(vehicle.route)} fill="none" stroke={vehicleColors.get(vehicle.id)} strokeWidth={1.6} strokeDasharray="6 4" opacity={selectedVehicle || selectedLoader ? 0.1 : 0.34} vectorEffect="non-scaling-stroke" role="button" aria-label={`Select vehicle route V-${vehicle.id}`} onMouseDown={(event) => event.stopPropagation()} onClick={() => selectVehicle(vehicle.id)}><title>Vehicle route V-{vehicle.id}</title></polyline>)}
              {selectedVehicle && <polyline points={routePointsAttr(selectedVehicle.route)} fill="none" stroke={vehicleColors.get(selectedVehicle.id)} strokeWidth={4} strokeDasharray="7 4" opacity={1} vectorEffect="non-scaling-stroke" role="button" aria-label={`Selected vehicle route V-${selectedVehicle.id}`} onMouseDown={(event) => event.stopPropagation()} onClick={() => selectVehicle(selectedVehicle.id)}><title>Selected vehicle route V-{selectedVehicle.id}</title></polyline>}
              {orders.map((order) => {
                const point = displayPoint(order);
                const unserved = unservedOptional.includes(order.id);
                const muted = selectedVehicle ? !selectedIdSet.has(order.id) : selectedLoader ? !selectedLoaderIds.includes(order.id) : false;
                return <circle key={`order-${order.id}`} cx={point.x} cy={point.y} r={viewBox.w / (unserved ? 185 : 260)} fill={unserved ? "white" : "#64748B"} stroke={unserved ? "#64748B" : "white"} strokeWidth={1.2} opacity={muted ? 0.22 : 0.75} vectorEffect="non-scaling-stroke" tabIndex={0} role="button" aria-label={`Order ${order.id} at coordinates ${order.x}, ${order.y}`} onMouseDown={(event) => event.stopPropagation()} onClick={() => { const owner = routeOwner(order.id); if (owner) selectVehicle(owner.id); }} onMouseEnter={() => setHoveredOrder({ order, unserved })} onMouseLeave={() => setHoveredOrder(null)} onFocus={() => setHoveredOrder({ order, unserved })} onBlur={() => setHoveredOrder(null)}><title>{`${unserved ? "Unserved optional order. " : ""}Order ${order.id}; coordinates (${order.x}, ${order.y})`}</title></circle>;
              })}
              {selectedVehicle && selectedIds.map((id, index) => {
                const order = orderById.get(id);
                if (!order) return null;
                const point = displayPoint(order);
                const radius = Math.max(viewBox.w / 105, 2.8);
                return <g key={`stop-${index}-${id}`} role="button" tabIndex={0} aria-label={`Stop ${index + 1} of ${selectedIds.length}, order ${id}`} onMouseDown={(event) => event.stopPropagation()} onClick={() => selectVehicle(selectedVehicle.id)} onMouseEnter={() => setHoveredOrder({ order, stop: index + 1, total: selectedIds.length })} onMouseLeave={() => setHoveredOrder(null)} onFocus={() => setHoveredOrder({ order, stop: index + 1, total: selectedIds.length })} onBlur={() => setHoveredOrder(null)}><circle cx={point.x} cy={point.y} r={radius} fill={vehicleColors.get(selectedVehicle.id)} stroke="white" strokeWidth={2} vectorEffect="non-scaling-stroke" /><text x={point.x} y={point.y} fill="white" fontSize={radius * 1.05} fontWeight={700} textAnchor="middle" dominantBaseline="central" pointerEvents="none">{index + 1}</text><title>{`Stop ${index + 1} of ${selectedIds.length}; order ${id}; coordinates (${order.x}, ${order.y})`}</title></g>;
              })}
              {selectedLoader && selectedLoaderIds.map((id, index) => {
                const order = orderById.get(id);
                if (!order) return null;
                const point = displayPoint(order);
                const radius = Math.max(viewBox.w / 105, 2.8);
                return <g key={`loader-stop-${index}-${id}`} role="button" tabIndex={0} aria-label={`Loader stop ${index + 1} of ${selectedLoaderIds.length}, order ${id}`} onMouseDown={(event) => event.stopPropagation()} onMouseEnter={() => setHoveredOrder({ order, stop: index + 1, total: selectedLoaderIds.length })} onMouseLeave={() => setHoveredOrder(null)} onFocus={() => setHoveredOrder({ order, stop: index + 1, total: selectedLoaderIds.length })} onBlur={() => setHoveredOrder(null)}><circle cx={point.x} cy={point.y} r={radius} fill={loaderColors.get(selectedLoader.id)} stroke="white" strokeWidth={2} vectorEffect="non-scaling-stroke" /><text x={point.x} y={point.y} fill="white" fontSize={radius * 1.05} fontWeight={700} textAnchor="middle" dominantBaseline="central" pointerEvents="none">{index + 1}</text><title>{`Loader stop ${index + 1} of ${selectedLoaderIds.length}; order ${id}; coordinates (${order.x}, ${order.y})`}</title></g>;
              })}
              {depot && (() => { const point = displayPoint(depot); const size = Math.max(viewBox.w / 80, 4); return <g><rect x={point.x - size / 2} y={point.y - size / 2} width={size} height={size} rx={size / 8} fill="#1D4ED8" stroke="white" strokeWidth={2} vectorEffect="non-scaling-stroke" /><text x={point.x} y={point.y - size * 0.8} fontSize={Math.max(viewBox.w / 65, 4)} fill="#1D4ED8" fontWeight={700} textAnchor="middle">Depot</text><title>{`Depot (${depot.x}, ${depot.y})`}</title></g>; })()}
            </svg>
            <div className="absolute right-2 top-2 flex gap-1"><button className="rounded border border-gray-200 bg-white px-2 py-1 text-xs" aria-label="Zoom out" onClick={() => zoom(1.15)}>−</button><button className="rounded border border-gray-200 bg-white px-2 py-1 text-xs" aria-label="Reset view" onClick={fitAll}>Reset</button><button className="rounded border border-gray-200 bg-white px-2 py-1 text-xs" aria-label="Zoom in" onClick={() => zoom(0.85)}>+</button></div>
            <div className="pointer-events-none absolute bottom-2 right-2 text-[10px] text-gray-400">Scroll to zoom · Drag to pan</div>
            {showLoaders && <div className="absolute left-2 top-2 rounded border border-gray-200 bg-white/95 px-2 py-1 text-[10px] text-gray-600"><span className="mr-3">- - dashed — vehicle route</span><span>— solid — loader route</span></div>}
            {hoveredOrder && <OrderTooltip {...hoveredOrder} />}
          </>}
        </div>

        {selectedVehicle && <aside className="min-w-0 rounded-lg border border-gray-200 bg-white p-3">
          <div className="mb-2 flex flex-wrap items-center justify-between gap-2"><h3 className="m-0 text-sm font-semibold" style={{ color: vehicleColors.get(selectedVehicle.id) }}>Route V-{selectedVehicle.id}</h3><button className="inline-flex items-center gap-1 rounded border border-gray-200 px-2 py-1 text-[11px] text-gray-600 hover:bg-gray-100" aria-label="Clear selection" title="Clear selection" onClick={() => setSelectedVehicleId(null)}><X size={12} />Clear selection</button></div>
          <dl className="m-0 space-y-1 text-xs"><div><dt className="inline font-semibold">Orders: </dt><dd className="inline">{selectedIds.length}</dd></div><div><dt className="inline font-semibold">Coordinate length: </dt><dd className="inline">{formatCoordinateLength(lengths.get(selectedVehicle.id) ?? 0)}</dd></div><div className="break-words"><dt className="font-semibold">Route:</dt><dd className="m-0">Depot → {selectedIds.join(" → ")} → Depot</dd></div>{selectedLoaders.length > 0 && <div><dt className="font-semibold">Loaders serving route orders:</dt><dd className="m-0">{selectedLoaders.map((loader) => `L-${loader.id}`).join(", ")}</dd></div>}</dl>
          <h4 className="mb-1 mt-3 text-xs font-semibold text-gray-900">Stops</h4><ol className="m-0 max-h-[310px] space-y-1 overflow-y-auto p-0">{selectedIds.map((id, index) => { const order = orderById.get(id); return <li key={`${id}-${index}`} className="list-none rounded bg-gray-50 p-2 text-[11px] text-gray-700"><strong>{index + 1}. Order {id}</strong>{order && <><span className="block">Coordinates: ({order.x}, {order.y})</span>{optionalValue(order.volume) && <span className="block">Volume: {optionalValue(order.volume)}</span>}{optionalValue(order.time_window) && <span className="block">Time window: {optionalValue(order.time_window)}</span>}{optionalValue(order.vehicle_service_time) && <span className="block">Vehicle service time: {optionalValue(order.vehicle_service_time)}</span>}{optionalValue(order.loader_cnt) && <span className="block">Required loaders: {optionalValue(order.loader_cnt)}</span>}{optionalValue(order.loader_service_time) && <span className="block">Loader service time: {optionalValue(order.loader_service_time)}</span>}{optionalValue(order.optional) && <span className="block">Optional: {optionalValue(order.optional)}</span>}</>}</li>; })}</ol>
        </aside>}
        {selectedLoader && <aside className="min-w-0 rounded-lg border border-purple-200 bg-white p-3">
          <div className="mb-2 flex flex-wrap items-center justify-between gap-2"><h3 className="m-0 text-sm font-semibold" style={{ color: loaderColors.get(selectedLoader.id) }}>Loader route L-{selectedLoader.id}</h3><button className="inline-flex items-center gap-1 rounded border border-gray-200 px-2 py-1 text-[11px] text-gray-600 hover:bg-gray-100" aria-label="Clear loader selection" onClick={() => setSelectedLoaderId(null)}><X size={12} />Clear selection</button></div>
          <dl className="m-0 space-y-1 text-xs"><div><dt className="inline font-semibold">Service stops: </dt><dd className="inline">{selectedLoaderIds.length}</dd></div><div className="break-words"><dt className="font-semibold">Route:</dt><dd className="m-0">{selectedLoaderIds.length ? `${selectedLoaderIds.join(" → ")} → ${selectedLoaderIds[0]}` : "—"}</dd></div><div><dt className="font-semibold">Vehicle routes containing these orders:</dt><dd className="m-0">{vehicles.filter((vehicle) => getRouteOrderIds(vehicle.route).some((id) => selectedLoaderIds.includes(id))).map((vehicle) => `V-${vehicle.id}`).join(", ") || "—"}</dd></div></dl>
          <h4 className="mb-1 mt-3 text-xs font-semibold text-gray-900">Service stops</h4><ol className="m-0 max-h-[330px] space-y-1 overflow-y-auto p-0">{selectedLoaderIds.map((id, index) => { const order = orderById.get(id); return <li key={`loader-detail-${id}-${index}`} className="list-none rounded bg-purple-50 p-2 text-[11px] text-gray-700"><strong>{index + 1}. Order {id}</strong>{order && <><span className="block">Coordinates: ({order.x}, {order.y})</span>{optionalValue(order.loader_service_time) && <span className="block">Loader service time: {optionalValue(order.loader_service_time)}</span>}{optionalValue(order.loader_cnt) && <span className="block">Required loaders: {optionalValue(order.loader_cnt)}</span>}{optionalValue(order.time_window) && <span className="block">Time window: {optionalValue(order.time_window)}</span>}{optionalValue(order.optional) && <span className="block">Optional: {optionalValue(order.optional)}</span>}</>}</li>; })}</ol>
        </aside>}
      </div>
    </section>
  );
}
