from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multimodal RAG API"
    environment: str = "development"
    # path to the application log file
    log_file: str = "logs/app.log"
    pinecone_api_key: str
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()