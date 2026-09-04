# Job Search Copilot

An agentic job-search system for discovering, ranking, reviewing, and preparing applications for AI/ML roles in the Netherlands and Europe.

## Primary user goal

Help the candidate find and prioritize roles in:
- AI Engineering
- Agentic AI Engineering
- LLM / Applied AI Engineering
- ML Engineering
- Data Science focused on ML systems
- Biomedical AI / Bioinformatics / Drug Discovery AI

The system should learn from explicit user feedback over time and improve ranking quality.

## Core product principles

1. Ground all candidate claims in verified candidate evidence.
2. Prefer relevant live roles over keyword-similar but unrealistic roles.
3. Treat Dutch-language requirements as hard constraints unless explicitly relaxed.
4. Optimize for actual user preference, not only semantic similarity.
5. Keep application-generation steps human-in-the-loop.
6. Do not fabricate candidate skills, achievements, years of experience, or company facts.

## Planned system components

- Job sourcing and normalization
- Candidate-job matching
- Preference learning
- Interactive job review cockpit
- CV tailoring via Claude
- Cover-letter generation via OpenAI
- Factuality and application-quality evaluation
- MCP / ChatGPT integration
- Observability and evaluation

See `docs/ROADMAP.md` for staged implementation.

## Milestone 1 — Feedback Loop (implemented)

A local, deterministic app: 10 fixture jobs displayed as cards with a
transparent fit score, Like / Reject / Shortlist actions, optional reject
reasons, append-only feedback history in PostgreSQL, and a ranking that
re-sorts as learned preference signals accumulate. No LLM calls are made
anywhere in this milestone.

- Backend: FastAPI + SQLAlchemy 2.x + Alembic + PostgreSQL (`backend/`)
- Frontend: React + TypeScript + Vite (`frontend/`)
- The 10 seed jobs are **fictional development fixtures** (see
  `backend/app/seed/seed_data.py`), not live vacancies.

### Run everything with Docker

```bash
cp .env.example .env
docker compose up --build
```

Then, once the containers are up, load the fixture jobs (only needed once,
or whenever you want to reset to a clean demo state):

```bash
docker compose exec backend python -m app.seed.seed
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000 (docs at `/docs`)
- Postgres: localhost:5432 (credentials from `.env`)

Re-running the seed command wipes all Feedback/PreferenceSignal/Job data and
reloads the fixed 10-job set from scratch — it's a full reset, not a merge.

### Run locally without Docker

Backend (requires a local PostgreSQL and Python 3.12+):

```bash
cd backend
python3.12 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example .env   # edit DATABASE_URL if needed
alembic upgrade head
python -m app.seed.seed
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
echo "VITE_API_BASE_URL=http://localhost:8000/api" > .env
npm run dev
```

### Database migrations

```bash
cd backend
alembic revision --autogenerate -m "describe the change"
alembic upgrade head
```

### Tests

```bash
cd backend
source .venv/bin/activate
python -m pytest -q
```

Tests run against a real PostgreSQL database (`job_search_copilot_test` by
default, see `backend/tests/conftest.py`) — not SQLite or mocks — so
JSONB/enum behavior matches production. Create it once:

```sql
CREATE DATABASE job_search_copilot_test OWNER copilot;
```

### Architecture notes specific to Milestone 1

- `MatchScore` is computed once, deterministically, per `agents/MATCHER.md`
  (`backend/app/services/scoring.py`) and is never modified by feedback.
- `Feedback` is append-only: changing your mind about a job adds a new row,
  it never edits or deletes an old one.
- `PreferenceSignal` is always rebuilt by replaying the full `Feedback`
  history (`backend/app/services/preference_learner.py`) — it is a derived
  projection, never a second source of truth.
- Ranking (`backend/app/services/ranking.py`) = `base_score` (MatchScore) +
  `preference_adjustment` (live, from PreferenceSignal), with a per-job
  `preference_explanation` list so any ranking difference is inspectable.
  Jobs with a hard-constraint blocker (e.g. mandatory Dutch) always sort
  below jobs without one, regardless of score.
