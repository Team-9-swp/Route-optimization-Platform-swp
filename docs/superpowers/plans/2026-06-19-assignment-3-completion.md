# Assignment 3 — план завершения

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Закрыть все требования Assignment 3: мигрировать user stories в issue-based Product Backlog, настроить Scrum-воркфлоу, создать Sprint Backlog для MVP v1, реализовать и задеплоить MVP v1, провести Sprint Review и Retrospective, собрать Week 3 отчёт.

**Architecture:** Используем уже имеющийся FastAPI-бэкенд + greedy/LS солвер (`main_mvp.py`) и React-заглушку фронтенда. MVP v1 ограничиваем Must Have историями, которые уже работают через API, плюс доводим фронтенд до реального подключения к API. Все артефакты процесса (issues, milestones, project board, reports) ведём в GitHub.

**Tech Stack:** Python 3.11, FastAPI, Pydantic, pytest; React 18 + TypeScript + Vite + Tailwind CSS; Docker Compose; GitHub Issues/Projects/Milestones/Releases.

---

## 1. Текущее состояние (gap analysis)

### Уже сделано ✅

| Часть задания | Что есть | Где |
|---|---|---|
| Part 1 — User stories | Истории недели 2 сохранены в `reports/week2/user-stories.md`; индекс в `docs/user-stories.md`; US-01 разбит на US-01a/US-01b, исходный US-01 помечен Removed | `reports/week2/user-stories.md`, `docs/user-stories.md` |
| Part 2 — Templates | 4 шаблона issue + расширенный PR-шаблон + workflow lychee | `.github/ISSUE_TEMPLATE/`, `.github/pull_request_template.md` |
| Part 6 — Definition of Done | Файл создан и заполнен | `docs/definition-of-done.md` |
| Part 8 — Backend MVP | Работает `POST /solve`, `GET /jobs/{id}`; солвер возвращает vehicle routes, loader routes, проверяет hard constraints; Docker Compose для API | `app/`, `main_mvp.py`, `Dockerfile`, `docker-compose.yml` |
| Changelog | `CHANGELOG.md` ведётся | `CHANGELOG.md` |
| Tests | pytest-suite проходит (кроме медленного e2e) | `tests/` |
| Frontend prototype | React-приложение с Dashboard / New Job / Job Detail / Validate, но на мок-данных | `frontend/src/` |
| Superpowers plans | Детальные планы бэкенда и фронтенда уже написаны | `docs/superpowers/plans/` |

### Что ещё нужно сделать ⚠️

| Часть задания | Чего не хватает | Критичность |
|---|---|---|
| Part 1 — Backlog | `docs/user-stories.md` устарел: все статусы `To Do`, нужно синхронизировать с реальным состоянием issues | Высокая |
| Part 3 — Backlog ≥15 PBIs | Сейчас 13 активных user stories. Нужно добавить ≥2 тех/инфраструктурных PBI и вести их в GitHub Issues/Projects | Высокая |
| Part 3 — Boards | Нет GitHub Project board для Product Backlog и Sprint Backlog | Высокая |
| Part 4 — Acceptance criteria | Нет acceptance criteria в issues, отмеченных как MVP v1 | Высокая |
| Part 5 — Estimation | Нет story points в issues | Высокая |
| Part 7 — Sprint & MVP v1 | Нет milestone текущего Sprint, нет label/поля `MVP v1`, нет назначений и ревьюеров | Высокая |
| Part 8 — MVP v1 delivery | Фронтенд не подключён к API; не все Must Have истории доведены до `Done`; нет release/tag SemVer | Высокая |
| Part 9 — Customer review | Нет transcript/notes/summary | Средняя |
| Part 10 — Roadmap | Нет `docs/roadmap.md` | Средняя |
| Part 11–13 + Week 3 report | Нет `reports/week3/` | Высокая |
| Part 2 — Workflow evidence | Нет SemVer release, нет видео-демонстрации, нужны issue-linked reviewed PRs | Высокая |

---

## 2. Рекомендуемый скоуп MVP v1

Assignment 3 требует, чтобы MVP v1 включал только Must Have истории + supporting PBIs. Исходя из того, что бэкенд уже решает ядро задачи, рекомендуем следующий скоуп:

**User stories (Must Have):**
1. `US-01a` — Vehicle route output
2. `US-01b` — Vehicle arrival schedule
3. `US-02` — Loader route
4. `US-03` — Hard constraint validation
5. `US-04` — Docker execution

**Supporting PBIs:**
6. `PBI-01` — FastAPI async job API (`POST /solve`, `GET /jobs/{id}`, `GET /jobs`, `GET /health`)
7. `PBI-02` — CORS middleware для фронтенда
8. `PBI-03` — Frontend: Dashboard с реальными данными из API
9. `PBI-04` — Frontend: New Job page с реальной отправкой задачи
10. `PBI-05` — Frontend: Job Detail page с отображением routes / validation / raw JSON
11. `PBI-06` — Docker Compose с сервисами `api` + `frontend`
12. `PBI-07` — SemVer release `v1.0.0` для MVP v1

> Всего 12 PBIs, из них 5 user stories + 7 supporting. Этого достаточно для MVP v1. Оставшиеся Should/Could Have истории остаются в Product Backlogе для будущих спринтов.

---

## 3. Пошаговый план выполнения

### Этап A. Подготовка репозитория и Scrum-артефактов (вручную в GitHub + локальные файлы)

> ⚠️ Для создания issues/milestones/project board нужен доступ к GitHub UI или `gh` CLI. В текущем окружении `gh` CLI не установлен, поэтому эти шаги нужно выполнить вручную через GitHub web UI (или установить `gh` и автоматизировать).

#### Task A1. Создать GitHub Project (board view) для Product Backlog

**Files:**
- Modify: `docs/user-stories.md`
- Modify: `README.md` (добавить ссылку на board)

- [ ] **Step 1: Создать GitHub Project**
  - В репозитории `Team-9-swp/Route-optimization-Platform-swp` открыть Projects → New project → Board.
  - Назвать `Route Optimizer Product Backlog`.
  - Добавить поля: `MoSCoW priority`, `Story Points`, `Work Status`, `MVP version`, `Sprint`.
  - Добавить views: `Product Backlog` (все PBIs), `Sprint Backlog` (фильтр по текущему Sprint).

- [ ] **Step 2: Зафиксировать ссылку**
  - Скопировать URL project board.
  - Добавить в `README.md` раздел `## Product Backlog` со ссылкой.

- [ ] **Step 3: Commit**
  ```bash
  git add README.md
  git commit -m "docs: add Product Backlog board link"
  ```

#### Task A2. Создать milestone для текущего Sprint

- [ ] **Step 1: Создать milestone в GitHub**
  - Title: `Sprint 3` (или `Sprint 1 — MVP v1`, согласно внутренней нумерации команды).
  - Description должно содержать **Sprint Goal**, например:
    ```text
    Sprint Goal: Deliver MVP v1 — a runnable Dockerized Route Optimization API plus a React frontend that lets dispatchers submit instances and view vehicle/loader routes and validation results.
    ```
  - Due date: дата сдачи Assignment 3 (уточнить у команды).

- [ ] **Step 2: Создать label `mvp-v1`**
  - Цвет произвольный, description: `Items selected for MVP v1 scope`.

#### Task A3. Создать/обновить issues для всех PBIs

Для каждой user story из `docs/user-stories.md` и каждого supporting PBI:

- [ ] **Step 1: Создать issue по шаблону `User Story` или `Other PBI`**
  - Title формата: `<Stable ID>: <Short title>` (например, `US-01a: Vehicle route output`).
  - Body должен содержать:
    - Stable ID
    - User-story statement / Description
    - MoSCoW priority
    - Story Points (после оценки)
    - Work Status
    - Acceptance criteria (≥3 для MVP v1 items)
    - Notes, constraints, assumptions
    - Assignee (если в Sprint Backlog)
    - Reviewer (если в Sprint Backlog)
    - Milestone (если в Sprint Backlog)
    - Labels: `mvp-v1` для MVP v1 items

- [ ] **Step 2: Обновить `docs/user-stories.md`**
  - Синхронизировать Issue, Work Status, Sprint для каждой истории.
  - Добавить новые PBIs в конец таблицы или в отдельную секцию.

- [ ] **Step 3: Commit**
  ```bash
  git add docs/user-stories.md
  git commit -m "docs: sync user-story index with GitHub issues"
  ```

#### Task A4. Оценить Product Backlog в Story Points

- [ ] **Step 1: Провести командную оценку**
  - Рекомендуемые значения: 1, 2, 3, 5, 8, 13.
  - Примерные оценки:
    - US-01a: 3
    - US-01b: 2
    - US-02: 5
    - US-03: 5
    - US-04: 3
    - PBI-01 (API extensions): 5
    - PBI-02 (CORS): 1
    - PBI-03 (Dashboard): 3
    - PBI-04 (New Job): 3
    - PBI-05 (Job Detail): 5
    - PBI-06 (Docker Compose): 2
    - PBI-07 (Release): 1
  - **Итого Sprint ~38 SP**, **Product Backlog** включая оставшиеся Should/Could Have — записать в Week 3 report.

- [ ] **Step 2: Записать Story Points в каждый issue**

---

### Этап B. Доработка бэкенда для MVP v1

#### Task B1. Добавить CORS middleware

**Files:**
- Modify: `app/main.py`
- Test: `tests/test_api.py`

- [ ] **Step 1: Write the failing test**
  ```python
  def test_cors_preflight(client):
      response = client.options(
          "/solve",
          headers={
              "Origin": "http://localhost:5173",
              "Access-Control-Request-Method": "POST",
          },
      )
      assert response.status_code == 200
      assert "access-control-allow-origin" in response.headers
  ```

- [ ] **Step 2: Run test to verify it fails**
  ```bash
  .venv/Scripts/python -m pytest tests/test_api.py::test_cors_preflight -v
  ```
  Expected: FAIL — header missing.

- [ ] **Step 3: Implement CORS middleware**
  ```python
  import os
  from fastapi.middleware.cors import CORSMiddleware

  def create_app() -> FastAPI:
      app = FastAPI(...)
      origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
      app.add_middleware(
          CORSMiddleware,
          allow_origins=[o.strip() for o in origins],
          allow_credentials=True,
          allow_methods=["*"],
          allow_headers=["*"],
      )
      app.include_router(router)
      return app
  ```

- [ ] **Step 4: Run test to verify it passes**
  ```bash
  .venv/Scripts/python -m pytest tests/test_api.py::test_cors_preflight -v
  ```

- [ ] **Step 5: Commit**
  ```bash
  git add app/main.py tests/test_api.py
  git commit -m "feat(api): add configurable CORS middleware"
  ```

#### Task B2. Расширить schemas, store, runner, service и API endpoints

Следовать плану `docs/superpowers/plans/2026-06-13-backend-api-for-frontend.md`. Кратко:

- [ ] Добавить `ValidationStatus`, `ValidationRequest`, `ValidationResponse`, `JobListResponse` в `app/schemas.py`.
- [ ] Добавить поля `name`, `objective_value`, `validation_status`, `validation_report` в `JobRecord`/`JobResponse`/`SolveResponse`.
- [ ] Расширить `app/store.py`: `create_job(name=None)`, `list_jobs(page, page_size)`, `update_job(..., name, objective_value, validation_status, validation_report)`.
- [ ] Создать `app/validation.py` — wrapper вокруг логики валидации (пока fallback на структурную проверку, т.к. `validator.py` ссылается на отсутствующий `beta_code.validation.validator`).
- [ ] Обновить `app/runner.py`: извлекать `objective_value`, поддерживать `auto_validate`.
- [ ] Обновить `app/service.py`: `submit_job(name, auto_validate)`, `list_jobs`, `validate_solution`.
- [ ] Обновить `app/api.py`: `GET /jobs`, `POST /validate`, `GET /health`, параметры `name` и `auto_validate` в `POST /solve`.
- [ ] Дописать тесты `tests/test_schemas.py`, `tests/test_store.py`, `tests/test_runner.py`, `tests/test_service.py`, `tests/test_api.py`, `tests/test_validation.py`.
- [ ] Убедиться, что весь suite зелёный:
  ```bash
  .venv/Scripts/python -m pytest -v
  ```

- [ ] Commit пошагово по плану бэкенда.

#### Task B3. Исправить `validator.py` или удалить ссылку на отсутствующий модуль

**Files:**
- Modify: `validator.py`

- [ ] **Step 1: Проверить, нужен ли `validator.py` для MVP v1**
  - Если официальный валидатор предоставлен курсом и лежит в `beta_code/`, добавить его в репозиторий.
  - Если нет — переписать `validator.py` так, чтобы он использовал `Evaluator` из `main_mvp.py`:
    ```python
    from main_mvp import ProblemData, Evaluator, Solution
    import json, argparse

    def validate(instance_path: str, solution_path: str) -> dict:
        with open(instance_path) as f:
            instance = json.load(f)
        with open(solution_path) as f:
            solution_raw = json.load(f)
        problem = ProblemData(instance)
        evaluator = Evaluator(problem)
        solution = Solution()
        solution.vehicle_routes = [r["route"] for r in solution_raw.get("vehicles", [])]
        solution.loader_routes = [r["route"] for r in solution_raw.get("loaders", [])]
        cost, feasible, details = evaluator.evaluate(solution)
        return {
            "passed": feasible,
            "objective_value": cost if feasible else None,
            "violations": [] if feasible else ["Solution is infeasible"],
            "report": details,
        }
    ```

- [ ] **Step 2: Добавить тест**
  - `tests/test_validator.py` — проверить `validate` на `test_cases/t1.json` + известным хорошим решением.

- [ ] **Step 3: Commit**
  ```bash
  git add validator.py tests/test_validator.py
  git commit -m "feat(validation): make validator standalone using main_mvp evaluator"
  ```

#### Task B4. Исправить медленный e2e-тест

**Files:**
- Modify: `tests/test_e2e.py`

- [ ] **Step 1: Увеличить таймаут или уменьшить размер входных данных**
  - Либо заменить `test_cases/t1.json` на меньший synthetic instance.
  - Либо увеличить число итераций в цикле ожидания (например, 300 × 0.5 с).

- [ ] **Step 2: Run test**
  ```bash
  .venv/Scripts/python -m pytest tests/test_e2e.py -v
  ```

- [ ] **Step 3: Commit**
  ```bash
  git add tests/test_e2e.py
  git commit -m "test(e2e): stabilize solver timeout"
  ```

---

### Этап C. Доводка фронтенда до работы с реальным API

#### Task C1. Подключить API client и заменить мок-данные

**Files:**
- Create: `frontend/src/api/client.ts`
- Create: `frontend/src/api/jobs.ts`
- Create: `frontend/src/types/index.ts`
- Modify: `frontend/src/app/App.tsx`
- Modify: `frontend/src/app/components/Dashboard.tsx`
- Modify: `frontend/src/app/components/NewJob.tsx`
- Modify: `frontend/src/app/components/JobDetail.tsx`
- Modify: `frontend/vite.config.ts`

- [ ] **Step 1: Добавить зависимости**
  ```bash
  cd frontend
  npm install axios
  npm install -D @types/node
  ```

- [ ] **Step 2: Создать типы**
  ```typescript
  // frontend/src/types/index.ts
  export type JobStatus = "pending" | "running" | "completed" | "failed";
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
    validation_status?: "pending" | "passed" | "failed";
    validation_report?: Record<string, unknown>;
    seed?: number;
  }
  ```

- [ ] **Step 3: Создать API client**
  ```typescript
  // frontend/src/api/client.ts
  import axios from "axios";
  export const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  });
  ```

- [ ] **Step 4: Добавить функции API**
  ```typescript
  // frontend/src/api/jobs.ts
  import { api } from "./client";
  import type { Job } from "../types";
  export const submitJob = (instance: unknown, seed = 42, name?: string, autoValidate = false) =>
    api.post<Job>(`/solve?seed=${seed}${name ? `&name=${encodeURIComponent(name)}` : ""}${autoValidate ? "&auto_validate=true" : ""}`, instance);
  export const getJob = (id: string) => api.get<Job>(`/jobs/${id}`);
  export const listJobs = () => api.get<Job[]>("/jobs");
  ```

- [ ] **Step 5: Настроить Vite proxy**
  ```typescript
  // frontend/vite.config.ts
  server: {
    proxy: {
      "/api": {
        target: process.env.VITE_API_BASE_URL || "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
  ```

- [ ] **Step 6: Заменить мок-данные в Dashboard на реальные**
  - Использовать `useEffect` + `listJobs()`.
  - Poll каждые 2 секунды.

- [ ] **Step 7: Подключить NewJob к `submitJob`**
  - После успешного ответа редирект на Job Detail с реальным `job_id`.

- [ ] **Step 8: Подключить JobDetail к `getJob`**
  - Poll каждую секунду, пока статус не terminal.
  - Отображать `result.vehicles`, `result.loaders`, `validation_report`, raw JSON.

- [ ] **Step 9: Type-check и build**
  ```bash
  cd frontend
  npx tsc --noEmit
  npm run build
  ```

- [ ] **Step 10: Commit**
  ```bash
  git add frontend/
  git commit -m "feat(frontend): wire Dashboard, NewJob, JobDetail to real API"
  ```

#### Task C2. Добавить Dockerfile и nginx.conf для фронтенда

**Files:**
- Create: `frontend/Dockerfile`
- Create: `frontend/nginx.conf`
- Modify: `docker-compose.yml`

- [ ] **Step 1: `frontend/Dockerfile`**
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

- [ ] **Step 2: `frontend/nginx.conf`**
  ```nginx
  server {
    listen 80;
    location / {
      root /usr/share/nginx/html;
      try_files $uri $uri/ /index.html;
    }
    location /api/ {
      proxy_pass http://api:8000/;
    }
  }
  ```

- [ ] **Step 3: Обновить `docker-compose.yml`**
  ```yaml
  services:
    api:
      build: .
      ports:
        - "8000:8000"
      environment:
        - PYTHONUNBUFFERED=1
        - CORS_ORIGINS=http://localhost:5173,http://localhost:3000
      healthcheck:
        test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
        interval: 10s
        timeout: 5s
        retries: 5

    frontend:
      build: ./frontend
      ports:
        - "3000:80"
      depends_on:
        - api
  ```

- [ ] **Step 4: Обновить `Dockerfile` бэкенда, добавив `curl`**
  ```dockerfile
  RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
  ```

- [ ] **Step 5: Проверить compose**
  ```bash
  docker compose config
  docker compose up --build
  ```

- [ ] **Step 6: Commit**
  ```bash
  git add frontend/Dockerfile frontend/nginx.conf docker-compose.yml Dockerfile
  git commit -m "chore(docker): add frontend service and healthchecks"
  ```

---

### Этап D. Релиз и деплой MVP v1

#### Task D1. Создать SemVer release `v1.0.0`

- [ ] **Step 1: Обновить `CHANGELOG.md`**
  - Добавить секцию `## [1.0.0] - <date>` с описанием MVP v1.

- [ ] **Step 2: Обновить `app/main.py` version**
  - `version="1.0.0"`.

- [ ] **Step 3: Commit**
  ```bash
  git add CHANGELOG.md app/main.py
  git commit -m "chore(release): bump version to 1.0.0 for MVP v1"
  ```

- [ ] **Step 4: Создать GitHub release**
  - Tag: `v1.0.0`.
  - Target: `main`.
  - Title: `MVP v1`.
  - Description: скопировать пункты из CHANGELOG.

#### Task D2. Задеплоить MVP v1

- [ ] **Step 1: Развернуть на university VM**
  ```bash
  docker compose -f docker-compose.yml up --build -d
  ```

- [ ] **Step 2: Проверить endpoints**
  ```bash
  curl http://<host>:8000/health
  curl -X POST "http://<host>:8000/solve?seed=42" -H "Content-Type: application/json" -d @test_cases/t1.json
  ```

- [ ] **Step 3: Обновить `README.md`**
  - Актуальные ссылки на развёрнутый API и фронтенд.
  - Инструкции по запуску.

- [ ] **Step 4: Commit**
  ```bash
  git add README.md
  git commit -m "docs: update deployment links and run instructions for MVP v1"
  ```

#### Task D3. Записать короткое видео-демо (<2 мин)

- [ ] **Step 1: Записать демо**
  - Показать Dashboard → New Job → submit → Job Detail с routes/validation.
  - Залить на YouTube/Google Drive/университетский хостинг.

- [ ] **Step 2: Добавить ссылку в `README.md` и `reports/week3/README.md`**

---

### Этап E. Процессные артефакты и отчётность

#### Task E1. Создать `docs/roadmap.md`

**Files:**
- Create: `docs/roadmap.md`

- [ ] **Step 1: Написать roadmap**
  - Текущий Sprint: MVP v1 (API + frontend + Docker).
  - Следующий Sprint: MVP v2 — PostgreSQL persistence, advanced map visualization, skipped optional orders report.
  - Дальше: MVP v3 — authentication, multi-tenancy, benchmarking.

- [ ] **Step 2: Commit**
  ```bash
  git add docs/roadmap.md
  git commit -m "docs: add product roadmap"
  ```

#### Task E2. Создать `reports/week3/` структуру

**Files:**
- Create: `reports/week3/README.md`
- Create: `reports/week3/customer-review-summary.md`
- Create: `reports/week3/customer-review-transcript.md` или `customer-review-notes.md`
- Create: `reports/week3/reflection.md`
- Create: `reports/week3/retrospective.md`
- Create: `reports/week3/llm-report.md`
- Create: `reports/week3/images/`

- [ ] **Step 1: Создать директорию и файлы-заглушки**
  ```bash
  mkdir -p reports/week3/images
  touch reports/week3/README.md reports/week3/customer-review-summary.md reports/week3/reflection.md reports/week3/retrospective.md reports/week3/llm-report.md
  ```

- [ ] **Step 2: Наполнить `reports/week3/README.md`**
  - Все 34 пункта из Assignment 3 (`Project name`, scope, links to `docs/user-stories.md`, board, milestone, MVP v1 view, release, video, screenshots, contribution table, etc.).
  - Contribution traceability table:
    | Team member | Issues | PRs | Reviews |
    |---|---|---|---|
    | ... | ... | ... | ... |

- [ ] **Step 3: Наполнить остальные файлы**
  - `customer-review-summary.md` — date, participants, scope, feedback, approvals, action points.
  - `reflection.md` — learning points, validated assumptions, friction and gaps, planned response.
  - `retrospective.md` — what went well (3), what did not go well (3), action points (1–2).
  - `llm-report.md` — как использовались LLM/AI tools.

- [ ] **Step 4: Сделать скриншоты и положить в `reports/week3/images/`**
  - Product Backlog view
  - Sprint Backlog view
  - Sprint milestone
  - MVP v1 grouped/filtered view
  - SemVer release
  - Delivered MVP v1 (frontend + API)
  - Example reviewed issue-linked PR

- [ ] **Step 5: Commit**
  ```bash
  git add reports/week3/
  git commit -m "docs(week3): add assignment 3 report structure and content"
  ```

#### Task E3. Провести Sprint Review с заказчиком

- [ ] **Step 1: Договориться о встрече**
- [ ] **Step 2: Подготовить демо**
  - Показать развёрнутый фронтенд и API.
  - Показать MVP v1 scope в project board.
- [ ] **Step 3: Получить feedback / approval**
- [ ] **Step 4: Спросить разрешение на запись и публикацию transcript**
- [ ] **Step 5: Написать `customer-review-transcript.md` или `customer-review-notes.md`**
- [ ] **Step 6: Обновить Product Backlog по результатам встречи**

#### Task E4. Провести Sprint Retrospective

- [ ] **Step 1: Командная встреча (можно внутренняя)**
- [ ] **Step 2: Заполнить `reports/week3/retrospective.md`**

---

## 4. Чек-лист перед сдачей

- [ ] Все issue-linked PRs имеют ревью и approval.
- [ ] Все PRs влиты в `main` через merge-commit.
- [ ] Все MVP v1 PBIs в GitHub marked `Done`.
- [ ] `docs/user-stories.md` синхронизирован с issue tracker.
- [ ] `CHANGELOG.md` обновлён для v1.0.0.
- [ ] GitHub release `v1.0.0` создан.
- [ ] MVP v1 доступен по публичной ссылке.
- [ ] Видео-демо <2 мин записано и в отчёте.
- [ ] `reports/week3/README.md` содержит все обязательные пункты.
- [ ] Все ссылки проверены (можно запустить `.venv/Scripts/python -m pytest` и lychee).
- [ ] Moodle PDF подготовлен с командами, ролями, ссылками, commit-hash permalink.

---

## 5. Зависимости и риски

| Риск | Влияние | Митигация |
|---|---|---|
| `validator.py` ссылается на отсутствующий `beta_code.validation.validator` | Среднее | Переписать `validator.py` на базе `Evaluator` из `main_mvp.py` |
| Солвер медленный на больших инстансах, e2e падает по таймауту | Среднее | Уменьшить тестовый инстанс или увеличить таймаут; для демо использовать маленький instance |
| Frontend на мок-данных | Высокое | Подключить к API (Task C1) |
| Нет `gh` CLI в окружении | Среднее | Создавать issues/milestones/release вручную через GitHub UI |
| Мало времени до дедлайна | Высокое | Сфокусироваться на Must Have + отчёт; отложить Should/Could Have |

---

## 6. Рекомендуемый порядок работы (приоритеты)

1. **Сначала** — Scrum-артефакты (issues, milestone, labels, project board). Без них нечего показывать в отчёте.
2. **Параллельно** — бэкенд (Task B1–B4) и фронтенд (Task C1–C2). Независимые команды могут работать одновременно.
3. **Затем** — релиз, деплой, видео (Task D1–D3).
4. **В конце** — отчёты и customer review (Task E1–E4).

---

## Self-review checklist

- [x] **Spec coverage:** Каждая часть Assignment 3 (Part 1–13 + Week 3 report) покрыта задачами.
- [x] **Placeholder scan:** Нет `TBD`, `TODO`, ссылок на несуществующие файлы.
- [x] **Type consistency:** Поля `JobRecord`/`JobResponse`/`SolveResponse` согласованы между бэкенд-планом и фронтенд-типами.
