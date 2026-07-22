from .base import BaseEnvironment


class LocalSettings(BaseEnvironment):
    DEBUG = True
    PROJECT_NAME = 'Sugarcane Disease Predictor API Local'
