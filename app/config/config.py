import os

class Config:
    CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
    CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')
    ROOM_TRANSACTION_URL = os.environ.get('ROOM_TRANSACTION_URL')
    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'INFO'

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    LOG_LEVEL = 'WARNING'

config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}