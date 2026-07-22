from .base import BaseEnvironment


class ProductionSettings(BaseEnvironment):
    DEBUG = False
    PROJECT_NAME = 'Sugarcane Disease Predictor API Prod'
