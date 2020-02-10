import os
from datetime import timedelta


class Config(object):
    # Server
    HOST = "0.0.0.0"
    PORT = 5050

    # JWT
    SECRET_KEY = "apiserver is porwered by xmetadata"
    JWT_EXPIRATION_DELTA = timedelta(weeks=1)
    JWT_AUTH_URL_RULE = '/apiserver/v1.0/auth'


class ProductionConfig(Config):
    # Server
    DEBUG = True

    # MySQL
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Aa888888@47.103.36.82:3306/cd_heatmap?charset=utf8'


class DevelopmentConfig(Config):
    # Server
    DEBUG = True

    # SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///%s/data/databases.db' % os.path.dirname(
        os.path.realpath(__file__))
