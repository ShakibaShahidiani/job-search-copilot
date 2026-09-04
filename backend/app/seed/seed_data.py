"""Deterministic development fixtures: 10 FICTIONAL sample AI/ML jobs.

These are NOT live vacancies. Companies, URLs, and postings are invented
sample data used only to exercise the ranking and preference-learning loop
for Milestone 1. `posted_date` is computed relative to seed-run time so
freshness scoring stays meaningful without the fixtures going stale.
"""

import datetime as dt
from dataclasses import dataclass, field

from app.models.enums import CompanyType, EmploymentType, SeniorityLevel, WorkModel

TODAY = dt.date.today()


@dataclass
class SeedJob:
    company: str
    title: str
    location: str
    work_model: WorkModel
    source_url: str
    direct_application_url: str
    posted_days_ago: int
    description: str
    required_skills: list[str]
    preferred_skills: list[str]
    experience_requirement: str
    language_requirements: str
    employment_type: EmploymentType
    role_family: str
    company_type: CompanyType
    seniority_level: SeniorityLevel
    domain: str
    required_tags: list[str]
    preferred_tags: list[str]
    dutch_required: bool = False
    seniority_blocker: bool = False

    @property
    def posted_date(self) -> dt.date:
        return TODAY - dt.timedelta(days=self.posted_days_ago)

    @property
    def technologies(self) -> list[str]:
        seen: list[str] = []
        for tag in self.required_tags + self.preferred_tags:
            if tag not in seen:
                seen.append(tag)
        return seen


SEED_JOBS: list[SeedJob] = [
    SeedJob(
        company="Northwind Cognition",
        title="Agentic AI Engineer",
        location="Amsterdam",
        work_model=WorkModel.HYBRID,
        source_url="https://example-fixtures.dev/northwind-cognition/jobs/agentic-ai-engineer",
        direct_application_url="https://example-fixtures.dev/northwind-cognition/apply/1",
        posted_days_ago=5,
        description=(
            "Build autonomous agent workflows that plan, call tools, and self-correct "
            "for enterprise customers. You will design multi-step agent orchestration, "
            "integrate LLM planning loops, and productionize agentic pipelines."
        ),
        required_skills=["Python", "LLM-based agent design", "Model orchestration", "FastAPI"],
        preferred_skills=["RAG", "Docker", "AWS"],
        experience_requirement="2-4 years",
        language_requirements="English required, Dutch is a plus",
        employment_type=EmploymentType.FULL_TIME,
        role_family="agentic_ai_engineer",
        company_type=CompanyType.PRODUCT,
        seniority_level=SeniorityLevel.MEDIOR,
        domain="general_ai",
        required_tags=["python", "agentic_ai", "llm", "orchestration", "fastapi"],
        preferred_tags=["rag", "docker", "aws"],
    ),
    SeedJob(
        company="Veridian Health AI",
        title="Biomedical AI Engineer - Drug Discovery",
        location="Utrecht",
        work_model=WorkModel.HYBRID,
        source_url="https://example-fixtures.dev/veridian-health-ai/jobs/biomedical-ai-engineer",
        direct_application_url="https://example-fixtures.dev/veridian-health-ai/apply/2",
        posted_days_ago=10,
        description=(
            "Apply graph-based machine learning to gene-drug interaction and target "
            "discovery problems. Work with biomedical knowledge graphs, wet-lab "
            "collaborators, and production ML pipelines for early-stage drug discovery."
        ),
        required_skills=["Python", "Graph ML", "Knowledge graphs", "PyTorch"],
        preferred_skills=["Graph Neural Networks", "Bioinformatics"],
        experience_requirement="2-5 years",
        language_requirements="English only",
        employment_type=EmploymentType.FULL_TIME,
        role_family="biomedical_ai_engineer",
        company_type=CompanyType.PRODUCT,
        seniority_level=SeniorityLevel.MEDIOR,
        domain="biomedical",
        required_tags=["python", "graph_ml", "knowledge_graph", "pytorch"],
        preferred_tags=["gnn", "bioinformatics"],
    ),
    SeedJob(
        company="Aether Labs",
        title="LLM Engineer",
        location="Remote (NL)",
        work_model=WorkModel.REMOTE,
        source_url="https://example-fixtures.dev/aether-labs/jobs/llm-engineer",
        direct_application_url="https://example-fixtures.dev/aether-labs/apply/3",
        posted_days_ago=3,
        description=(
            "Own the retrieval-augmented generation stack for our developer-tools "
            "product: chunking, embeddings, vector search, and grounded answer "
            "generation with citation and abstention behavior."
        ),
        required_skills=["Python", "LLM engineering", "RAG", "Vector search"],
        preferred_skills=["Guardrails / hallucination mitigation", "LLM evaluation", "ChromaDB"],
        experience_requirement="2-4 years",
        language_requirements="English required",
        employment_type=EmploymentType.FULL_TIME,
        role_family="llm_engineer",
        company_type=CompanyType.PRODUCT,
        seniority_level=SeniorityLevel.MEDIOR,
        domain="general_ai",
        required_tags=["python", "llm", "rag", "vector_db"],
        preferred_tags=["guardrails", "llm_eval", "chromadb"],
    ),
    SeedJob(
        company="Deltaworks Consulting",
        title="Data Scientist - ML Systems",
        location="Amsterdam",
        work_model=WorkModel.HYBRID,
        source_url="https://example-fixtures.dev/deltaworks-consulting/jobs/data-scientist-ml",
        direct_application_url="https://example-fixtures.dev/deltaworks-consulting/apply/4",
        posted_days_ago=20,
        description=(
            "Deliver ML systems for a rotating portfolio of client engagements: "
            "forecasting, classification, and MLOps pipelines across industries."
        ),
        required_skills=["Python", "MLOps", "scikit-learn", "XGBoost"],
        preferred_skills=["AWS", "Docker"],
        experience_requirement="3-5 years",
        language_requirements="Dutch is a plus",
        employment_type=EmploymentType.FULL_TIME,
        role_family="data_scientist",
        company_type=CompanyType.CONSULTANCY,
        seniority_level=SeniorityLevel.MEDIOR,
        domain="general_ai",
        required_tags=["python", "mlops", "sklearn", "xgboost"],
        preferred_tags=["aws", "docker"],
    ),
    SeedJob(
        company="Brainport Robotics",
        title="Machine Learning Engineer",
        location="Eindhoven",
        work_model=WorkModel.ONSITE,
        source_url="https://example-fixtures.dev/brainport-robotics/jobs/ml-engineer",
        direct_application_url="https://example-fixtures.dev/brainport-robotics/apply/5",
        posted_days_ago=15,
        description=(
            "Train and deploy perception and control models for industrial robotics "
            "at our High Tech Campus site. Junior-friendly with strong mentorship."
        ),
        required_skills=["Python", "PyTorch", "MLOps"],
        preferred_skills=["AWS", "Docker", "Kubernetes"],
        experience_requirement="0-2 years",
        language_requirements="English required",
        employment_type=EmploymentType.FULL_TIME,
        role_family="ml_engineer",
        company_type=CompanyType.PRODUCT,
        seniority_level=SeniorityLevel.JUNIOR,
        domain="general_ai",
        required_tags=["python", "pytorch", "mlops"],
        preferred_tags=["aws", "docker", "kubernetes"],
    ),
    SeedJob(
        company="Cascade Partners",
        title="AI Platform Engineer",
        location="Eindhoven",
        work_model=WorkModel.HYBRID,
        source_url="https://example-fixtures.dev/cascade-partners/jobs/ai-platform-engineer",
        direct_application_url="https://example-fixtures.dev/cascade-partners/apply/6",
        posted_days_ago=40,
        description=(
            "Build and operate the ML platform (training infra, deployment, "
            "observability) used across client AI engagements."
        ),
        required_skills=["Python", "Kubernetes", "Cloud deployment", "MLOps"],
        preferred_skills=["AWS", "Terraform", "GitHub Actions"],
        experience_requirement="3-6 years",
        language_requirements="English required",
        employment_type=EmploymentType.FULL_TIME,
        role_family="ai_platform_engineer",
        company_type=CompanyType.CONSULTANCY,
        seniority_level=SeniorityLevel.MEDIOR,
        domain="general_ai",
        required_tags=["python", "kubernetes", "cloud", "mlops"],
        preferred_tags=["aws", "terraform", "github_actions"],
    ),
    SeedJob(
        company="Lumen NLP",
        title="NLP Engineer",
        location="Remote (EU)",
        work_model=WorkModel.REMOTE,
        source_url="https://example-fixtures.dev/lumen-nlp/jobs/nlp-engineer",
        direct_application_url="https://example-fixtures.dev/lumen-nlp/apply/7",
        posted_days_ago=8,
        description=(
            "Fine-tune and evaluate transformer-based NLP models for document "
            "classification and information extraction. Junior-friendly role."
        ),
        required_skills=["Python", "NLP", "Transformers"],
        preferred_skills=["PyTorch", "LLM engineering"],
        experience_requirement="0-2 years",
        language_requirements="English required",
        employment_type=EmploymentType.FULL_TIME,
        role_family="nlp_engineer",
        company_type=CompanyType.PRODUCT,
        seniority_level=SeniorityLevel.JUNIOR,
        domain="nlp",
        required_tags=["python", "nlp", "transformers"],
        preferred_tags=["pytorch", "llm"],
    ),
    SeedJob(
        company="Helix Genomics",
        title="Bioinformatics ML Engineer",
        location="Utrecht",
        work_model=WorkModel.HYBRID,
        source_url="https://example-fixtures.dev/helix-genomics/jobs/bioinformatics-ml-engineer",
        direct_application_url="https://example-fixtures.dev/helix-genomics/apply/8",
        posted_days_ago=12,
        description=(
            "Build ML pipelines over genomic and proteomic data, including graph-based "
            "representations of biological interaction networks."
        ),
        required_skills=["Python", "Bioinformatics", "Graph ML"],
        preferred_skills=["Graph Neural Networks", "Knowledge graphs", "SQL"],
        experience_requirement="2-4 years",
        language_requirements="English required",
        employment_type=EmploymentType.FULL_TIME,
        role_family="bioinformatics_ml_engineer",
        company_type=CompanyType.PRODUCT,
        seniority_level=SeniorityLevel.MEDIOR,
        domain="biomedical",
        required_tags=["python", "bioinformatics", "graph_ml"],
        preferred_tags=["gnn", "knowledge_graph", "sql"],
    ),
    SeedJob(
        company="Orion Applied AI",
        title="Applied AI Engineer",
        location="Utrecht",
        work_model=WorkModel.HYBRID,
        source_url="https://example-fixtures.dev/orion-applied-ai/jobs/applied-ai-engineer",
        direct_application_url="https://example-fixtures.dev/orion-applied-ai/apply/9",
        posted_days_ago=4,
        description=(
            "Ship applied GenAI features end-to-end: FastAPI services, RAG-backed "
            "assistants, and production LLM integrations for B2B customers."
        ),
        required_skills=["Python", "FastAPI", "RAG", "LLM integration"],
        preferred_skills=["PostgreSQL", "Docker", "AWS", "SQL"],
        experience_requirement="2-4 years",
        language_requirements="English required",
        employment_type=EmploymentType.FULL_TIME,
        role_family="applied_ai_engineer",
        company_type=CompanyType.PRODUCT,
        seniority_level=SeniorityLevel.MEDIOR,
        domain="general_ai",
        required_tags=["python", "fastapi", "rag", "llm"],
        preferred_tags=["postgresql", "docker", "aws", "sql"],
    ),
    SeedJob(
        company="Fortress Dynamics",
        title="Senior Machine Learning Engineer",
        location="Amsterdam",
        work_model=WorkModel.HYBRID,
        source_url="https://example-fixtures.dev/fortress-dynamics/jobs/senior-ml-engineer",
        direct_application_url="https://example-fixtures.dev/fortress-dynamics/apply/10",
        posted_days_ago=25,
        description=(
            "Lead a team of ML engineers delivering large-scale training "
            "infrastructure. Requires extensive leadership experience."
        ),
        required_skills=["Python", "PyTorch", "MLOps", "Kubernetes", "Team leadership"],
        preferred_skills=["AWS"],
        experience_requirement="7+ years, team leadership required",
        language_requirements="Dutch fluency mandatory",
        employment_type=EmploymentType.FULL_TIME,
        role_family="ml_engineer",
        company_type=CompanyType.PRODUCT,
        seniority_level=SeniorityLevel.SENIOR,
        domain="general_ai",
        required_tags=["python", "pytorch", "mlops", "kubernetes"],
        preferred_tags=["aws"],
        dutch_required=True,
        seniority_blocker=True,
    ),
]
