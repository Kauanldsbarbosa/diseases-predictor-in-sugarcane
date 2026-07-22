from os import getenv

from .base import BaseEnvironment


class DevSettings(BaseEnvironment):
    DEBUG = True
    DATABASE_URL = getenv('DATABASE_URL')
    PROJECT_NAME = 'Api-Startkit DEV'
