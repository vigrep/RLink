from sqlalchemy import func
from app import db
from app.utils import Utils


# 用户表
class User(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.INT, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.VARCHAR(20), nullable=False, index=True)
    password = db.Column(db.CHAR(32), nullable=False)
    gender = db.Column(db.CHAR(1), nullable=True)
    birth = db.Column(db.DATE, nullable=True)
    nickname = db.Column(db.VARCHAR(20), nullable=True)
    avatar = db.Column(db.VARCHAR(300), nullable=True)
    introduce = db.Column(db.VARCHAR(100), nullable=True)
    email = db.Column(db.VARCHAR(50), nullable=True)
    phone = db.Column(db.VARCHAR(11), nullable=True)
    register_datetime = db.Column(db.DATETIME, nullable=False, server_default=func.now())
    login_count = db.Column(db.INT, nullable=False, server_default="0")
    last_login_datetime = db.Column(db.DATETIME, nullable=True)
    bonus = db.Column(db.INT, nullable=False, server_default="100")     # 积分

    # 保存到数据库中
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    # 更新
    def update(self):
        db.session.commit()
        return self

    # 查询该用户保存的所有链接, 排序规则：递减
    def shared_links(self):
        return Link.query.filter(Link.user_id == self.id).order_by(Link.datetime.desc())

    # 将对象封装成字典格式，方便json化
    def json(self):
        return Utils.to_json(self, self.__class__)

    def __repr__(self):
        return '<User %r>' % self.json()


# 链接表
class Link(db.Model):
    __tablename__ = 'tb_link'
    id = db.Column(db.INT, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.VARCHAR(20), nullable=False, index=True)
    link = db.Column(db.VARCHAR(300), nullable=False, index=True)

    user_id = db.Column(db.INT, db.ForeignKey('tb_user.id'), nullable=False, index=True)
    category_id = db.Column(db.INT, db.ForeignKey('tb_category.id'), nullable=False, index=True)

    add_datetime = db.Column(db.DATETIME, nullable=False, server_default=func.now(), index=True)
    update_datetime = db.Column(db.DATETIME, nullable=False, onupdate=func.now(), index=True)
    description = db.Column(db.VARCHAR(100), nullable=True, index=True)

    link_icon_id = db.Column(db.INT, db.ForeignKey('tb_icon.id'), nullable=True, index=False)
    link_check_state = db.Column(db.SMALLINT, nullable=False, server_default="0", index=True)
    complaints_count = db.Column(db.INT, nullable=False, server_default="0", index=True)

    # expand1 = db.Column(db.VARCHAR(100), nullable=True)
    # expand2 = db.Column(db.VARCHAR(100), nullable=True)
    # expand3 = db.Column(db.VARCHAR(100), nullable=True)

    # 保存到数据库中
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    # 更新
    def update(self):
        db.session.commit()
        return self

    # 将对象封装成字典格式，方便json化
    def json(self):
        return Utils.to_json(self, self.__class__)

    def __repr__(self):
        return '<Link %r>' % self.json()


# 图标表
class Icon(db.Model):
    __tablename__ = 'tb_icon'
    id = db.Column(db.INT, primary_key=True, nullable=False, autoincrement=True)
    url = db.Column(db.VARCHAR(300), nullable=False)
    name = db.Column(db.VARCHAR(20), nullable=False)

    # 将对象封装成字典格式，方便json化
    def json(self):
        return Utils.to_json(self, self.__class__)

    def __repr__(self):
        return '<Icon %r-%r: %r>' % (self.id, self.name, self.url)


# 分类表
class Category(db.Model):
    __tablename__ = 'tb_category'
    id = db.Column(db.INT, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.VARCHAR(20), nullable=False)
    icon_id = db.Column(db.INT, db.ForeignKey('tb_icon.id'), nullable=True)

    # 将对象封装成字典格式，方便json化
    def json(self):
        return Utils.to_json(self, self.__class__)

    def __repr__(self):
        return '<Icon %r-%r: %r>' % (self.id, self.name, self.icon_id)

