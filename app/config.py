# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    MODEL_NAME: str = "llama3-8b-8192"  # default model

    class Config:
        env_file = ".env"
        extra = "ignore" # resolves error

settings = Settings()