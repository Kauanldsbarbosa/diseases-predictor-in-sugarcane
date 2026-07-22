from .base import BaseEnvironment


class TestingSettings(BaseEnvironment):
    DEBUG = False
    PROJECT_NAME = 'Sugarcane Disease Predictor API Test'
