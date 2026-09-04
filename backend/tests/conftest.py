import os

os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://copilot:copilot@localhost:5432/job_search_copilot_test"
)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models  # noqa: F401  (registers all tables on Base.metadata)
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.seed.seed import load_seed_jobs
from app.seed.seed_data import SEED_JOBS

engine = create_engine(os.environ["DATABASE_URL"], future=True)
TestSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


@pytest.fixture()
def db_session():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def seeded_db(db_session):
    load_seed_jobs(db_session)
    return db_session


@pytest.fixture()
def client(db_session):
    def _get_db_override():
        yield db_session

    app.dependency_overrides[get_db] = _get_db_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def seeded_client(seeded_db):
    def _get_db_override():
        yield seeded_db

    app.dependency_overrides[get_db] = _get_db_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def job_id_for(company: str) -> int:
    return next(i + 1 for i, j in enumerate(SEED_JOBS) if j.company == company)
