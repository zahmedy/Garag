from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = "dev"

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    DATABASE_URL: str
    REDIS_URL: str

    JWT_SECRET: str
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 30

    OPENSEARCH_URL: str
    OPENSEARCH_INDEX: str = "garag_cars"

    S3_ENDPOINT_URL: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET: str
    S3_PUBLIC_BASE_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()