# Architecture

## High-level flow

```text
Job Sources
   |
   v
Sourcing / Normalization
   |
   v
Hard Filters
   |
   v
Matching + Ranking
   |
   v
Interactive Job Cockpit
   |
   +--> Like / Reject / Apply / More
   |
   v
Preference Store
   |
   v
Updated Ranking

For shortlisted roles:

Job Description
   |
   +--> Claude CV Tailor
   |
   +--> OpenAI Cover Letter Writer
   |
   v
Application Evaluator
   |
   v
Human Review
```

## Initial implementation stack

- Backend: FastAPI
- Validation: Pydantic
- Database: PostgreSQL
- ORM: SQLAlchemy
- Migrations: Alembic
- Frontend: React
- Containerization: Docker
- Testing: pytest
- CI/CD: GitHub Actions

Later stages:
- MCP
- ChatGPT Apps SDK
- Anthropic API
- OpenAI API
- LangGraph or another explicit workflow engine
- pgvector where semantic preference/job retrieval is useful
- Langfuse or equivalent observability

## Design rule

Do not introduce agent frameworks until the workflow is stable enough to justify them.

Milestone 1 should use ordinary deterministic application code for:
- job storage
- feedback
- filtering
- scoring
- ranking

Agentic orchestration enters only after the product loop is useful.
