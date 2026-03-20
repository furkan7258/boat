# CLAUDE.md — BoAT (Boğaziçi University Annotation Tool)

## Project Overview

Collaborative tool for linguistic annotation of Universal Dependencies treebanks. Available as a web app and a Tauri desktop app.

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI 0.115 + SQLAlchemy 2.0 (async) + asyncpg |
| Database | PostgreSQL 16 |
| Frontend | SvelteKit 2 + Svelte 5 + TypeScript + Tailwind CSS 4 |
| Auth | JWT (python-jose + bcrypt) |
| Migrations | Alembic (async) |
| Packaging | uv (backend), npm (frontend) |
| Server | Uvicorn + Caddy |
| Linting | ruff (backend), svelte-check (frontend) |
| Tests | pytest + pytest-asyncio (backend) |
| CI/CD | GitLab CI (.gitlab-ci.yml) |

## Directory Structure

```
backend/
  app/
    main.py             # FastAPI app factory, CORS, router includes
    core/
      config.py         # Pydantic Settings (env vars)
      security.py       # JWT create/verify, bcrypt, get_current_user dep
      database.py       # Async engine, sessionmaker, get_db dep
    models/             # SQLAlchemy 2.0 mapped classes (8 tables)
    schemas/            # Pydantic request/response models
    routers/            # API route handlers (9 routers)
    services/
      conllu.py         # CoNLL-U parse/validate/export
      agreement.py      # Inter-annotator agreement
    data/
      language_ids.json # Language code list
  alembic/              # DB migrations
  tests/                # pytest test suite
  pyproject.toml
  Dockerfile            # Production (multi-stage, non-root)
  Dockerfile.dev        # Development (hot reload)
  entrypoint.sh         # Runs migrations then starts uvicorn

frontend/
  src/
    lib/
      api/              # Typed fetch client (mode-aware: fetch or Tauri invoke)
      components/
        annotation/     # AnnotationTable, Cell, Toolbar, SearchableSelect, FeatsEditor
        graph/          # DisplacyGraph (SVG arcs), DiffView
        common/         # Button, Input, Modal, Toast, Tooltip, Skeleton
        layout/         # Navbar, Breadcrumb
        desktop/        # ConnectDialog, DesktopShortcuts
      stores/           # auth, annotation, mode, preferences, theme, toast
      utils/            # keyboard shortcuts, cn(), ud-tagsets
    routes/             # SvelteKit pages
    app.css             # Tailwind 4 theme + dark mode
  src-tauri/            # Tauri v2 Rust backend (desktop app)
    src/
      commands.rs       # API dispatch + file I/O commands
      conllu.rs         # CoNLL-U parser/exporter (Rust)
      document.rs       # In-memory document state
  Dockerfile            # Production (multi-stage, adapter-node)
  Dockerfile.dev        # Development (hot reload)

docker-compose.yml      # Production: backend + frontend + db + caddy
docker-compose.dev.yml  # Development: backend + frontend + db
Caddyfile               # Reverse proxy (/api/* → backend, /* → frontend)
.env.example            # Required env vars template
```

## Development Commands

### Backend

```bash
cd backend

# Install deps (needs uv)
pip install uv
uv pip install --system -e ".[dev]"

# Run tests
python -m pytest tests/ -v --tb=short

# Lint
ruff check app/
ruff format --check app/

# Run dev server (standalone)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"
```

### Frontend

```bash
cd frontend

# Install deps
npm ci

# Dev server (port 5173, proxies /api → localhost:8000)
npm run dev

# Type check
npm run check

# Production build
npm run build
```

### Docker (Development)

```bash
# Start all services (db + backend + frontend)
docker compose -f docker-compose.dev.yml up --build

# Backend: http://localhost:8000 (API docs: /docs)
# Frontend: http://localhost:5173
# DB: localhost:5432 (boat/boat)
```

### Docker (Production via Cloudflare Tunnel)

```bash
cp .env.example .env
# Edit .env — set POSTGRES_PASSWORD, SECRET_KEY, DOMAIN

docker compose up -d --build
# Caddy listens on 127.0.0.1:8880 (HTTP only)
# Add to cloudflared config:
#   - hostname: $DOMAIN
#     service: http://localhost:8880
# TLS is terminated at the Cloudflare edge
```

## API Structure

All API routes are prefixed with `/api`:

| Router | Prefix | Key endpoints |
|--------|--------|---------------|
| auth | `/auth` | POST /register, POST /login, GET /me |
| treebanks | `/treebanks` | CRUD + /upload, /export, /progress |
| sentences | `/sentences` | CRUD + /annotations |
| annotations | `/annotations` | CRUD + GET /by-position/, GET /mine |
| wordlines | `/wordlines` | PUT /annotations/{id}/wordlines (batch) |
| search | `/search` | GET with multi-field query |
| comments | `/comments` | CRUD per sentence |
| guidelines | `/guidelines` | CRUD per treebank |
| validation | `/validation` | Validation profiles per treebank |

Health check: `GET /health` (no /api prefix).

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DATABASE_URL | Yes (prod) | — | PostgreSQL connection string |
| SECRET_KEY | Yes | — | JWT signing key |
| POSTGRES_PASSWORD | Yes (compose) | — | DB password |
| POSTGRES_USER | No | boat | DB username |
| POSTGRES_DB | No | boat | DB name |
| ACCESS_TOKEN_EXPIRE_MINUTES | No | 480 | JWT token lifetime |
| ALLOWED_ORIGINS | No | `["https://$DOMAIN"]` | CORS origins |
| DOMAIN | No | localhost | Domain for CORS + SvelteKit ORIGIN |

## Key Patterns

- **Svelte 5 runes**: Use `$state`, `$derived`, `$effect`, `$props`, `$bindable` — not legacy `$:` or `let:`.
- **Path aliases**: `$components`, `$stores`, `$api`, `$utils` (configured in svelte.config.js).
- **Async SQLAlchemy**: All DB access uses `AsyncSession` via `get_db` dependency.
- **JWT auth**: `get_current_user` dependency extracts user from Bearer token.
- **CoNLL-U**: 10-column tab-separated format for linguistic annotations. Fields: ID, FORM, LEMMA, UPOS, XPOS, FEATS, HEAD, DEPREL, DEPS, MISC.
- **AnnotationStatus**: IntEnum — 0=NEW, 1=DRAFT, 2=SUBMITTED, 3=APPROVED, 4=REJECTED.
- **Template annotations**: `is_template=True` annotations hold the original CoNLL-U data. User annotations are copies.
- **Batch wordline update**: `PUT /annotations/{id}/wordlines` replaces all wordlines in one request.

## Testing

Backend tests use pytest-asyncio with aiosqlite (in-memory SQLite). The test fixture creates tables via `Base.metadata.create_all`.

```bash
cd backend && python -m pytest tests/ -v
```

## Git

- Default branch: `main`
- CI runs on all branches; Docker image builds only on `main`
