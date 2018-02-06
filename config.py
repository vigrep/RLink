"""
配置
"""
import os


# 基类
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'rlink422rsgzljjtt'
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


# 开发环境
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rlink:123456@127.0.0.1:3306/rlink?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_DEFAULT_SENDER = "yad2206@163.com"


# 测试服务器
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rlink:rlink422@127.0.0.1:3306/rlink?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


# 正式环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rlink:rlink422@127.0.0.1:3306/rlink?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

