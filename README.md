# React Fast Template

Monorepo: FastAPI backend (`backend/`) + React frontend (`frontend/`).

## Overview

- **Backend** — modular FastAPI API: centralized config (`app/core`), shared layers (`app/common`), feature modules (`app/modules` — auth, users), middleware, Alembic migrations, worker stub, and Docker image.
- **Frontend** — React SPA: app providers (`src/providers`), shared utilities (`src/shared`), feature modules with Zod schemas and Zustand stores (`src/modules`), file-based routes (`src/routes`), Axios HTTP client, env validation, Biome lint/format, TypeScript project references, and a multi-stage Docker image (Node build → nginx).

## Tech stack

### Backend

| Layer | Technology |
| --- | --- |
| Runtime | Python `>=3.14` (see `backend/.python-version`) |
| Package manager | [uv](https://github.com/astral-sh/uv) |
| Web framework | FastAPI + Uvicorn |
| ORM / DB | SQLAlchemy 2 + asyncpg (PostgreSQL) |
| Migration | Alembic |
| Cache / session | Redis |
| Auth | JWT (PyJWT) + bcrypt |
| Validation / settings | Pydantic Settings |
| Lint / typecheck | Ruff, mypy |

### Frontend

| Layer | Technology |
| --- | --- |
| Runtime | Node.js `22` (see `frontend/.nvmrc`; `engines` also allow `^20.19.0`) |
| Package manager | npm (swap via `FE_PM` in root `Makefile`) |
| Bundler / dev server | Vite |
| UI library | React 19 |
| Routing | TanStack Router |
| Server state | TanStack Query |
| Client state | Zustand |
| Validation | Zod |
| HTTP | Axios |
| Styling | Tailwind CSS 4 |
| Lint / format | Biome |
| Typecheck | TypeScript (`tsc -b`) |
| Production image | Multi-stage Docker + nginx |

## Quick start

```bash
# Install deps and create .env files
make setup-all

# Fill in backend/.env (Postgres, Redis, JWT)
# Confirm frontend/.env has a valid VITE_API_URL

# Run migrations
make upgrade-backend

# Start (separate terminals)
make start-backend
make start-frontend
```

- API docs: `http://127.0.0.1:8000/docs`
- App: `http://127.0.0.1:3000`

List all Make targets: `make help`.

Git hooks live in `.githooks/` (pre-commit runs check + typecheck for changed sides). Enable once per clone:

```bash
git config core.hooksPath .githooks
chmod -R +x .githooks
```

## Environment

### Frontend

| Variable | Description |
| --- | --- |
| `VITE_API_URL` | Backend API base URL (exposed to the client by Vite) |

Validated in `frontend/src/configs/env.ts`. Missing or invalid values fail fast on boot / build.

Vite inlines `VITE_*` at **build time**. The value must be reachable from the **browser** (not an internal Docker service hostname unless the browser can resolve it).

### Backend

See `backend/.env.example` for CORS, Postgres, Redis, and JWT settings.

## Commands

All commands run from the repo root via the root `Makefile`.

| Command | Description |
| --- | --- |
| `make help` | List targets |
| `make setup-all` | Install frontend + backend deps and create `.env` files |
| `make setup-frontend` | `npm install` + copy `frontend/.env` if missing |
| `make setup-backend` | `uv sync --dev` + copy `backend/.env` if missing |
| `make start-frontend` | Vite dev server |
| `make start-backend` | Uvicorn with `--reload` |
| `make revision-backend msg="..."` | Create an Alembic migration (autogenerate) |
| `make upgrade-backend` | Apply migrations to `head` |
| `make downgrade-backend` | Roll back one revision |
| `make check-frontend` | Biome check |
| `make fix-frontend` | Biome check + write |
| `make typecheck-frontend` | TypeScript build-mode check |
| `make check-backend` | Ruff check |
| `make fix-backend` | Ruff check + autofix |
| `make typecheck-backend` | mypy |
| `make check-all` | Check frontend + backend |
| `make fix-all` | Auto-fix frontend + backend |
| `make typecheck-all` | Typecheck frontend + backend |

Or run tools directly:

```bash
# Backend
cd backend
uv run uvicorn app.main:app --reload
uv run alembic upgrade head
uv run ruff check .
uv run mypy .

# Frontend
cd frontend
npm install
npm run start
npm run check
npm run fix
npm run typecheck
npm run build
npm run preview
```

## CI

`.github/workflows/ci.yml` runs on `push` / `pull_request` to `master`.

- Detects changes under `frontend/` and `backend/`
- Frontend: `npm ci`, `npm run check`, `npm run typecheck`
- Backend: `uv sync --dev`, `ruff check`, `mypy`
- Telegram notify (optional): set repo secrets `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `TELEGRAM_THREAD_ID`

## Docker

### Frontend

Multi-stage build: compile the SPA with Node, serve `dist/` with nginx (SPA `try_files` fallback in `frontend/nginx.conf`).

```bash
cd frontend

# Build (VITE_API_URL is required — baked into the bundle)
docker build \
  --build-arg VITE_API_URL=http://localhost:8000 \
  -t react-fast-template-frontend .

# Run (host 3000 → container nginx 80)
docker run --rm -p 3000:80 react-fast-template-frontend
```

App: `http://127.0.0.1:3000` (same port as local Vite)

Verify SPA routing: open `/login` and refresh — nginx should still serve the app (not a raw 404).

### Backend

```bash
cd backend

docker build -t react-fast-template-backend .

docker run --rm -p 8000:8000 --env-file .env react-fast-template-backend
```

API docs: `http://127.0.0.1:8000/docs`

## Project structure

```
react-fast-template/
│
├── Makefile
├── README.md
│
├── .githooks/
│   ├── _lib.sh
│   ├── pre-commit
│   └── pre-push
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── common/
│   │   ├── modules/
│   │   │   ├── auth/
│   │   │   └── users/
│   │   ├── middleware/
│   │   ├── main.py
│   │   └── router.py
│   ├── alembic/
│   ├── worker/
│   ├── .env.example
│   ├── .python-version
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── pyproject.toml
│   └── uv.lock
│
└── frontend/
    ├── src/
    │   ├── configs/
    │   │   └── env.ts
    │   ├── modules/
    │   │   └── auth/
    │   ├── providers/
    │   ├── routes/
    │   │   ├── _protected.tsx
    │   │   ├── _protected/
    │   │   ├── _public.tsx
    │   │   ├── _public/
    │   │   ├── __root.tsx
    │   │   └── index.tsx
    │   ├── shared/
    │   ├── App.tsx
    │   ├── main.tsx
    │   └── routeTree.gen.ts
    ├── .env.example
    ├── .nvmrc
    ├── biome.json
    ├── Dockerfile
    ├── nginx.conf
    ├── package.json
    └── vite.config.ts
```
