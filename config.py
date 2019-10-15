from os import getenv

BLACKLIST = set()

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'NadaAlemDeNada'
    JWT_BLACKLIST_ENABLED = True
    SECRET_KEY = getenv('SECRET_KEY') or 'NadaAlemdeNada'
    APP_PORT = int(getenv('APP_PORT'))
    DEBUG = eval(getenv('DEBUG').title())

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI')
    FLASK_ENV = 'development'
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///banco.db'

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}