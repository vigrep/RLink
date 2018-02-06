from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import config

db = SQLAlchemy()
lm = LoginManager()
lm.login_view = 'auth.login'
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 初始化
    db.init_app(app)
    lm.init_app(app)
    mail.init_app(app)

    # 注册蓝图
    from app.main import main
    app.register_blueprint(main)

    from app.admin import admin
    app.register_blueprint(admin, url_prefix='/admin')

    from app.auth import auth
    app.register_blueprint(auth)

    return app

