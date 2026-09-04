"""Deterministic representation of the candidate, used only by
services/scoring.py to compute the one-time MatchScore for each seed job.

Every value here must trace back to a verified claim in context/CANDIDATE.md.
Kept as plain data (not parsed from the markdown) so scoring stays fast,
typed, and independent of prose formatting.
"""

# Demonstrated-evidence strength (0-1) per normalized technology tag.
# 1.0 = direct, well-evidenced professional/project experience.
# Lower values reflect partial, indirect, or unverified exposure.
DEMONSTRATED_EVIDENCE: dict[str, float] = {
    # Backend / infra (RAG Assistant, LLM Debate System, Corteva work)
    "python": 1.0,
    "fastapi": 1.0,
    "sqlalchemy": 1.0,
    "postgresql": 1.0,
    "docker": 1.0,
    "docker_compose": 1.0,
    "aws": 0.9,
    "terraform": 0.9,
    "github_actions": 0.9,
    "ci_cd": 0.9,
    "sql": 1.0,
    "numpy": 1.0,
    "pandas": 1.0,
    "streamlit": 1.0,
    # GenAI / LLM
    "rag": 1.0,
    "vector_db": 0.9,
    "chromadb": 1.0,
    "llm": 0.9,
    "llm_eval": 0.8,
    "guardrails": 1.0,
    "multi_agent": 0.9,
    "agentic_ai": 0.6,
    "orchestration": 0.55,
    "litellm": 0.9,
    "nlp": 0.8,
    "genai": 0.8,
    # ML / biomedical
    "pytorch": 1.0,
    "sklearn": 1.0,
    "transformers": 1.0,
    "gnn": 1.0,
    "graph_ml": 1.0,
    "knowledge_graph": 1.0,
    "cnn": 0.7,
    "lstm": 0.7,
    "random_forest": 1.0,
    "xgboost": 1.0,
    "bioinformatics": 0.9,
    "mlops": 0.5,
    "kubernetes": 0.2,
    "cloud": 0.8,
}

# Tags the candidate has touched at all (used for technical_fit overlap,
# independent of how strongly it's evidenced).
CANDIDATE_TECH_SKILLS: frozenset[str] = frozenset(DEMONSTRATED_EVIDENCE.keys())

# Tags considered "infrastructure" for infrastructure_fit.
INFRA_TAGS: frozenset[str] = frozenset(
    {
        "aws",
        "docker",
        "docker_compose",
        "terraform",
        "github_actions",
        "ci_cd",
        "kubernetes",
        "cloud",
        "postgresql",
        "fastapi",
    }
)

SENIORITY_FIT = {"junior": 1.0, "medior": 0.8, "senior": 0.25}

DOMAIN_FIT = {
    "biomedical": 1.0,
    "healthcare": 0.9,
    "nlp": 0.65,
    "general_ai": 0.6,
    "other": 0.4,
}

# Location priority per context/CONSTRAINTS.md geography ordering.
LOCATION_FIT = {
    "Utrecht": 1.0,
    "Amsterdam": 0.9,
    "Eindhoven": 0.75,
    "Rotterdam": 0.6,
    "Remote (NL)": 0.6,
    "Remote (EU)": 0.4,
}
DEFAULT_LOCATION_FIT = 0.5

# Role-family priority per context/TARGET_ROLES.md (A > C > B).
ROLE_FAMILY_TIER = {
    "agentic_ai_engineer": "A",
    "applied_ai_engineer": "A",
    "llm_engineer": "A",
    "ai_engineer": "A",
    "generative_ai_engineer": "A",
    "biomedical_ai_engineer": "C",
    "bioinformatics_ml_engineer": "C",
    "ml_engineer": "B",
    "data_scientist": "B",
    "nlp_engineer": "B",
    "ai_platform_engineer": "B",
}
CAREER_DIRECTION_FIT = {"A": 1.0, "C": 0.85, "B": 0.75}
DEFAULT_CAREER_DIRECTION_FIT = 0.3

# Human-readable labels for tags, used in top_matches / gap output.
TAG_LABELS: dict[str, str] = {
    "python": "Python",
    "fastapi": "FastAPI",
    "sqlalchemy": "SQLAlchemy",
    "postgresql": "PostgreSQL",
    "docker": "Docker",
    "docker_compose": "Docker Compose",
    "aws": "AWS",
    "terraform": "Terraform",
    "github_actions": "GitHub Actions CI/CD",
    "ci_cd": "CI/CD pipelines",
    "sql": "SQL",
    "numpy": "NumPy",
    "pandas": "Pandas",
    "streamlit": "Streamlit",
    "rag": "RAG pipelines",
    "vector_db": "Vector search",
    "chromadb": "ChromaDB",
    "llm": "LLM engineering",
    "llm_eval": "LLM evaluation",
    "guardrails": "Guardrails / hallucination mitigation",
    "multi_agent": "Multi-agent systems",
    "agentic_ai": "Agentic AI workflows",
    "orchestration": "Model orchestration",
    "litellm": "LiteLLM",
    "nlp": "NLP",
    "genai": "Generative AI",
    "pytorch": "PyTorch",
    "sklearn": "scikit-learn",
    "transformers": "Transformers",
    "gnn": "Graph Neural Networks",
    "graph_ml": "Graph ML",
    "knowledge_graph": "Knowledge graphs",
    "cnn": "CNNs",
    "lstm": "Bidirectional LSTMs",
    "random_forest": "Random Forest",
    "xgboost": "XGBoost",
    "bioinformatics": "Bioinformatics / biomedical data",
    "mlops": "MLOps",
    "kubernetes": "Kubernetes",
    "cloud": "Cloud deployment",
}
