from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg://hub:hub@localhost:5432/hub"
    cors_origins: str = "http://localhost:3001"
    # "dev" lets every request through as an admin. Switch to "cognito" before real data.
    auth_mode: str = "dev"
    retell_api_key: str = ""
    monthly_budget_usd: float = 2000.0
    clinic_timezone: str = "America/Chicago"
    office_open_hour: int = 8
    office_close_hour: int = 17


settings = Settings()
