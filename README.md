# React Fast Template

Monorepo: FastAPI backend (`backend/`) + React frontend (`frontend/`).

## Overview

- **Backend** — modular FastAPI API: centralized config (`app/core`), shared layers (`app/common`), feature modules (`app/modules` — auth, users), middleware, Alembic migrations, worker stub, and Docker image.
- **Frontend** — React SPA: app providers (`src/providers`), shared utilities (`src/shared`), feature modules with Zod schemas and Zustand stores (`src/modules`), file-based routes (`src/routes`), Axios HTTP client, env validation, Biome lint/format, TypeScript project references, and a multi-stage Docker image (Node build → nginx).

## Tech stack

### Backend

| Layer | Technology |
| --- | --- |
| Runtime | Python `>=3.14` |
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
| Runtime | Node.js `^20.19.0 \|\| ^22.12.0` (see `frontend/package.json` `engines`) |
| Package manager | npm (swap via `PM_FE` in root `Makefile`) |
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
# Configure git hooks (once per clone)
make setup

# Install everything
make install-all

# Backend env
cp backend/.env.example backend/.env
# Fill in Postgres, Redis, and JWT settings

# Frontend env
cp frontend/.env.example frontend/.env
# Set VITE_API_URL (must be a valid URL; validated at startup via Zod)

# Run migrations
make upgrade

# Start (separate terminals)
make start-backend
make start-frontend
```

- API docs: `http://127.0.0.1:8000/docs`
- App: `http://127.0.0.1:3000`

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
| `make setup` | Configure git hooks |
| `make install-all` | Install backend + frontend deps |
| `make install-backend` | `uv sync --dev` in `backend/` |
| `make install-frontend` | `npm install` in `frontend/` |
| `make start-backend` | Uvicorn with `--reload` |
| `make start-frontend` | Vite dev server |
| `make migration msg="..."` | Create an Alembic migration (autogenerate) |
| `make upgrade` | Apply migrations to `head` |
| `make downgrade` | Roll back one revision |
| `make history` | Show migration history |
| `make current` | Show current revision |
| `make check-backend` | Ruff check |
| `make fix-backend` | Ruff check + autofix |
| `make typecheck-backend` | mypy |
| `make check-frontend` | Biome check |
| `make fix-frontend` | Biome format |
| `make typecheck-frontend` | TypeScript build-mode check |
| `make check-all` | Check backend + frontend |
| `make typecheck-all` | Typecheck backend + frontend |

Or run tools directly:

```bash
# Backend
cd backend
uv run uvicorn app.main:app --reload --no-access-log
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

Verify SPA routing: open `/auth/login` and refresh — nginx should still serve the app (not a raw 404).

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
├── docker-compose.yaml
│
├── .githooks/
│   ├── _lib.sh
│   ├── pre-commit
│   └── pre-push
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── redis.py
│   │   │   ├── security.py
│   │   │   ├── logging.py
│   │   │   ├── exception.py
│   │   │   └── dependency.py
│   │   │
│   │   ├── common/
│   │   │   ├── base_model.py
│   │   │   ├── base_schema.py
│   │   │   ├── base_repository.py
│   │   │   ├── pagination.py
│   │   │   ├── response.py
│   │   │   └── utils.py
│   │   │
│   │   ├── modules/
│   │   │   ├── auth/
│   │   │   │   ├── dependency.py
│   │   │   │   ├── schema.py
│   │   │   │   ├── repository.py
│   │   │   │   ├── service.py
│   │   │   │   └── router.py
│   │   │   └── users/
│   │   │       ├── model.py
│   │   │       ├── dependency.py
│   │   │       ├── schema.py
│   │   │       ├── repository.py
│   │   │       ├── service.py
│   │   │       └── router.py
│   │   │
│   │   ├── middleware/
│   │   │   ├── cors.py
│   │   │   └── logging.py
│   │   ├── main.py
│   │   └── router.py
│   │
│   ├── alembic/
│   │   └── versions/
│   ├── worker/
│   │   └── tasks.py
│   ├── .env.example
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
    │   │       ├── providers/
    │   │       │   └── auth-provider.tsx
    │   │       ├── utils/
    │   │       │   └── session.ts
    │   │       ├── api.ts
    │   │       ├── constants.ts
    │   │       ├── mapper.ts
    │   │       ├── query.ts
    │   │       ├── schemas.ts
    │   │       └── store.ts
    │   ├── providers/
    │   │   ├── query-provider.tsx
    │   │   └── router-provider.tsx
    │   ├── routes/
    │   │   ├── auth/
    │   │   │   └── login.tsx
    │   │   ├── __root.tsx
    │   │   └── index.tsx
    │   ├── shared/
    │   │   ├── api/
    │   │   │   └── http-client.ts
    │   │   ├── hooks/
    │   │   │   ├── use-click-outside.ts
    │   │   │   └── use-debounce.ts
    │   │   └── utils/
    │   │       └── cn.ts
    │   ├── App.tsx
    │   ├── main.tsx
    │   ├── index.css
    │   └── routeTree.gen.ts
    │
    ├── public/
    ├── index.html
    ├── .env.example
    ├── biome.json
    ├── Dockerfile
    ├── nginx.conf
    ├── package.json
    ├── tsr.config.json
    ├── vite.config.ts
    └── tsconfig.json
```
