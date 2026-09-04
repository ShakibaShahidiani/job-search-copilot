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
