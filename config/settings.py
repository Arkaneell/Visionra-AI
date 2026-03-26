from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Groq
    groq_api_key: str = Field(..., env="GROQ_API_KEY")
    groq_model: str = Field("llama3-70b-8192", env="GROQ_MODEL")
    groq_temperature: float = Field(0.7, env="GROQ_TEMPERATURE")
    groq_max_tokens: int = Field(2048, env="GROQ_MAX_TOKENS")

    # Agent
    agent_max_iterations: int = Field(10, env="AGENT_MAX_ITERATIONS")
    agent_verbose: bool = Field(True, env="AGENT_VERBOSE")

    # Memory
    session_history_limit: int = Field(20, env="SESSION_HISTORY_LIMIT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton — import this throughout the project
settings = Settings()
