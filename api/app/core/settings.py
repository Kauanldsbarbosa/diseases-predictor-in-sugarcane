import os

from dotenv import load_dotenv

from app.core.settingEnv.base import BaseEnvironment
from app.core.settingEnv.dev import DevSettings
from app.core.settingEnv.local import LocalSettings
from app.core.settingEnv.prod import ProductionSettings
from app.core.settingEnv.test import TestingSettings

load_dotenv()


def get_settings() -> BaseEnvironment:
    env = os.getenv("ENVIRONMENT", "local").lower()

    if env == "prod":
        return ProductionSettings()
    elif env == "dev":
        return DevSettings()
    elif env == "test":
        return TestingSettings()
    else:
        return LocalSettings()


settings = get_settings()
