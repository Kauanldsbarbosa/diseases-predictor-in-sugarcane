from os import getenv

from .base import BaseEnvironment


class ProductionSettings(BaseEnvironment):
    DEBUG = False
    DATABASE_URL = getenv("DATABASE_URL")
