from .base import BaseEnvironment


class TestingSettings(BaseEnvironment):
    DEBUG = False
    DATABASE_URL = "sqlite:///./test.db"
