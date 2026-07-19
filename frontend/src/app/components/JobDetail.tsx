import { useEffect, useState } from "react";
import { ArrowLeft, CheckCircle2, Download, Loader2, RotateCcw, XCircle } from "lucide-react";
import { getJob, getJobSolution } from "../../api/jobs";
import type { Job } from "../../types";
import { formatExecutionTime, type LoaderRoute, type VehicleRoute } from "../utils/routeMetrics";
import type { Page } from "../App";
import { GanttSchedule } from "./GanttSchedule";
import { RoutePlan } from "./RoutePlan";

const TABS = ["Routes", "Schedule", "Validation", "Raw JSON"] as const;
type Tab = (typeof TABS)[number];

interface Props { id: string; navigate: (page: Page) => void }

const formatRoute = (route?: number[]) => (route ?? []).map((id) => id === 0 ? "Depot" : String(id)).join(" → ");
const formatLoaderRoute = (route?: number[]) => {
  const orders = (route ?? []).filter((id) => id !== 0);
  return orders.length ? [...orders, orders[0]].join(" → ") : "";
};
const formatObjective = (value?: number) => Number.isFinite(value) ? value!.toFixed(2) : "—";

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
        if (!cancelled) { setJob(data); setIsLoading(false); }
      } catch (reason) {
        if (!cancelled) { setError(reason instanceof Error ? reason.message : "Job not found"); setIsLoading(false); }
      }
    }
    load();
    const interval = window.setInterval(() => {
      if (job?.status === "completed" || job?.status === "failed") window.clearInterval(interval);
      else load();
    }, 1000);
    return () => { cancelled = true; window.clearInterval(interval); };
  }, [id, job?.status]);

  if (isLoading) return <p className="p-6 text-gray-600">Loading job…</p>;
  if (error || !job) return <p className="p-6 text-red-600">{error || "Job not found"}</p>;

  const vehicles = (job.result?.vehicles as VehicleRoute[] | undefined) ?? [];
  const loaders = (job.result?.loaders as LoaderRoute[] | undefined) ?? [];
  const validation = job.validation_report;

  const downloadSolution = async () => {
    try {
      const solution = await getJobSolution(job.job_id);
      const url = URL.createObjectURL(new Blob([JSON.stringify(solution, null, 2)], { type: "application/json" }));
      const link = document.createElement("a");
      link.href = url;
      link.download = `${job.job_id}-solution.json`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (reason) {
      alert(reason instanceof Error ? reason.message : "Solution not available");
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6">
        <button onClick={() => navigate({ name: "dashboard" })} className="mb-5 inline-flex items-center gap-1.5 border-0 bg-transparent p-0 text-sm font-medium text-blue-600 hover:underline"><ArrowLeft size={15} />Dashboard</button>

        <header className="mb-5 rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
          <div className="flex flex-col justify-between gap-4 md:flex-row md:items-start">
            <div className="min-w-0">
              <div className="mb-1 flex flex-wrap items-center gap-3">
                <h1 className="m-0 text-xl font-semibold text-gray-900">{job.name || "Untitled job"}</h1>
                {job.status === "completed" && <span className="inline-flex items-center gap-1 rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-700"><CheckCircle2 size={12} />Completed</span>}
                {job.status === "failed" && <span className="inline-flex items-center gap-1 rounded-full bg-red-100 px-2.5 py-0.5 text-xs font-medium text-red-700"><XCircle size={12} />Failed</span>}
                {job.status === "running" && <span className="inline-flex items-center gap-1 rounded-full bg-blue-100 px-2.5 py-0.5 text-xs font-medium text-blue-700"><Loader2 size={12} className="animate-spin" />Running</span>}
                {job.status === "pending" && <span className="rounded-full bg-yellow-100 px-2.5 py-0.5 text-xs font-medium text-yellow-700">Pending</span>}
              </div>
              <p className="mb-4 break-all font-mono text-xs text-gray-400">{job.job_id}</p>
              <div className="flex flex-wrap gap-x-8 gap-y-3">
                {[
                  ["Seed", String(job.seed ?? "—")],
                  ["Objective", formatObjective(job.objective_value)],
                  ["Validation", job.validation_status ?? "—"],
                  ["Execution time", formatExecutionTime(job.started_at, job.finished_at)],
                ].map(([label, value]) => <div key={label}><p className="m-0 mb-0.5 text-xs font-medium text-gray-500">{label}</p><p className={`m-0 text-base font-semibold ${label === "Validation" && value === "passed" ? "text-green-700" : "text-gray-900"}`}>{value}</p></div>)}
              </div>
            </div>
            <div className="flex flex-wrap gap-2">
              <button className="flex items-center gap-1.5 rounded-lg border border-gray-200 bg-white px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-50" onClick={downloadSolution}><Download size={14} />Download JSON</button>
              <button className="flex items-center gap-1.5 rounded-lg border border-blue-200 bg-blue-50 px-3 py-1.5 text-sm font-medium text-blue-600 hover:bg-blue-100" onClick={() => navigate({ name: "new-job" })}><RotateCcw size={14} />Re-run</button>
            </div>
          </div>
        </header>

        {job.unserved_optional && job.unserved_optional.length > 0 && <div className="mb-5 rounded-lg border border-yellow-200 bg-yellow-50 p-4"><h3 className="m-0 mb-1.5 text-sm font-semibold text-yellow-800">Skipped optional orders</h3><p className="m-0 text-sm text-yellow-700">{job.unserved_optional.join(", ")}</p></div>}
        {job.unserved_optional?.length === 0 && <div className="mb-5 text-sm text-gray-600">No optional orders were skipped.</div>}

        <RoutePlan inputData={job.input_data} vehicles={vehicles} loaders={loaders} unservedOptional={job.unserved_optional} />

        <section className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
          <div className="flex overflow-x-auto border-b border-gray-100">
            {TABS.map((tab) => <button key={tab} onClick={() => setActiveTab(tab)} className={`whitespace-nowrap border-0 border-b-2 bg-transparent px-5 py-3 text-sm ${activeTab === tab ? "border-blue-600 font-semibold text-blue-600" : "border-transparent text-gray-500"}`}>{tab}</button>)}
          </div>
          <div className="p-4 sm:p-6">
            {activeTab === "Routes" && <RouteTables vehicles={vehicles} loaders={loaders} />}
            {activeTab === "Schedule" && <div><h3 className="mb-3 mt-0 text-sm font-semibold text-gray-900">Schedule</h3><p className="mb-3 mt-0 text-sm text-gray-500">Interactive vehicle and loader schedule reconstructed from solver arrival times and the saved instance data.</p><GanttSchedule vehicles={vehicles.map((vehicle) => ({ ...vehicle, time: vehicle.time ?? [] }))} loaders={loaders} inputData={job.input_data} /></div>}
            {activeTab === "Validation" && <ValidationPanel validation={validation} />}
            {activeTab === "Raw JSON" && <pre className="m-0 max-h-96 overflow-auto rounded-lg bg-slate-800 p-5 font-mono text-xs leading-relaxed text-slate-200">{JSON.stringify(job.result ?? job, null, 2)}</pre>}
          </div>
        </section>
      </div>
    </div>
  );
}

function RouteTables({ vehicles, loaders }: { vehicles: VehicleRoute[]; loaders: LoaderRoute[] }) {
  return <div>
    <h3 className="mb-3 mt-0 text-sm font-semibold text-gray-900">Vehicle Routes</h3>
    {vehicles.length === 0 ? <p className="text-sm text-gray-500">No vehicle routes available.</p> : <div className="mb-6 overflow-x-auto"><table className="w-full border-collapse text-left"><thead><tr className="border-b border-gray-100">{["Vehicle", "Route", "Start Time"].map((column) => <th key={column} className="px-3 py-2 text-[11px] font-semibold uppercase tracking-wide text-gray-500">{column}</th>)}</tr></thead><tbody>{vehicles.map((vehicle) => <tr key={vehicle.id} className="hover:bg-gray-50"><td className="px-3 py-2.5 text-sm font-medium text-gray-900">V-{vehicle.id}</td><td className="px-3 py-2.5 font-mono text-xs text-gray-700">{formatRoute(vehicle.route)}</td><td className="px-3 py-2.5 text-sm text-gray-500">{vehicle.time?.[0] ?? "—"}</td></tr>)}</tbody></table></div>}
    <h3 className="mb-3 mt-0 text-sm font-semibold text-gray-900">Loader Routes</h3>
    {loaders.length === 0 ? <p className="text-sm text-gray-500">No loader routes available.</p> : <div className="overflow-x-auto"><table className="w-full border-collapse text-left"><thead><tr className="border-b border-gray-100"><th className="px-3 py-2 text-[11px] font-semibold uppercase tracking-wide text-gray-500">Loader</th><th className="px-3 py-2 text-[11px] font-semibold uppercase tracking-wide text-gray-500">Route</th></tr></thead><tbody>{loaders.map((loader) => <tr key={loader.id} className="hover:bg-gray-50"><td className="px-3 py-2.5 text-sm font-medium text-gray-900">L-{loader.id}</td><td className="px-3 py-2.5 font-mono text-xs text-gray-700">{formatLoaderRoute(loader.route)}</td></tr>)}</tbody></table></div>}
  </div>;
}

function ValidationPanel({ validation }: { validation?: Record<string, unknown> }) {
  const violations = Array.isArray(validation?.violations) ? validation.violations as string[] : [];
  return <div>{validation?.passed ? <div className="mb-4 flex items-center gap-3 rounded-lg border border-green-200 bg-green-50 p-4"><CheckCircle2 size={20} className="text-green-700" /><div><p className="m-0 font-semibold text-green-700">Validation Passed</p><p className="m-0 mt-0.5 text-sm text-green-800">Objective value: <strong>{formatObjective(validation.objective_value as number | undefined)}</strong></p></div></div> : <div className="mb-4 flex items-center gap-3 rounded-lg border border-red-200 bg-red-50 p-4"><XCircle size={20} className="text-red-600" /><p className="m-0 font-semibold text-red-600">Validation Failed</p></div>}{violations.length ? <><p className="mb-2 text-sm font-semibold">Violations:</p><ul className="m-0 pl-5">{violations.map((violation, index) => <li key={index} className="mb-1 text-sm text-red-800">{violation}</li>)}</ul></> : <p className="text-sm text-gray-500">{validation ? "No constraint violations detected." : "No validation report available."}</p>}</div>;
}
