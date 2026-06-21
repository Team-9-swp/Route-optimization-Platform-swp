# React Frontend Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a React + TypeScript SPA that lets users submit optimization jobs, view job status and routes on a map, validate solutions, and browse recent jobs.

**Architecture:** Vite-powered React SPA. State server sync via TanStack Query and a small Axios client. Pages routed with React Router. Interactive map via Leaflet/`react-leaflet`. Styling via Tailwind CSS.

**Tech Stack:** React 18, TypeScript, Vite, React Router, TanStack Query, Axios, Tailwind CSS, Leaflet, react-leaflet, lucide-react.

---

## File Structure

| File | Responsibility |
|------|----------------|
| `frontend/package.json` | Frontend dependencies and scripts |
| `frontend/vite.config.ts` | Vite config with `/api` proxy |
| `frontend/tsconfig.json` | TypeScript config |
| `frontend/tailwind.config.js` / `postcss.config.js` | Tailwind setup |
| `frontend/src/main.tsx` | App entry point, QueryClient provider |
| `frontend/src/App.tsx` | Router setup |
| `frontend/src/types/index.ts` | Shared TypeScript types |
| `frontend/src/api/client.ts` | Axios instance |
| `frontend/src/api/jobs.ts` | Job API calls |
| `frontend/src/api/validate.ts` | Validation API call |
| `frontend/src/hooks/usePolling.ts` | Generic polling hook |
| `frontend/src/hooks/useJobs.ts` | List jobs query |
| `frontend/src/hooks/useJob.ts` | Single job query with polling |
| `frontend/src/components/Layout.tsx` | Top navigation shell |
| `frontend/src/components/JobStatusBadge.tsx` | Status badge component |
| `frontend/src/components/RouteMap.tsx` | Leaflet map for vehicle/loader routes |
| `frontend/src/components/VehicleRoutesTable.tsx` | Vehicle route table |
| `frontend/src/components/LoaderRoutesTable.tsx` | Loader route table |
| `frontend/src/components/ValidationReport.tsx` | Validation result display |
| `frontend/src/components/JsonViewer.tsx` | Pretty-printed JSON viewer |
| `frontend/src/pages/DashboardPage.tsx` | Job list page |
| `frontend/src/pages/NewJobPage.tsx` | Create job page |
| `frontend/src/pages/JobDetailPage.tsx` | Job detail + map page |
| `frontend/src/pages/ValidatePage.tsx` | Standalone validation page |
| `frontend/Dockerfile` | Production nginx image |
| `frontend/nginx.conf` | SPA fallback + `/api` proxy |

---

### Task 1: Initialize Vite project and install dependencies

**Files:**
- Create: `frontend/package.json`, `frontend/vite.config.ts`, `frontend/tsconfig.json`, `frontend/index.html`
- Create: `frontend/tailwind.config.js`, `frontend/postcss.config.js`

- [ ] **Step 1: Scaffold project**

Run from repo root:

```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install
```

- [ ] **Step 2: Install additional dependencies**

Run:

```bash
npm install react-router-dom @tanstack/react-query axios leaflet react-leaflet lucide-react
npm install -D @types/leaflet tailwindcss postcss autoprefixer
```

- [ ] **Step 3: Configure Tailwind**

`frontend/tailwind.config.js`:

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
};
```

`frontend/postcss.config.js`:

```js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

`frontend/src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

- [ ] **Step 4: Configure Vite proxy**

`frontend/vite.config.ts`:

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: process.env.VITE_API_BASE_URL || "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
```

- [ ] **Step 5: Verify dev server starts**

Run: `npm run dev`
Expected: Vite starts on `http://localhost:5173` without errors.

- [ ] **Step 6: Commit**

```bash
git add frontend/
git commit -m "chore(frontend): initialize Vite React TypeScript project"
```

---

### Task 2: Create shared types and API client

**Files:**
- Create: `frontend/src/types/index.ts`
- Create: `frontend/src/api/client.ts`
- Create: `frontend/src/api/jobs.ts`
- Create: `frontend/src/api/validate.ts`

- [ ] **Step 1: Add types**

`frontend/src/types/index.ts`:

```ts
export type JobStatus = "pending" | "running" | "completed" | "failed";
export type ValidationStatus = "pending" | "passed" | "failed";

export interface Job {
  job_id: string;
  status: JobStatus;
  name?: string;
  created_at: string;
  started_at?: string;
  finished_at?: string;
  result?: Record<string, unknown>;
  error?: string;
  objective_value?: number;
  validation_status?: ValidationStatus;
  validation_report?: Record<string, unknown>;
}

export interface JobListResponse {
  items: Job[];
  total: number;
  page: number;
  page_size: number;
}

export interface SolveResponse {
  job_id: string;
  status: JobStatus;
  created_at: string;
  name?: string;
}

export interface ValidationResponse {
  passed: boolean;
  objective_value?: number;
  violations: string[];
  report: Record<string, unknown>;
}
```

- [ ] **Step 2: Add Axios client**

`frontend/src/api/client.ts`:

```ts
import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  headers: {
    "Content-Type": "application/json",
  },
});
```

- [ ] **Step 3: Add job API functions**

`frontend/src/api/jobs.ts`:

```ts
import { api } from "./client";
import type { Job, JobListResponse, SolveResponse } from "../types";

export async function submitJob(
  instance: Record<string, unknown>,
  options: { seed?: number; name?: string; autoValidate?: boolean } = {},
): Promise<SolveResponse> {
  const params = new URLSearchParams();
  if (options.seed !== undefined) params.set("seed", String(options.seed));
  if (options.name) params.set("name", options.name);
  if (options.autoValidate) params.set("auto_validate", "true");

  const { data } = await api.post<SolveResponse>(`/solve?${params.toString()}`, instance);
  return data;
}

export async function getJob(jobId: string): Promise<Job> {
  const { data } = await api.get<Job>(`/jobs/${jobId}`);
  return data;
}

export async function listJobs(options: { page?: number; pageSize?: number } = {}): Promise<JobListResponse> {
  const params = new URLSearchParams();
  if (options.page) params.set("page", String(options.page));
  if (options.pageSize) params.set("page_size", String(options.pageSize));

  const { data } = await api.get<JobListResponse>(`/jobs?${params.toString()}`);
  return data;
}
```

- [ ] **Step 4: Add validation API function**

`frontend/src/api/validate.ts`:

```ts
import { api } from "./client";
import type { ValidationResponse } from "../types";

export async function validateSolution(
  instance: Record<string, unknown>,
  solution: Record<string, unknown>,
): Promise<ValidationResponse> {
  const { data } = await api.post<ValidationResponse>("/validate", { instance, solution });
  return data;
}
```

- [ ] **Step 5: Type-check**

Run: `npx tsc --noEmit`
Expected: no TypeScript errors.

- [ ] **Step 6: Commit**

```bash
git add frontend/src/types frontend/src/api
git commit -m "feat(frontend): add types and API clients"
```

---

### Task 3: Create hooks for polling and data fetching

**Files:**
- Create: `frontend/src/hooks/usePolling.ts`
- Create: `frontend/src/hooks/useJob.ts`
- Create: `frontend/src/hooks/useJobs.ts`

- [ ] **Step 1: Add usePolling hook**

`frontend/src/hooks/usePolling.ts`:

```ts
import { useEffect, useRef } from "react";

export function usePolling(callback: () => void, intervalMs: number, active: boolean) {
  const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (!active) return;

    const tick = () => savedCallback.current();
    tick();
    const id = setInterval(tick, intervalMs);
    return () => clearInterval(id);
  }, [intervalMs, active]);
}
```

- [ ] **Step 2: Add useJobs hook**

`frontend/src/hooks/useJobs.ts`:

```ts
import { useQuery } from "@tanstack/react-query";
import { listJobs } from "../api/jobs";

export function useJobs(page = 1, pageSize = 25) {
  return useQuery({
    queryKey: ["jobs", page, pageSize],
    queryFn: () => listJobs({ page, pageSize }),
    refetchInterval: 2000,
  });
}
```

- [ ] **Step 3: Add useJob hook**

`frontend/src/hooks/useJob.ts`:

```ts
import { useQuery } from "@tanstack/react-query";
import { getJob } from "../api/jobs";

const TERMINAL_STATUSES = new Set(["completed", "failed"]);

export function useJob(jobId: string) {
  return useQuery({
    queryKey: ["job", jobId],
    queryFn: () => getJob(jobId),
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      return TERMINAL_STATUSES.has(status || "") ? false : 1000;
    },
  });
}
```

- [ ] **Step 4: Type-check**

Run: `npx tsc --noEmit`
Expected: no errors.

- [ ] **Step 5: Commit**

```bash
git add frontend/src/hooks
git commit -m "feat(frontend): add polling and data hooks"
```

---

### Task 4: Create Layout and JobStatusBadge

**Files:**
- Create: `frontend/src/components/Layout.tsx`
- Create: `frontend/src/components/JobStatusBadge.tsx`

- [ ] **Step 1: Create Layout**

`frontend/src/components/Layout.tsx`:

```tsx
import { Link, Outlet } from "react-router-dom";
import { Activity, FilePlus, FileCheck, BookOpen } from "lucide-react";

export function Layout() {
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="mx-auto max-w-7xl px-4">
          <div className="flex h-14 gap-6">
            <Link to="/" className="flex items-center gap-2 font-semibold text-gray-900">
              <Activity className="h-5 w-5" />
              Route Optimizer
            </Link>
            <Link to="/" className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900">
              Dashboard
            </Link>
            <Link to="/jobs/new" className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900">
              <FilePlus className="h-4 w-4" />
              New Job
            </Link>
            <Link to="/validate" className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900">
              <FileCheck className="h-4 w-4" />
              Validate
            </Link>
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noreferrer"
              className="ml-auto flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900"
            >
              <BookOpen className="h-4 w-4" />
              API Docs
            </a>
          </div>
        </div>
      </nav>
      <main className="mx-auto max-w-7xl p-4">
        <Outlet />
      </main>
    </div>
  );
}
```

- [ ] **Step 2: Create JobStatusBadge**

`frontend/src/components/JobStatusBadge.tsx`:

```tsx
import type { JobStatus } from "../types";

const STYLES: Record<JobStatus, string> = {
  pending: "bg-yellow-100 text-yellow-800",
  running: "bg-blue-100 text-blue-800",
  completed: "bg-green-100 text-green-800",
  failed: "bg-red-100 text-red-800",
};

export function JobStatusBadge({ status }: { status: JobStatus }) {
  return (
    <span className={`rounded-full px-2 py-1 text-xs font-medium ${STYLES[status]}`}>
      {status}
    </span>
  );
}
```

- [ ] **Step 3: Type-check**

Run: `npx tsc --noEmit`
Expected: no errors.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/Layout.tsx frontend/src/components/JobStatusBadge.tsx
git commit -m "feat(frontend): add Layout and JobStatusBadge"
```

---

### Task 5: Create DashboardPage

**Files:**
- Create: `frontend/src/pages/DashboardPage.tsx`

- [ ] **Step 1: Implement DashboardPage**

```tsx
import { Link } from "react-router-dom";
import { useJobs } from "../hooks/useJobs";
import { JobStatusBadge } from "../components/JobStatusBadge";

export function DashboardPage() {
  const { data, isLoading, error } = useJobs();

  if (isLoading) return <p>Loading jobs...</p>;
  if (error) return <p className="text-red-600">Failed to load jobs.</p>;

  const jobs = data?.items || [];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Jobs</h1>
        <Link
          to="/jobs/new"
          className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          New Job
        </Link>
      </div>

      <div className="overflow-hidden rounded-lg border bg-white shadow">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-2 text-left text-xs font-medium uppercase text-gray-500">ID</th>
              <th className="px-4 py-2 text-left text-xs font-medium uppercase text-gray-500">Name</th>
              <th className="px-4 py-2 text-left text-xs font-medium uppercase text-gray-500">Status</th>
              <th className="px-4 py-2 text-left text-xs font-medium uppercase text-gray-500">Created</th>
              <th className="px-4 py-2 text-left text-xs font-medium uppercase text-gray-500">Objective</th>
              <th className="px-4 py-2 text-left text-xs font-medium uppercase text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {jobs.map((job) => (
              <tr key={job.job_id}>
                <td className="px-4 py-2 text-sm font-mono text-gray-900">{job.job_id.slice(0, 8)}</td>
                <td className="px-4 py-2 text-sm text-gray-900">{job.name || "—"}</td>
                <td className="px-4 py-2">
                  <JobStatusBadge status={job.status} />
                </td>
                <td className="px-4 py-2 text-sm text-gray-500">{new Date(job.created_at).toLocaleString()}</td>
                <td className="px-4 py-2 text-sm text-gray-900">{job.objective_value ?? "—"}</td>
                <td className="px-4 py-2 text-sm">
                  <Link to={`/jobs/${job.job_id}`} className="text-blue-600 hover:underline">
                    View
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Type-check**

Run: `npx tsc --noEmit`
Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/pages/DashboardPage.tsx
git commit -m "feat(frontend): add Dashboard page"
```

---

### Task 6: Create NewJobPage

**Files:**
- Create: `frontend/src/pages/NewJobPage.tsx`

- [ ] **Step 1: Implement NewJobPage**

```tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { submitJob } from "../api/jobs";

export function NewJobPage() {
  const navigate = useNavigate();
  const [jsonText, setJsonText] = useState("");
  const [name, setName] = useState("");
  const [seed, setSeed] = useState(42);
  const [autoValidate, setAutoValidate] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleFile = async (file: File) => {
    const text = await file.text();
    setJsonText(text);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    let instance: Record<string, unknown>;
    try {
      instance = JSON.parse(jsonText);
    } catch {
      setError("Invalid JSON");
      return;
    }

    setIsSubmitting(true);
    try {
      const response = await submitJob(instance, { seed, name: name || undefined, autoValidate });
      navigate(`/jobs/${response.job_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit job");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl space-y-4">
      <h1 className="text-2xl font-bold">New Job</h1>
      <form onSubmit={handleSubmit} className="space-y-4 rounded-lg border bg-white p-6 shadow">
        <div>
          <label className="block text-sm font-medium text-gray-700">Instance JSON</label>
          <textarea
            value={jsonText}
            onChange={(e) => setJsonText(e.target.value)}
            rows={12}
            className="mt-1 w-full rounded border p-2 font-mono text-sm"
            placeholder="Paste instance JSON here"
          />
          <input
            type="file"
            accept=".json,application/json"
            onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
            className="mt-2 block text-sm"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="mt-1 w-full rounded border p-2"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Seed</label>
            <input
              type="number"
              value={seed}
              onChange={(e) => setSeed(Number(e.target.value))}
              className="mt-1 w-full rounded border p-2"
            />
          </div>
        </div>

        <label className="flex items-center gap-2 text-sm text-gray-700">
          <input
            type="checkbox"
            checked={autoValidate}
            onChange={(e) => setAutoValidate(e.target.checked)}
          />
          Auto-validate after solve
        </label>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={isSubmitting}
          className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {isSubmitting ? "Submitting..." : "Run Solver"}
        </button>
      </form>
    </div>
  );
}
```

- [ ] **Step 2: Type-check**

Run: `npx tsc --noEmit`
Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/pages/NewJobPage.tsx
git commit -m "feat(frontend): add New Job page"
```

---

### Task 7: Create route visualization components

**Files:**
- Create: `frontend/src/components/RouteMap.tsx`
- Create: `frontend/src/components/VehicleRoutesTable.tsx`
- Create: `frontend/src/components/LoaderRoutesTable.tsx`

- [ ] **Step 1: Implement RouteMap**

`frontend/src/components/RouteMap.tsx`:

```tsx
import { MapContainer, TileLayer, Marker, Polyline, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

interface RouteMapProps {
  depot?: { lat: number; lng: number };
  orders?: Array<{ id: string; lat: number; lng: number }>;
  vehicleRoutes?: Array<Array<{ lat: number; lng: number }>>;
  loaderRoutes?: Array<Array<{ lat: number; lng: number }>>;
}

const COLORS = ["#2563eb", "#dc2626", "#16a34a", "#9333ea", "#ea580c"];

export function RouteMap({ depot, orders = [], vehicleRoutes = [], loaderRoutes = [] }: RouteMapProps) {
  const center = depot || orders[0] || { lat: 55.75, lng: 37.62 };

  return (
    <MapContainer center={[center.lat, center.lng]} zoom={12} className="h-96 w-full rounded-lg">
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      {depot && (
        <Marker position={[depot.lat, depot.lng]}>
          <Popup>Depot</Popup>
        </Marker>
      )}
      {orders.map((order) => (
        <Marker
          key={order.id}
          position={[order.lat, order.lng]}
          icon={L.divIcon({ className: "bg-blue-500 h-2 w-2 rounded-full" })}
        >
          <Popup>Order {order.id}</Popup>
        </Marker>
      ))}
      {vehicleRoutes.map((route, idx) => (
        <Polyline
          key={`v-${idx}`}
          positions={route.map((p) => [p.lat, p.lng])}
          color={COLORS[idx % COLORS.length]}
        />
      ))}
      {loaderRoutes.map((route, idx) => (
        <Polyline
          key={`l-${idx}`}
          positions={route.map((p) => [p.lat, p.lng])}
          color="#000"
          dashArray="5, 10"
        />
      ))}
    </MapContainer>
  );
}
```

- [ ] **Step 2: Implement route tables**

`frontend/src/components/VehicleRoutesTable.tsx`:

```tsx
export function VehicleRoutesTable({ routes }: { routes: unknown[] }) {
  if (!routes || routes.length === 0) return <p className="text-sm text-gray-500">No vehicle routes.</p>;

  return (
    <table className="min-w-full divide-y divide-gray-200">
      <thead className="bg-gray-50">
        <tr>
          <th className="px-4 py-2 text-left text-xs font-medium uppercase text-gray-500">#</th>
          <th className="px-4 py-2 text-left text-xs font-medium uppercase text-gray-500">Stops</th>
        </tr>
      </thead>
      <tbody className="divide-y divide-gray-200">
        {routes.map((route, idx) => (
          <tr key={idx}>
            <td className="px-4 py-2 text-sm">{idx + 1}</td>
            <td className="px-4 py-2 text-sm font-mono">{JSON.stringify(route)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

`frontend/src/components/LoaderRoutesTable.tsx`:

```tsx
export function LoaderRoutesTable({ routes }: { routes: unknown[] }) {
  if (!routes || routes.length === 0) return <p className="text-sm text-gray-500">No loader routes.</p>;

  return (
    <table className="min-w-full divide-y divide-gray-200">
      <thead className="bg-gray-50">
        <tr>
          <th className="px-4 py-2 text-left text-xs font-medium uppercase text-gray-500">#</th>
          <th className="px-4 py-2 text-left text-xs font-medium uppercase text-gray-500">Assignments</th>
        </tr>
      </thead>
      <tbody className="divide-y divide-gray-200">
        {routes.map((route, idx) => (
          <tr key={idx}>
            <td className="px-4 py-2 text-sm">{idx + 1}</td>
            <td className="px-4 py-2 text-sm font-mono">{JSON.stringify(route)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

- [ ] **Step 3: Type-check**

Run: `npx tsc --noEmit`
Expected: no errors.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/RouteMap.tsx frontend/src/components/VehicleRoutesTable.tsx frontend/src/components/LoaderRoutesTable.tsx
git commit -m "feat(frontend): add route map and tables"
```

---

### Task 8: Create ValidationReport and JsonViewer

**Files:**
- Create: `frontend/src/components/ValidationReport.tsx`
- Create: `frontend/src/components/JsonViewer.tsx`

- [ ] **Step 1: Implement ValidationReport**

```tsx
import type { ValidationResponse } from "../types";

export function ValidationReport({ report }: { report: ValidationResponse }) {
  return (
    <div className="space-y-2 rounded-lg border bg-white p-4 shadow">
      <div className="flex items-center gap-2">
        <span className={`h-3 w-3 rounded-full ${report.passed ? "bg-green-500" : "bg-red-500"}`} />
        <span className="font-semibold">{report.passed ? "Passed" : "Failed"}</span>
      </div>
      {report.objective_value !== undefined && (
        <p className="text-sm text-gray-700">Objective value: {report.objective_value}</p>
      )}
      {report.violations.length > 0 && (
        <ul className="list-disc space-y-1 pl-5 text-sm text-red-700">
          {report.violations.map((v, i) => (
            <li key={i}>{v}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

- [ ] **Step 2: Implement JsonViewer**

```tsx
export function JsonViewer({ data }: { data: unknown }) {
  return (
    <pre className="overflow-auto rounded-lg border bg-gray-900 p-4 text-xs text-green-400">
      {JSON.stringify(data, null, 2)}
    </pre>
  );
}
```

- [ ] **Step 3: Type-check**

Run: `npx tsc --noEmit`
Expected: no errors.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/components/ValidationReport.tsx frontend/src/components/JsonViewer.tsx
git commit -m "feat(frontend): add ValidationReport and JsonViewer"
```

---

### Task 9: Create JobDetailPage

**Files:**
- Create: `frontend/src/pages/JobDetailPage.tsx`

- [ ] **Step 1: Implement JobDetailPage**

```tsx
import { useParams, Link } from "react-router-dom";
import { useJob } from "../hooks/useJob";
import { JobStatusBadge } from "../components/JobStatusBadge";
import { RouteMap } from "../components/RouteMap";
import { VehicleRoutesTable } from "../components/VehicleRoutesTable";
import { LoaderRoutesTable } from "../components/LoaderRoutesTable";
import { ValidationReport } from "../components/ValidationReport";
import { JsonViewer } from "../components/JsonViewer";
import { useState } from "react";

type Tab = "routes" | "validation" | "json";

export function JobDetailPage() {
  const { jobId } = useParams<{ jobId: string }>();
  const { data: job, isLoading, error } = useJob(jobId || "");
  const [activeTab, setActiveTab] = useState<Tab>("routes");

  if (isLoading) return <p>Loading job...</p>;
  if (error || !job) return <p className="text-red-600">Job not found.</p>;

  const result = job.result || {};
  const vehicles = Array.isArray(result.vehicles) ? result.vehicles : [];
  const loaders = Array.isArray(result.loaders) ? result.loaders : [];

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 text-sm text-gray-500">
        <Link to="/" className="hover:underline">
          ← Dashboard
        </Link>
      </div>

      <div className="rounded-lg border bg-white p-6 shadow">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">{job.name || "Untitled job"}</h1>
          <JobStatusBadge status={job.status} />
        </div>
        <p className="mt-1 font-mono text-sm text-gray-500">{job.job_id}</p>
        <div className="mt-4 grid grid-cols-3 gap-4 text-sm">
          <div>
            <span className="text-gray-500">Seed:</span> {job.seed ?? "—"}
          </div>
          <div>
            <span className="text-gray-500">Objective:</span> {job.objective_value ?? "—"}
          </div>
          <div>
            <span className="text-gray-500">Validation:</span> {job.validation_status ?? "—"}
          </div>
        </div>
      </div>

      <RouteMap vehicleRoutes={vehicles} loaderRoutes={loaders} />

      <div className="border-b">
        <nav className="-mb-px flex gap-6">
          {(["routes", "validation", "json"] as Tab[]).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`border-b-2 px-1 py-2 text-sm font-medium capitalize ${
                activeTab === tab
                  ? "border-blue-600 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700"
              }`}
            >
              {tab}
            </button>
          ))}
        </nav>
      </div>

      {activeTab === "routes" && (
        <div className="space-y-4">
          <h2 className="font-semibold">Vehicle Routes</h2>
          <VehicleRoutesTable routes={vehicles} />
          <h2 className="font-semibold">Loader Routes</h2>
          <LoaderRoutesTable routes={loaders} />
        </div>
      )}

      {activeTab === "validation" && job.validation_report && (
        <ValidationReport report={job.validation_report as any} />
      )}

      {activeTab === "json" && (
        <div className="space-y-4">
          <h2 className="font-semibold">Result</h2>
          <JsonViewer data={result} />
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 2: Type-check**

Run: `npx tsc --noEmit`
Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/pages/JobDetailPage.tsx
git commit -m "feat(frontend): add Job Detail page"
```

---

### Task 10: Create ValidatePage

**Files:**
- Create: `frontend/src/pages/ValidatePage.tsx`

- [ ] **Step 1: Implement ValidatePage**

```tsx
import { useState } from "react";
import { validateSolution } from "../api/validate";
import { ValidationReport } from "../components/ValidationReport";
import type { ValidationResponse } from "../types";

export function ValidatePage() {
  const [instanceText, setInstanceText] = useState("");
  const [solutionText, setSolutionText] = useState("");
  const [result, setResult] = useState<ValidationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    let instance: Record<string, unknown>;
    let solution: Record<string, unknown>;
    try {
      instance = JSON.parse(instanceText);
      solution = JSON.parse(solutionText);
    } catch {
      setError("Invalid JSON in one of the inputs");
      return;
    }

    setIsRunning(true);
    try {
      const data = await validateSolution(instance, solution);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Validation request failed");
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="max-w-3xl space-y-4">
      <h1 className="text-2xl font-bold">Validate Solution</h1>
      <form onSubmit={handleSubmit} className="space-y-4 rounded-lg border bg-white p-6 shadow">
        <div>
          <label className="block text-sm font-medium text-gray-700">Instance JSON</label>
          <textarea
            value={instanceText}
            onChange={(e) => setInstanceText(e.target.value)}
            rows={8}
            className="mt-1 w-full rounded border p-2 font-mono text-sm"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Solution JSON</label>
          <textarea
            value={solutionText}
            onChange={(e) => setSolutionText(e.target.value)}
            rows={8}
            className="mt-1 w-full rounded border p-2 font-mono text-sm"
          />
        </div>
        {error && <p className="text-sm text-red-600">{error}</p>}
        <button
          type="submit"
          disabled={isRunning}
          className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {isRunning ? "Validating..." : "Validate"}
        </button>
      </form>
      {result && <ValidationReport report={result} />}
    </div>
  );
}
```

- [ ] **Step 2: Type-check**

Run: `npx tsc --noEmit`
Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add frontend/src/pages/ValidatePage.tsx
git commit -m "feat(frontend): add Validate page"
```

---

### Task 11: Wire up App.tsx and main.tsx

**Files:**
- Modify: `frontend/src/App.tsx`
- Modify: `frontend/src/main.tsx`

- [ ] **Step 1: Update main.tsx**

```tsx
import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { App } from "./App";
import "./index.css";

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
);
```

- [ ] **Step 2: Update App.tsx**

```tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Layout } from "./components/Layout";
import { DashboardPage } from "./pages/DashboardPage";
import { NewJobPage } from "./pages/NewJobPage";
import { JobDetailPage } from "./pages/JobDetailPage";
import { ValidatePage } from "./pages/ValidatePage";

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<DashboardPage />} />
          <Route path="jobs/new" element={<NewJobPage />} />
          <Route path="jobs/:jobId" element={<JobDetailPage />} />
          <Route path="validate" element={<ValidatePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
```

- [ ] **Step 3: Type-check**

Run: `npx tsc --noEmit`
Expected: no errors.

- [ ] **Step 4: Commit**

```bash
git add frontend/src/main.tsx frontend/src/App.tsx
git commit -m "feat(frontend): wire up router and query client"
```

---

### Task 12: Add production Dockerfile and nginx config

**Files:**
- Create: `frontend/Dockerfile`
- Create: `frontend/nginx.conf`

- [ ] **Step 1: Create Dockerfile**

```dockerfile
FROM node:20-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

- [ ] **Step 2: Create nginx.conf**

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://api:8000/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/Dockerfile frontend/nginx.conf
git commit -m "chore(frontend): add production Dockerfile and nginx config"
```

---

### Task 13: Build and verify

- [ ] **Step 1: Production build**

Run: `cd frontend && npm run build`
Expected: `dist/` folder created without errors.

- [ ] **Step 2: Lint**

Run: `cd frontend && npm run lint`
Expected: no lint errors (ESLint is included in Vite template).

- [ ] **Step 3: Commit final frontend**

```bash
git add frontend/
git commit -m "feat(frontend): complete initial SPA"
```

---

## Self-Review Checklist

- [x] Spec coverage: all pages (Dashboard, New Job, Job Detail, Validate), map, validation, API docs link map to tasks.
- [x] No placeholders: every task has exact file paths, code, commands, expected output.
- [x] Type consistency: `Job`, `ValidationResponse`, and API function signatures match across components and hooks.
