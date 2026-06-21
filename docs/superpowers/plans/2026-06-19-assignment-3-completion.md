# План доведения Assignment 3 до сдачи

> **For agentic workers:** REQUIRED SUB-LEVEL: superpowers:subagent-driven-development или inline execution. Действия внизу — чек-лист; большинство шагов по репозиторию можно сделать скриптами, но часть требует действий людей (видео, скриншоты, согласование прав, участие команды).

**Goal:** Закрыть все формальные и содержательные пробелы Assignment 3, синхронизировать GitHub Issues/Project/PR с отчётом и подготовить PDF для Moodle.

**Architecture:** Исправляем цифры в отчётах, приводим состояние issue к документам, добиваемся участия каждого члена команды в PR-workflow, заполняем GitHub Project поля, записываем демо и делаем скриншоты.

**Tech Stack:** GitHub CLI, Python, Markdown, Docker (на машине пользователя), видео/скриншот-инструменты.

---

## Сводка текущих пробелов

### Критичные (блокируют проверку Assignment 3)

| # | Пробел | Где это видно | Что делать |
|---|--------|---------------|------------|
| 1 | Неверные Story Points в отчёте | `docs/user-stories.md`, `reports/week3/README.md`, описание milestone `Sprint 1` | Пересчитать и вписать реальные суммы |
| 2 | GitHub Issues не синхронизированы с `docs/user-stories.md` | `#9`–`#12`, `#20`, `#21` открыты, хотя в индексе `Done` Sprint 1; `#5` не помечен `Removed` | Закрыть/переместить issue, обновить статусы |
| 3 | Не все PBI на доске и не заполнены поля Project | Project items = 16, а qualifying PBIs ≥21; поля `Status`, `Work status`, `Story Points`, `MVP Version` пусты | Добавить issue на доску и заполнить поля (вручную — у CLI нет прав) |
| 4 | Не у всех членов команды есть issue-linked PR за Assignment 3 | Только `whateverwillbewillbe` и `FuFill` | Попросить `Adelevere`, `Aydar-art`, `belelvser` создать PR |
| 5 | Не у всех членов команды есть review с текстом | `belelvser`, `FuFill`, `Aydar-art` только пустые approve | Оставить осмысленные комментарии в чужих PR |
| 6 | PR `#46`–`#60` смержены без ревью другого человека | В них только self-comment `whateverwillbewillbe` | Попросить товарищей approve/прокомментировать эти PR |
| 7 | Нет публичного видео <2 мин | `reports/week3/README.md` | Записать, выложить, вставить ссылку |
| 8 | Нет скриншотов в `reports/week3/images/` | Там папка пустая | Сделать скриншоты всех требуемых видов |
| 9 | В таблице contribution — `Name (TBD)` / `Role (TBD)` | `reports/week3/README.md` | Заполнить реальные ФИО и роли |
| 10 | Нет Moodle PDF | — | Сгенерировать PDF по шаблону |

### Средние

| # | Пробел | Где это видно | Что делать |
|---|--------|---------------|------------|
| 11 | Ссылка на `Process_Requirements.md` в корне битая | `reports/week3/README.md` | Либо добавить файл в репозиторий, либо заменить ссылку на пояснение |
| 12 | `#23` «Refactor route optimization algorithm…» висит открытым в Sprint 1, но не в MVP v1 | issues | Переместить в Sprint 2 / Product Backlog или закрыть как выполненное `#71` |
| 13 | Docker не проверен в этом окружении | — | Пользователь запускает `docker compose up --build` и делает smoke-тест |

---

## Реальные Story Points (после исправлений)

Расчёт по открытым/закрытым issue (без `#5` — Removed и без Course Task):

- Qualifying PBIs: 21 issue (6 user stories MVP v1 + 15 технических PBI + US-11/US-12 и US-05–US-08, если их тоже считать Done в Sprint 1).
- **MVP v1 (по label `mvp-v1`)**: `#6,7,8,18,19,26,30–44` = **62 SP**.
- **Sprint 1**, если туда же перенести выполненные `#9–12,20,21` = **91 SP**.
- **Product Backlog active** (все активные story, включая Sprint 2/3) ≈ **106 SP** (или **98 SP**, если `#23` закрыть).

> В `reports/week3/README.md` и `docs/user-stories.md` сейчас написано «34 SP» — это устаревшая цифра.

---

## Task 1: Исправить цифры и ссылки в отчётах

**Files:**
- Modify: `docs/user-stories.md`
- Modify: `reports/week3/README.md`
- Modify (опционально): описание milestone `Sprint 1` через GitHub API/веб-интерфейс

- [ ] **Step 1.1: Пересчитать SP**

Запустить:

```bash
.venv/Scripts/python - << 'PY'
import json, re
with open('issues.json',encoding='utf-8') as f:
    issues=json.load(f)
def pts(b):
    for pat in [r'\*\*Story Points:\*\*\s*(\d+)', r'## Story Points\s*\n\s*(\d+)']:
        m=re.search(pat, b or '')
        if m: return int(m.group(1))
    return 0
active=sum(pts(i['body']) for i in issues if 'removed' not in [l['name'] for l in i['labels']])
mvp=sum(pts(i['body']) for i in issues if 'mvp-v1' in [l['name'] for l in i['labels']])
sprint1=sum(pts(i['body']) for i in issues if i.get('milestone',{}).get('title')=='Sprint 1')
print('active', active, 'mvp-v1', mvp, 'sprint1', sprint1)
PY
```

- [ ] **Step 1.2: Вписать актуальные числа в `docs/user-stories.md` и `reports/week3/README.md`**

Заменить:

```markdown
- **Total Product Backlog size**: 34 Story Points
- **Total Sprint 1 size**: 34 Story Points
```

на:

```markdown
- **Total Product Backlog size**: <active> Story Points
- **Total Sprint 1 size**: <sprint1> Story Points
- **Total MVP v1 size**: <mvp-v1> Story Points
```

- [ ] **Step 1.3: Исправить/убрать битую ссылку на `Process_Requirements.md`**

Если файл не коммитится в репозиторий, заменить строку в `reports/week3/README.md`:

```markdown
- [Process Requirements](../../Process_Requirements.md)
```

на:

```markdown
- Process Requirements — course document used during backlog refinement (not committed to the public repo per team policy).
```

- [ ] **Step 1.4: Закоммитить и открыть PR**

```bash
git checkout -b docs/a3-report-corrections
git add docs/user-stories.md reports/week3/README.md
git commit -m "docs(week3): correct story-point totals and fix broken process link"
gh pr create --base main --title "docs(week3): correct Assignment 3 report numbers" --body "Closes #<issue-if-any>"
```

---

## Task 2: Синхронизировать состояние issue с отчётом

**Files:**
- Modify: issue bodies/state/milestone/labels через GitHub CLI

- [ ] **Step 2.1: Закрыть выполненные истории и переместить в Sprint 1**

Выполнены, но открыты в Sprint 2/3:

```bash
for n in 9 10 11 12 20 21; do
  "/c/Program Files/GitHub CLI/gh.exe" issue edit $n --repo Team-9-swp/Route-optimization-Platform-swp --milestone "Sprint 1" --add-label "Done"
  "/c/Program Files/GitHub CLI/gh.exe" issue close $n --repo Team-9-swp/Route-optimization-Platform-swp --reason completed
done
```

> Альтернатива: не ставить им `mvp-v1`, если они не входят в официально выбранный MVP v1 scope (оставить как дополнительный Sprint scope).

- [ ] **Step 2.2: Пометить `#5` как Removed**

```bash
"/c/Program Files/GitHub CLI/gh.exe" issue edit 5 --repo Team-9-swp/Route-optimization-Platform-swp --add-label "removed" --body-file - << 'EOF'
### User role / persona

Driver

### Desired action

Receive my route and order visit schedule

### Expected value

I can arrive at orders within the allowed time windows

### Description

**Requirement status:** Removed (split into US-01a #18 and US-01b #19).

Stable ID: US-01

User-story statement:
As a driver, I want to receive my route and order visit schedule,
so that I can arrive at orders within the allowed time windows.

MoSCoW priority: Must Have

Notes and constraints:
The vehicle route must respect time windows, vehicle capacity, shift duration, and depot start/end requirements.

### Acceptance criteria

- [ ] Driver can see the ordered list of stops for their route
- [ ] Each stop shows the expected arrival time
- [ ] Route begins and ends at the depot
EOF
"/c/Program Files/GitHub CLI/gh.exe" issue close 5 --repo Team-9-swp/Route-optimization-Platform-swp --reason "not planned"
```

- [ ] **Step 2.3: Переместить `#23` из Sprint 1**

```bash
"/c/Program Files/GitHub CLI/gh.exe" issue edit 23 --repo Team-9-swp/Route-optimization-Platform-swp --milestone "Sprint 2"
```

или закрыть как выполненное `#71`.

---

## Task 3: Заполнить GitHub Project

**Files:**
- Web UI проекта: https://github.com/orgs/Team-9-swp/projects/1

> CLI не имеет прав `AddProjectV2ItemById`, поэтому это действие только вручную или после выдачи прав администратора `whateverwillbewillbe` на проект.

- [ ] **Step 3.1: Добавить на доску все qualifying PBIs**

Добавить issue:

`#5` (Removed/Closed), `#6,7,8,9,10,11,12,13,14,18,19,20,21,23,26,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44`.

- [ ] **Step 3.2: Заполнить поля для каждого item**

| Поле | Значение |
|------|----------|
| `Status` | `Todo` / `In Progress` / `Done` (по состоянию issue) |
| `Work status` | `To Do` / `In Progress` / `Done` |
| `MoSCoW` | Must Have / Should Have / Could Have / Won't Have |
| `Story Points` | число из issue |
| `MVP Version` | `MVP v1` для label `mvp-v1`; `MVP v2` для Sprint 2/3 |
| `Milestone` | Sprint 1 / Sprint 2 / Sprint 3 |
| `Assignees` | тот, кто указан в issue |

- [ ] **Step 3.3: Настроить/проверить views**

- Product Backlog view (`views/1`) — группировка по `MoSCoW`.
- Sprint Backlog view (`views/2`) — фильтр `Milestone = Sprint 1`.
- MVP v1 view — фильтр/группировка по `MVP Version = MVP v1`.

---

## Task 4: Обеспечить участие каждого члена команды

**Files:**
- PR/MR на GitHub

- [ ] **Step 4.1: Issue-linked PR от каждого**

Кто не создавал issue-linked PR в Assignment 3, должен создать один (можно маленький docs/фикс):

| Участник | Минимальный PR |
|----------|----------------|
| `Adelevere` | Например, PR на редактирование `reports/week3/README.md` (имя/роль) |
| `Aydar-art` | Например, PR на добавление строки в CHANGELOG |
| `belelvser` | Например, PR на обновление `docs/definition-of-done.md` |

Ветка должна быть вида `<issue-number>-short-description`.

- [ ] **Step 4.2: Review с текстом от каждого**

Каждый из `belelvser`, `FuFill`, `Aydar-art`, `Adelevere` должен оставить **осмысленный** комментарий в чужом PR (не пустой approve).

- [ ] **Step 4.3: Ретро-ревью PR `#46`–`#60`**

Попросить `belelvser`, `Adelevere`, `Aydar-art`, `FuFill` зайти в эти PR и нажать `Approve` с коротким комментарием, чтобы у каждого issue-linked PR была проверка от другого человека.

---

## Task 5: Записать и выложить демо-видео

**Files:**
- `reports/week3/README.md`
- `README.md` (опционально)

- [ ] **Step 5.1: Записать экран <2 мин**

Содержание:

1. `docker compose up --build` (или `python -m uvicorn app.main:app` + `npm run dev`).
2. Swagger: `POST /solve`, `GET /jobs`, `GET /jobs/{id}`, `POST /validate`, `GET /health`.
3. Web UI: Dashboard → New Job → Job Detail с картой → Validate.

- [ ] **Step 5.2: Выложить на публичный хостинг**

YouTube (unlisted), Loom, Google Drive с публичной ссылкой и т.п.

- [ ] **Step 5.3: Вставить ссылку в отчёт**

В `reports/week3/README.md` заменить:

```markdown
- *(link to be added after recording...)*
```

на:

```markdown
- [Video demonstration (<2 min)](https://youtu.be/XXXXX)
```

---

## Task 6: Сделать скриншоты

**Files:**
- Create: `reports/week3/images/*.png`

- [ ] **Step 6.1: Сделать 7 скриншотов**

1. Product Backlog view
2. Sprint Backlog view
3. Sprint milestone page
4. MVP v1 grouped/filtered view
5. SemVer release `v1.0.0`
6. Delivered MVP v1 (Swagger + web UI side-by-side или два отдельных)
7. Example reviewed issue-linked PR (например, `#71` или `#46`)

- [ ] **Step 6.2: Встроить в `reports/week3/README.md`**

```markdown
## Screenshots

![Product Backlog](./images/product-backlog.png)
![Sprint Backlog](./images/sprint-backlog.png)
...
```

---

## Task 7: Заполнить contribution table

**Files:**
- Modify: `reports/week3/README.md`

- [ ] **Step 7.1: Заменить `Name (TBD)` и `Role (TBD)`**

Пример:

```markdown
| Name | GitHub username | Role | Issues / PBIs | PRs | Reviews |
|---|---|---|---|---|---|
| Иванов Иван | whateverwillbewillbe | Scrum Master / Full-stack | #7, #8, #26, #30–#44 | #45–#72 | #34, #39, #44, ... |
```

- [ ] **Step 7.2: Дополнить строки всеми реальными участниками**

Нужны: ФИО, GitHub username, Scrum-роль, список issue/PR/review.

---

## Task 8: Собрать Moodle PDF

**Files:**
- Create: `reports/week3/Assignment3_Submission_Team9.pdf`

- [ ] **Step 8.1: Собрать документ**

Содержание по `Assignment_03.md`:

1. Название проекта и номер команды.
2. Таблица: ФИО, GitHub username, роль, university identity mapping.
3. Summary of contributions.
4. Commit-hash permalink к `reports/week3/README.md`.
5. Commit-hash permalink к дереву репозитория на `main`.
6. Live links: Product Backlog, Sprint Backlog, Sprint milestone, MVP v1 view, release, deployment, video.
7. Live links: `docs/user-stories.md`, Process Requirements, roadmap, DoD, CHANGELOG.
8. Links to reviewed issue-linked PRs.
9. Access instructions for MVP v1.
10. Customer recording link (если разрешено делиться только инструкторам).
11. Sanitized transcript / notes.
12. Customer feedback summary.

- [ ] **Step 8.2: Проверить все ссылки перед отправкой**

- [ ] **Step 8.3: Загрузить в Moodle**

---

## Task 9: Docker smoke test

**Files:**
- `docker-compose.yml`, `README.md`

- [ ] **Step 9.1: Запустить стек**

```bash
docker compose up --build -d
```

- [ ] **Step 9.2: Проверить endpoints**

```bash
curl http://localhost:8000/health
curl -X POST "http://localhost:8000/solve?seed=42&time_limit=120" -H "Content-Type: application/json" -d @test_cases/t1.json
```

- [ ] **Step 9.3: Открыть `http://localhost:3000` и проверить UI**

---

## Self-review checklist

- [ ] Все 15+ qualifying PBIs имеют Type, Description, Work Status, MoSCoW, Story Points, Milestone, Assignee.
- [ ] Все MVP v1 PBIs имеют ≥3 acceptance criteria.
- [ ] Все MVP v1 PBIs закрыты (`Done`).
- [ ] Каждый участник: push commit, issue-linked PR, review+approve, осмысленный комментарий.
- [ ] `docs/user-stories.md` содержит актуальные ссылки и статусы.
- [ ] `reports/week3/README.md` содержит правильные SP, видео, скриншоты, contribution table.
- [ ] GitHub Project board заполнен и публично доступен.
- [ ] Release `v1.0.0` указывает на `main`.
- [ ] PDF создан и все ссылки в нём рабочие.
