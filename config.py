"""
Configuration management using Pydantic settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # AI Provider Selection
    AI_PROVIDER: str = "azure"  # Options: "azure", "digitalocean"
    
    # Azure OpenAI Configuration
    AZURE_OPENAI_ENDPOINT: str ="https://agent-ai-servicess2v7.openai.azure.com/"
    AZURE_OPENAI_API_KEY: str
    AZURE_OPENAI_MODEL: str = "gpt-4"
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    
    # DigitalOcean AI Configuration (optional, used when AI_PROVIDER="digitalocean")
    DIGITALOCEAN_INFERENCE_ENDPOINT: str = "https://inference.do-ai.run/v1"
    DIGITALOCEAN_API_KEY: str = ""
    DIGITALOCEAN_MODEL: str = "openai-gpt-4o"
    
    # Default System Prompt
    DEFAULT_SYSTEM_PROMPT: str = "You are a helpful AI assistant."
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # CORS Configuration
    CORS_ORIGINS: Union[str, List[str]] = "*"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    @field_validator('CORS_ORIGINS', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS from string or list"""
        if isinstance(v, str):
            if v == "*":
                return ["*"]
            # Handle comma-separated values
            return [origin.strip() for origin in v.split(",")]
        return v
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Create global settings instance
settings = Settings()
