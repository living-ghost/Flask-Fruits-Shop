import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abcdefghijk'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///sample.db'
    UPLOAD_FOLDER = 'static/uploads'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
    

class TestConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False


config = {

    'development' : DevConfig,
    'testing' : TestConfig,
    'production' : ProdConfig,
    'default' : DevConfig

}