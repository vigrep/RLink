from app import db
from datetime import datetime
from app import Utils


class User(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.INT, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.VARCHAR(20), nullable=False)
    password = db.Column(db.CHAR(32), nullable=False)
    gender = db.Column(db.CHAR(1), nullable=True)
    birth = db.Column(db.DATE, nullable=True)
    nickname = db.Column(db.VARCHAR(20), nullable=True)
    avatar = db.Column(db.VARCHAR(300), nullable=True)
    introduce = db.Column(db.VARCHAR(100), nullable=True)
    email = db.Column(db.VARCHAR(50), nullable=True)
    phone = db.Column(db.VARCHAR(11), nullable=True)
    register_datetime = db.Column(db.DATETIME, nullable=False, default=datetime.now)
    login_count = db.Column(db.INT)
    last_login_datetime = db.Column(db.DATETIME)

    # 将对象封装成字典格式，方便json化
    def json(self):
        return Utils.to_json(self, self.__class__)

    def __repr__(self):
        return '<User %r>' % self.name


