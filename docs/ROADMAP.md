# Roadmap

## Milestone 1 — Feedback Loop

Goal:
Create a local application that can display jobs as cards, accept Like/Reject feedback, persist feedback, and re-rank jobs using deterministic preference signals.

Deliverables:
- FastAPI backend
- PostgreSQL database
- SQLAlchemy models
- Alembic migrations
- React job-card UI
- Like / Reject interactions
- optional rejection reasons
- deterministic ranking
- seed dataset with 10 sample jobs
- tests

No LLM API calls yet.

## Milestone 2 — Live Job Ingestion

Add:
- source adapters
- normalization
- deduplication
- freshness checks
- hard filters
- daily sourcing workflow

## Milestone 3 — AI Matching

Add:
- structured LLM-assisted requirement extraction
- grounded candidate-job matching
- evaluation dataset
- OpenAI API integration

## Milestone 4 — Application Generation

Add:
- Claude CV tailoring
- OpenAI cover-letter generation
- factuality evaluator
- human approval workflow

## Milestone 5 — Agentic Orchestration

Add:
- explicit workflow graph
- LangGraph or equivalent
- retries / failure handling
- structured state
- observability

## Milestone 6 — MCP + ChatGPT UI

Expose:
- get_daily_jobs
- like_job
- reject_job
- shortlist_job
- generate_application
- get_application_package

Build a ChatGPT-facing interactive experience.

## Milestone 7 — Preference Learning

Compare deterministic preference ranking against learned models.

Only deploy learned ranking if evaluation improves.
