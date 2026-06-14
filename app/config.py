import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class BaseConfig:
    APP_NAME = "KAIRON"
    TESTING = False
    DEBUG = False
    ENVIRONMENT = os.getenv("FLASK_ENV", os.getenv("KAIRON_ENV", "development"))
    DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'kairon.db'}")
    SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    JSON_SORT_KEYS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "kairon-dev-secret")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    ENVIRONMENT = "development"


class IntegrationConfig(BaseConfig):
    ENVIRONMENT = "integration"


class ProductionConfig(BaseConfig):
    ENVIRONMENT = "production"

    @classmethod
    def validate(cls):
        if cls.DATABASE_URL.startswith("sqlite"):
            raise RuntimeError("Production requires a PostgreSQL DATABASE_URL")


CONFIG_BY_ENV = {
    "development": DevelopmentConfig,
    "dev": DevelopmentConfig,
    "integration": IntegrationConfig,
    "pipeline": IntegrationConfig,
    "test": IntegrationConfig,
    "production": ProductionConfig,
    "prod": ProductionConfig,
}


def get_config():
    env = os.getenv("FLASK_ENV", os.getenv("KAIRON_ENV", "development")).lower()
    config_class = CONFIG_BY_ENV.get(env, DevelopmentConfig)
    validate = getattr(config_class, "validate", None)
    if callable(validate):
        validate()
    return config_class
