from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """Environment settings"""

    GOOGLE_API_KEY: str
    OPENAI_API_KEY: str
    APP_ENV: str

    class Config:
        env_file = os.environ.get("ENV_FILE_PATH")
        extra = "allow"


env_settings = Settings()
