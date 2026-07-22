from .base import BaseEnvironment


class DevSettings(BaseEnvironment):
    DEBUG = True
    PROJECT_NAME = 'Sugarcane Disease Predictor API DEV'
