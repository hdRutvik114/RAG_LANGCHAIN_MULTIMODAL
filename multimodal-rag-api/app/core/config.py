from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Multimodal RAG API"
    environment: str = "development"
    # path to the application log file
    log_file: str = "logs/app.log"

    # Existing vector-store settings
    pinecone_api_key: str
    pinecone_index_name: str = "multimodal-rag-dense"

    # Neon Postgres settings
    database_url: str = ""
    database_url_pooled: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()