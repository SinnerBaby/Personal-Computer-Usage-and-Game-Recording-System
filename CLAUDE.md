# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This is a **three-tier local-first personal data tracking system** (PC usage + game recording):

```
client/        → Windows data collection agent (Python, pywin32 + psutil)
backend/       → REST API server (FastAPI + SQLAlchemy + SQLite)
frontend/      → SPA dashboard (Vue 3 + TypeScript + Element Plus + ECharts)
```

Data flows: **client → backend (REST API) → frontend fetches/charts**. No third-party services involved.

### Data Model (SQLite)

Three domain tables anchored by `app/database.py`:
- **users** (`app/models/user.py`) — JWT auth, bcrypt password
- **app_usage / app_categories** (`app/models/app_usage.py`) — per-process usage records with optional category grouping
- **games / game_tags / game_sessions** (`app/models/game.py`) — game library + play sessions, many-to-many tags

## Project Structure

```
├── backend/app/           # FastAPI server
│   ├── main.py            # App factory, CORS, router registration
│   ├── config.py          # Pydantic Settings (reads .env)
│   ├── database.py        # SQLAlchemy engine + session + Base
│   ├── models/            # ORM models
│   ├── schemas/           # Pydantic request/response schemas
│   ├── api/v1/            # Route handlers (auth, apps, games, stats, dashboard, sync, data)
│   ├── services/          # Business logic layer
│   └── utils/             # security.py (JWT/bcrypt), dependencies.py (auth guard), response.py (unified format)
├── client/                # Windows data collector
│   ├── collector/
│   │   ├── main.py        # Main loop: collect → buffer → sync every 60s
│   │   ├── window_monitor.py   # pywin32 GetForegroundWindow, track active app switches
│   │   ├── game_detector.py    # Process name → known game mapping (with wildcard support)
│   │   └── data_sender.py      # HTTP POST to backend /sync endpoints
│   └── config/config.yaml # Server URL, intervals, custom game list
├── frontend/src/          # Vue 3 SPA
│   ├── main.ts            # App bootstrap (Pinia + Router + ElementPlus)
│   ├── router/index.ts    # Auth guard (currently bypassed), lazy-loaded routes
│   ├── api/               # Axios client per domain (apps.ts, games.ts, stats.ts, ...)
│   ├── stores/            # Pinia stores (auth, theme, dashboard, apps, games, settings)
│   ├── types/             # TypeScript interfaces (api.d.ts, app.d.ts, dashboard.d.ts, ...)
│   ├── views/             # Page components (dashboard, apps, games, stats, settings, data)
│   └── utils/             # date.ts, format.ts, storage.ts, validation.ts
└── README.md
```

### Backend Conventions

- **Response format**: All endpoints return `{ code, message, data, timestamp }` via `utils/response.py`. Paginated endpoints wrap `data` as `{ list, pagination }`.
- **Auth**: Bearer JWT, validated by `utils/dependencies.py:get_current_user()`.
- **DB session**: FastAPI dependency `database.py:get_db()` wraps `SessionLocal`.
- **Routers registered in `main.py`** under `/api/v1/*`.

### Frontend Conventions

- **Auto-imports**: Vue, Vue Router, Pinia, and Element Plus components are auto-imported (see `vite.config.ts`). No manual import needed for these.
- **HTTP client**: `api/index.ts` — Axios instance with Token auto-attach + unified error handling.
- **State**: Pinia stores in `stores/`, each mirrors a backend domain.
- **Proxy**: Vite dev server proxies `/api` → `localhost:8000` (defined in `vite.config.ts`).
- **Router**: Lazy-loaded routes, `requiresAuth` meta flag (guard currently bypassed).

### Client Data Pipeline

```
WindowMonitor (5s interval, tracks active window switches)
  → buffers records in memory
  → DataSender flushes to backend every 60s via POST /api/v1/sync/app-usage
  → GameDetector matches process_name against known_games dict
```

## Key Commands

```bash
# Backend
cd backend
python -m venv .venv && .venv/Scripts/activate   # Windows setup
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000          # Dev server
# API docs at http://localhost:8000/docs

# Frontend
cd frontend
npm install
npm run dev                                        # Dev server on :5173
npm run build                                      # Production build

# Client (Windows only)
cd client
pip install -r requirements.txt
python -m collector.main                          # Start data collection

# VS Code: Tasks (Ctrl+Shift+B) can launch all three simultaneously
```

## Config Locations

- **Backend**: `backend/.env` overrides `backend/app/config.py:Settings` defaults
- **Client**: `client/config/config.yaml` (server URL, intervals, custom game process list)
- **Frontend**: `frontend/.env.development` (API base URL)
