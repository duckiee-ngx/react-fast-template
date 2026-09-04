# Package managers
PM_FE := cd frontend && npm
PM_FE_RUN := $(PM_FE) run
PM_BE := cd backend && uv
PM_BE_RUN := $(PM_BE) run
ALEMBIC := $(PM_BE_RUN) alembic

.PHONY: \
	setup \
	install-frontend install-backend install-all \
	start-frontend start-backend \
	migration upgrade downgrade history current \
	check-backend fix-backend typecheck-backend \
	check-frontend fix-frontend typecheck-frontend \
	check-all typecheck-all

# ── Setup ──────────────────────────────────────────────────────────────

setup:
	git config core.hooksPath .githooks
	chmod -R +x .githooks

# ── Install ──────────────────────────────────────────────────────────────────

install-frontend:
	$(PM_FE) install

install-backend:
	$(PM_BE) sync --dev

install-all: install-frontend install-backend

# ── Start ────────────────────────────────────────────────────────────────────

start-frontend:
	$(PM_FE_RUN) start

start-backend:
	$(PM_BE_RUN) uvicorn app.main:app --reload --no-access-log

# ── Backend: DB migrations ───────────────────────────────────────────────────

migration:
	$(ALEMBIC) revision --autogenerate -m "$(msg)"

upgrade:
	$(ALEMBIC) upgrade head

downgrade:
	$(ALEMBIC) downgrade -1

history:
	$(ALEMBIC) history

current:
	$(ALEMBIC) current

# ── Backend: quality ─────────────────────────────────────────────────────────

check-backend:
	$(PM_BE_RUN) ruff check .

fix-backend:
	$(PM_BE_RUN) ruff check --fix .

typecheck-backend:
	$(PM_BE_RUN) mypy .

# ── Frontend: quality ────────────────────────────────────────────────────────

check-frontend:
	$(PM_FE_RUN) check

fix-frontend:
	$(PM_FE_RUN) fix

typecheck-frontend:
	$(PM_FE_RUN) typecheck

# ── Combined quality ─────────────────────────────────────────────────────────

check-all: check-backend check-frontend

typecheck-all: typecheck-backend typecheck-frontend
