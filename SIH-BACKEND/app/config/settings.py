"""
Configuration module for The Odyssey backend.

Loads settings from environment variables or a .env file at the repo root.
All application-level constants that may differ per environment live here.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application metadata
    app_title: str = "The Odyssey Backend"
    app_description: str = (
        "Backend API for freight forecasting and charter optimization "
        "for bulk cargo procurement to India's East Coast ports."
    )
    api_version: str = "v1"
    api_prefix: str = "/api/v1"

    # CORS — only the Vite dev server origins; extend for production deployment
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # Auth
    secret_key: str = "placeholder_secret_replace_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# Singleton instance imported by other modules
settings = Settings()
