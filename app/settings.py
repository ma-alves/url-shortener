from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str
    secret_key: str
    postgres_db: str
    postgres_user: str
    postgres_password: str
    redis_host: str
    redis_port: int
    redis_db: int
