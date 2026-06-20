# Figma Prototype Guide — Route Optimization Platform

This document contains screen descriptions and ready-to-use prompts for Figma Make / Figma AI to generate an interactive prototype for Assignment 2.

## Prototype goal

Create a public, view-only interactive Figma prototype that demonstrates the key user flows of the Route Optimization web interface:

1. Browse recent optimization jobs on the Dashboard.
2. Submit a new job on the New Job page.
3. View job details, route map, and validation results on the Job Detail page.
4. Validate an arbitrary solution on the Validate page.

The prototype does not need production behavior — clickable navigation between screens and representative states are enough.

---

## Design system

Use a clean, professional logistics/dashboard aesthetic.

- **Primary color:** `#2563EB` (blue).
- **Success color:** `#16A34A` (green).
- **Warning color:** `#CA8A04` (yellow/amber).
- **Danger color:** `#DC2626` (red).
- **Background:** `#F9FAFB` (light gray).
- **Surface:** `#FFFFFF` (white cards).
- **Text primary:** `#111827`.
- **Text secondary:** `#6B7280`.
- **Font:** Inter, system-ui, sans-serif.
- **Spacing:** 16 px base grid, rounded corners `8 px` for cards and buttons.

---

## Navigation shell

A top navigation bar appears on every screen.

**Elements:**

- Left: logo icon + "Route Optimizer" title.
- Links: Dashboard, New Job, Validate.
- Right: "API Docs" link (external).

Height: 56 px, white background, subtle bottom shadow.

---

## Screen 1: Dashboard

### Purpose
Show the list of recent optimization jobs with status, timestamps, and quick actions.

### Layout

- Page title "Jobs" on the left, blue "New Job" button on the right.
- White card containing a data table:
  - Columns: ID, Name, Status, Created, Objective, Actions.
- Status badges:
  - Pending = amber pill.
  - Running = blue pill.
  - Completed = green pill.
  - Failed = red pill.
- Each row has a "View" text link that navigates to Job Detail.

### States

1. **Populated table** — 4–5 example rows:
   - completed job with objective value;
   - running job;
   - pending job;
   - failed job.
2. **Empty state** — placeholder text "No jobs yet. Create your first optimization job."

### Figma Make prompt

```text
Create a clean logistics dashboard web page titled "Jobs" in a desktop viewport (1440x900). 
Top navigation bar with logo "Route Optimizer" and links: Dashboard, New Job, Validate, API Docs.
Below the nav, a heading "Jobs" on the left and a blue "New Job" button on the right.
A white card containing a data table with columns: ID, Name, Status, Created, Objective, Actions.
Show 5 rows with example data:
- ID 7f3a..., Name "Test t1", Status "completed" green badge, Created "13 Jun 2026, 10:23", Objective "4 820", Action "View".
- ID 9c21..., Name "Test t2", Status "running" blue badge, Created "13 Jun 2026, 10:24", Objective "—", Action "View".
- ID a11b..., Name "", Status "pending" amber badge, Created "13 Jun 2026, 10:25", Objective "—", Action "View".
- ID d44e..., Name "Large instance", Status "failed" red badge, Created "13 Jun 2026, 10:26", Objective "—", Action "View".
- ID 55ff..., Name "Baseline run", Status "completed" green badge, Created "13 Jun 2026, 10:27", Objective "5 130", Action "View".
Use Inter font, light gray background, blue primary color, rounded cards, status pills.
```

---

## Screen 2: New Job

### Purpose
Allow the user to upload/paste a JSON instance, set seed and job name, and start the solver.

### Layout

- Page title "New Job".
- White card with a form:
  - Large textarea labeled "Instance JSON" with example JSON placeholder.
  - File upload input below the textarea.
  - Two-column row:
    - Input "Name" (optional).
    - Input "Seed" (number, default 42).
  - Checkbox "Auto-validate after solve".
  - Blue "Run Solver" button.
  - Inline error message area (hidden by default).

### States

1. **Initial** — empty form, button enabled.
2. **Filled** — textarea contains JSON, name and seed set.
3. **Submitting** — button shows spinner or "Submitting...".
4. **Error** — red text "Invalid JSON" below textarea.

### Navigation

- Clicking "Run Solver" navigates to Job Detail (loading state).

### Figma Make prompt

```text
Create a web form page titled "New Job" in a desktop viewport (1440x900).
Top navigation bar with logo "Route Optimizer" and links: Dashboard, New Job, Validate, API Docs.
Page heading "New Job".
A centered white card (max-width 800 px) containing a form:
- Label "Instance JSON" with a large monospace textarea (12 rows) showing a placeholder JSON snippet of a CVRPTW instance: depot, orders, weights.
- A file input "Upload JSON file" below the textarea.
- A two-column row with inputs "Name" and "Seed" (value 42).
- A checkbox labeled "Auto-validate after solve" (checked).
- A blue primary button "Run Solver".
- A small red error text area below the button (empty).
Light gray background, Inter font, rounded corners, professional logistics tool style.
```

---

## Screen 3: Job Detail

### Purpose
Display the status, summary, route map, route tables, validation report, and raw JSON for a single job.

### Layout

- Breadcrumb "← Dashboard".
- White header card:
  - Job name and status badge.
  - Job ID (monospace, small).
  - Summary grid: Seed, Objective, Validation.
- Interactive map placeholder — rectangle labeled "Route Map" with a note "Depot, orders, vehicle routes, loader routes".
- Tab bar: Routes | Validation | Raw JSON.
- **Routes tab:**
  - "Vehicle Routes" table with example route rows.
  - "Loader Routes" table with example rows.
- **Validation tab:**
  - Pass/fail indicator, objective value, violations list.
- **Raw JSON tab:**
  - Monospace JSON preview area.

### States

1. **Loading** — status badge "running", spinner on map, tables show skeleton or "Loading...".
2. **Completed** — green badge, map with route polylines, tables filled.
3. **Failed** — red badge, error message card.

### Navigation

- "← Dashboard" returns to Dashboard.
- Tabs switch content inside the same screen (no separate URL needed for prototype).
- Optional "Download result JSON" and "Re-run" buttons.

### Figma Make prompt

```text
Create a job detail page titled "Job Detail" in a desktop viewport (1440x900).
Top navigation bar with logo "Route Optimizer" and links: Dashboard, New Job, Validate, API Docs.
A breadcrumb link "← Dashboard" at the top left.
A white summary card containing:
- Heading "Baseline run" with a green "completed" status pill.
- Monospace job ID "7f3a..." below the heading.
- Three summary items in a row: "Seed: 42", "Objective: 4 820", "Validation: passed".
Below the card, a large rectangle placeholder for an interactive map labeled "Route Map" with small markers for depot and orders and colored route lines.
Below the map, a tab bar: "Routes", "Validation", "Raw JSON" with "Routes" active.
Under the active tab, show:
- Section "Vehicle Routes" with a small table: columns Vehicle, Route, Start times.
- Section "Loader Routes" with a small table: columns Loader, Route.
Light gray background, Inter font, rounded cards, blue primary color.
```

---

## Screen 4: Validate

### Purpose
Allow the user to validate an arbitrary instance-solution pair.

### Layout

- Page title "Validate Solution".
- White card with two textareas side by side:
  - Left: "Instance JSON".
  - Right: "Solution JSON".
- Blue "Validate" button below.
- Validation result card below the button:
  - Green checkmark + "Passed" or red cross + "Failed".
  - Objective value.
  - Violations list (if any).

### States

1. **Initial** — empty textareas, button enabled.
2. **Filled** — both JSON inputs populated.
3. **Result passed** — green card, no violations.
4. **Result failed** — red card with violation list.

### Figma Make prompt

```text
Create a validation page titled "Validate Solution" in a desktop viewport (1440x900).
Top navigation bar with logo "Route Optimizer" and links: Dashboard, New Job, Validate, API Docs.
Page heading "Validate Solution".
A white card containing:
- A two-column row of large monospace textareas:
  - Left textarea labeled "Instance JSON" (8 rows).
  - Right textarea labeled "Solution JSON" (8 rows).
- A blue "Validate" button centered below the textareas.
Below the button, a green result card with a checkmark icon, text "Passed", and "Objective value: 4 820".
Light gray background, Inter font, rounded cards, blue primary color.
```

---

## Prototype flow and interactions

After generating the screens in Figma, switch to **Prototype** mode and add the following interactions:

1. **Dashboard → New Job**
   - Trigger: click "New Job" button (top right or nav).
   - Action: Navigate to New Job screen.

2. **Dashboard → Job Detail**
   - Trigger: click any "View" link in a table row.
   - Action: Navigate to Job Detail screen.

3. **New Job → Job Detail**
   - Trigger: click "Run Solver" button.
   - Action: Navigate to Job Detail screen (use completed state for demo).

4. **Job Detail → Dashboard**
   - Trigger: click "← Dashboard".
   - Action: Navigate to Dashboard.

5. **Navigation links**
   - "Dashboard", "New Job", "Validate" in the top nav link to the corresponding screens.

6. **Job Detail tabs (optional)**
   - Click "Routes" / "Validation" / "Raw JSON" to switch between three duplicate frames showing the respective tab content.

---

## Sharing the prototype

1. In Figma, click **Share** in the top-right corner.
2. Set permission to **Anyone with the link → can view**.
3. Copy the link.
4. Add the link to:
   - `reports/week2/README.md` in the "Selected Interface and Prototype" section.
   - Moodle PDF in the live prototype field.

---

## Tips for best results

- Generate each screen as a separate Figma frame in the same file.
- After AI generation, manually adjust spacing, alignment, and colors to match the design system.
- Use Figma's native **Status badge** components (or simple colored pills) for consistency.
- Keep the map area as a styled placeholder in the prototype; a real map is not required.
- Add at least one empty-state and one error-state frame to show important states.
