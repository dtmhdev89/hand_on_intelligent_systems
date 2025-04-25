from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    """Environment settings"""

    APP_ENV: str
    TELEGRAM_API_KEY: str
    TELEGRAM_BOT_USERNAME: str
    GOOGLE_API_KEY: str

    class Config:
        env_file = os.environ.get("ENV_FILE_PATH")
        extra = "allow"


env_settings = Settings()
