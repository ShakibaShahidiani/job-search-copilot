from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = (
        "postgresql+psycopg://copilot:copilot@localhost:5432/job_search_copilot"
    )
    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
