from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4.1-mini"
    MAX_OPENAI_TOKENS: int = 800
    MAX_FILE_MB: int = 3

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
