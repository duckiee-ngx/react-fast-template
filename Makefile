# Package managers
FE_PM := npm --prefix frontend
FE_RUN := $(FE_PM) run

BE_PM := uv --directory backend
BE_RUN := $(BE_PM) run
BE_ALEMBIC := $(BE_RUN) alembic

.DEFAULT_GOAL := help

.PHONY: \
	help \
	setup-all check-all fix-all typecheck-all \
	setup-frontend \
	start-frontend \
	check-frontend fix-frontend typecheck-frontend \
	setup-backend \
	start-backend \
	check-backend fix-backend typecheck-backend \
	revision-backend upgrade-backend downgrade-backend

help:
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\n"} \
		/^[a-zA-Z0-9_-]+:.*##/ { printf "  %-22s %s\n", $$1, $$2 } \
		/^# ──/ { printf "\n%s\n", $$0 }' $(MAKEFILE_LIST)

# ── Workspace ────────────────────────────────────────────────────────────────

setup-all: setup-frontend setup-backend ## Set up frontend and backend
check-all: check-frontend check-backend ## Lint frontend and backend
fix-all: fix-frontend fix-backend ## Auto-fix frontend and backend
typecheck-all: typecheck-frontend typecheck-backend ## Typecheck frontend and backend

# ── Frontend ─────────────────────────────────────────────────────────────────

setup-frontend: ## Install frontend deps and create .env
	$(FE_PM) install
	test -f frontend/.env || cp frontend/.env.example frontend/.env

start-frontend: ## Start the frontend dev server
	$(FE_RUN) start

check-frontend: ## Lint the frontend
	$(FE_RUN) check

fix-frontend: ## Auto-fix frontend lint
	$(FE_RUN) fix

typecheck-frontend: ## Typecheck the frontend
	$(FE_RUN) typecheck

# ── Backend ──────────────────────────────────────────────────────────────────

setup-backend: ## Install backend deps and create .env
	$(BE_PM) sync --dev
	test -f backend/.env || cp backend/.env.example backend/.env

start-backend: ## Start the backend dev server
	$(BE_RUN) uvicorn app.main:app --reload

check-backend: ## Lint the backend
	$(BE_RUN) ruff check .

fix-backend: ## Auto-fix backend lint
	$(BE_RUN) ruff check --fix .

typecheck-backend: ## Typecheck the backend
	$(BE_RUN) mypy .

revision-backend: ## Create a migration (msg="add users")
	test -n "$(msg)" || (echo 'usage: make revision-backend msg="add users"' && exit 1)
	$(BE_ALEMBIC) revision --autogenerate -m "$(msg)"

upgrade-backend: ## Apply migrations to head
	$(BE_ALEMBIC) upgrade head

downgrade-backend: ## Roll back the last migration
	$(BE_ALEMBIC) downgrade -1
