import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'thisismysecretkey'
    APP_LOCALE = 'en_EN'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_PATH = 'sqlite:///{}/data.sqlite'.format(basedir)
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_PATH

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
