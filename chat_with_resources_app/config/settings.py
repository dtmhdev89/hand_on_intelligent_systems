from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Environment variables definition"""

    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_API_KEY: Optional[str] = None
    APP_ENV: Optional[str] = "development"

    class Config:
        """Specify config for settings"""

        env_file = os.environ.get("ENV_FILE_PATH")
        extra = "allow"
