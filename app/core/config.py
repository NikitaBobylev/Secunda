from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./secunda.db"
    async_database_url: str | None = None
    api_key: str = "changeme"
    log_path: str = "logs/app.log"
    pythonpath: str | None = None

    model_config = SettingsConfigDict(
        env_prefix="SECUNDA_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )

    def get_async_database_url(self) -> str:
        if self.async_database_url:
            return self.async_database_url
        if self.database_url.startswith("sqlite:///"):
            return self.database_url.replace("sqlite:///", "sqlite+aiosqlite:///")
        if self.database_url.startswith("postgresql://"):
            return self.database_url.replace("postgresql://", "postgresql+asyncpg://")
        return self.database_url


settings = Settings()
