import traceback

from sqlalchemy import func
from sqlalchemy.sql import expression
from flask_login import UserMixin, AnonymousUserMixin
from app import db
from app.model.Permission import Permission
from app.utils import Utils
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from datetime import datetime
from app import lm


# 用户表
class User(UserMixin, db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.INT, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.VARCHAR(20), nullable=False, index=True, unique=True)
    password = db.Column(db.String(128), nullable=False)
    # 性别
    gender = db.Column(db.CHAR(1), nullable=True)
    # 出生日期
    birth = db.Column(db.DATE, nullable=True)
    # 昵称 FIXME need delete
    nickname = db.Column(db.VARCHAR(20), nullable=True, index=True, unique=True)
    # 头像
    avatar = db.Column(db.VARCHAR(300), nullable=True)
    # 自我介绍
    introduce = db.Column(db.VARCHAR(100), nullable=True)
    # 邮箱
    email = db.Column(db.VARCHAR(50), nullable=True, unique=True)
    # 联系电话
    phone = db.Column(db.VARCHAR(11), nullable=True)
    # 注册时间
    register_datetime = db.Column(db.DATETIME, nullable=False, server_default=func.now())
    # 登录次数
    login_count = db.Column(db.INT, nullable=False, server_default="0")
    # 最近一次登录时间戳
    last_login_datetime = db.Column(db.DATETIME, nullable=True)
    # 积分
    bonus = db.Column(db.INT, nullable=False, server_default="100")
    # 邮箱确认
    confirmed = db.Column(db.Boolean, server_default=expression.false())
    # 角色
    role_id = db.Column(db.INT,
                        db.ForeignKey('tb_role.id', onupdate='CASCADE', ondelete='SET NULL'),
                        nullable=True)
    # 通过该变量可以获取到该用户保存的所有链接
    # 下行代码作用：User.links 可以获取到属于该用户的所有链接, Link.author 可以获取到该链接所有者的信息
    links = db.relationship('Link', backref='author', lazy='dynamic')

    # 定义查询规则
    LIKE_COLUMNS = ["name", "nickname"]
    EQ_COLUMNS = ["id", "gender"]
    IS_COLUMNS = ["role_id"]

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm_email_account(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        self.save()
        return True

    # 通过字典为属性复制
    def setvalue(self, value_dict):
        for key, value in value_dict.items():
            if key == 'password':
                self.set_password(value)
            else:
                setattr(self, key, value)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # 保存到数据库中
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    # 更新
    def update(self, value_dict):
        if isinstance(value_dict, dict) and len(value_dict) > 0:
            try:
                for key, value in value_dict.items():
                    if key == 'password':
                        self.set_password(value)
                    else:
                        setattr(self, key, value)
                db.session.commit()
                return True
            except:
                return False
        return False

    # 签到，更新登录日期
    def dingding(self):
        self.last_login_datetime = datetime.now()
        self.save()

    def can(self, permissions):
        """
        是否有某项权限
        :param permissions:
        :return:
        """
        return self.role is not None and (self.role.permissions & permissions) == permissions

    # 查询该用户保存的所有链接, 排序规则：递减
    def shared_links(self):
        return Link.query.filter(Link.user_id == self.id).order_by(Link.datetime.desc())

    # 将对象封装成字典格式，方便json化
    def json(self):
        return Utils.to_json(self, self.__class__, ignore_list=['password'])

    # FIXME 完善
    def to_json(self):
        json_str = {
            "username": self.name,
            "introduce": self.introduce
        }
        return json_str

    def __repr__(self):
        return '<User %r>' % self.json()


# 匿名用户
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    # def is_administrator(self):
    #     return False


lm.anonymous_user = AnonymousUser


# flask-login 扩展要求 必须要提供的方法
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 链接表
class Link(db.Model):
    __tablename__ = 'tb_link'
    id = db.Column(db.INT, primary_key=True, nullable=False, autoincrement=True)
    # 链接标题
    name = db.Column(db.VARCHAR(20), nullable=False, index=True)
    # 链接URL
    link = db.Column(db.VARCHAR(300), nullable=False)
    # 添加者ID
    user_id = db.Column(db.INT,
                        db.ForeignKey('tb_user.id', onupdate='CASCADE', ondelete='SET NULL'),
                        nullable=True,
                        index=True)
    # 所属分类ID
    category_id = db.Column(db.INT,
                            db.ForeignKey('tb_category.id', onupdate='CASCADE', ondelete='SET NULL'),
                            nullable=True,
                            index=True)
    # 添加的时间戳
    add_datetime = db.Column(db.DATETIME, nullable=False, server_default=func.now(), index=True)
    # 最近一次修改的时间戳
    update_datetime = db.Column(db.DATETIME, nullable=False, server_default=func.now(), onupdate=func.now(), index=True)
    # 描述信息
    description = db.Column(db.VARCHAR(100), nullable=True, index=True)
    # 链接审核状态
    link_check_state = db.Column(db.SMALLINT, nullable=False, server_default="0", index=True)
    # 举报次数
    complaints_count = db.Column(db.INT, nullable=False, server_default="0", index=True)
    # 访问量
    visit_count = db.Column(db.INT, nullable=False, server_default="0", index=True)

    # expand1 = db.Column(db.VARCHAR(100), nullable=True)
    # expand2 = db.Column(db.VARCHAR(100), nullable=True)
    # expand3 = db.Column(db.VARCHAR(100), nullable=True)

    # 以下不对表结构产生影响
    # 定义查询规则
    LIKE_COLUMNS = ["name", "link", "description"]
    EQ_COLUMNS = ["id", "user_id", "category_id", "link_check_state"]
    IS_COLUMNS = ["user_id", "category_id"]

    # 通过字典为属性复制
    def setvalue(self, value_dict):
        self.__dict__.update(value_dict)

    # 保存到数据库中
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    # 更新
    def update(self, value_dict):
        if isinstance(value_dict, dict) and len(value_dict) > 0:
            try:
                for key, value in value_dict.items():
                    setattr(self, key, value)
                db.session.commit()
                return True
            except:
                return False
        return False
        # update_count = Link.query.filter(Link.id == link_id).update(link_dict)

    # 将对象封装成字典格式，方便json化
    def json(self):
        return Utils.to_json(self, self.__class__)

    def __repr__(self):
        return '<Link %r>' % self.json()


# 分类表
class Category(db.Model):
    __tablename__ = 'tb_category'
    id = db.Column(db.INT, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.VARCHAR(20), nullable=False)

    # 以下不对表结构产生影响
    links = db.relationship('Link', backref='category', lazy='dynamic')

    # 定义查询规则
    LIKE_COLUMNS = ["name"]
    EQ_COLUMNS = ["id"]
    IS_COLUMNS = []

    # 通过字典为属性复制
    def setvalue(self, value_dict):
        self.__dict__.update(value_dict)

    # 保存到数据库中
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    # 更新
    def update(self, value_dict):
        if isinstance(value_dict, dict) and len(value_dict) > 0:
            try:
                for key, value in value_dict.items():
                    setattr(self, key, value)
                db.session.commit()
                return True
            except:
                return False
        return False

    # 将对象封装成字典格式，方便json化
    def json(self):
        return Utils.to_json(self, self.__class__)

    def __repr__(self):
        return '<Category %r>' % self.json()


# 角色表
# 1. 普通用户
# 2. 操作员：可登录后台管理系统，仅开放链接管理权限
# 3. 系统管理员：开放所有权限
class Role(db.Model):
    __tablename__ = 'tb_role'
    id = db.Column(db.INT, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    permissions = db.Column(db.Integer)

    users = db.relationship('User', backref='role', lazy='dynamic')

    # 定义查询规则
    LIKE_COLUMNS = ["name"]
    EQ_COLUMNS = ["id", "permissions"]
    IS_COLUMNS = []

    # 通过字典为属性复制
    def setvalue(self, value_dict):
        self.__dict__.update(value_dict)

    # 保存到数据库中
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    # 更新
    def update(self, value_dict):
        if isinstance(value_dict, dict) and len(value_dict) > 0:
            try:
                for key, value in value_dict.items():
                    setattr(self, key, value)
                db.session.commit()
                return True
            except:
                return False
        return False

    # 将对象封装成字典格式，方便json化
    def json(self):
        role_dict = {
            "id": self.id,
            "name": self.name,
            "permissions": Permission.get_permissions(only=Permission.split_permission(self.permissions))
        }
        return role_dict
        # return Utils.to_json(self, self.__class__)

    def __repr__(self):
        return '<Role %r>' % self.json()


# 轮播图展示的链接
class PrimaryLink(db.Model):
    __tablename__ = 'tb_primary_link'
    id = db.Column(db.INT, primary_key=True, nullable=False, autoincrement=True)
    # 链接ID
    link_id = db.Column(db.INT,
                        db.ForeignKey('tb_link.id', onupdate='CASCADE', ondelete='CASCADE'),
                        nullable=False)
    img_url = db.Column(db.VARCHAR(100), nullable=True)
    add_datetime = db.Column(db.DATETIME, nullable=False, server_default=func.now())

    # 定义查询规则
    LIKE_COLUMNS = []
    EQ_COLUMNS = []
    IS_COLUMNS = []

    def get_url(self):
        link = Link.query.filter_by(id=self.link_id).first()
        if link is not None:
            return link.link
        return ""

    def get_img(self):
        return self.img_url

    @staticmethod
    def add_link(link_id):
        try:
            link = Link.query.filter_by(id=link_id).first()
            if link is not None:
                primary = PrimaryLink()
                primary.link_id = link.id
                db.session.add(primary)
                db.session.commit()
                return True
            return False
        except:
            return False

    @staticmethod
    def add_links(link_ids):
        try:
            links = Link.query.filter(Link.id.in_(link_ids)).all()
            if links is not None:
                for link in links:
                    primary = PrimaryLink()
                    primary.link_id = link.id
                    db.session.add(primary)
                db.session.commit()
                return True
            return False
        except:
            traceback.print_exc()
            return False

    @staticmethod
    def delete_links(primary_ids=list()):
        try:
            PrimaryLink.query.filter(PrimaryLink.id.in_(primary_ids)).delete(synchronize_session=False)
            db.session.commit()
            return True
        except:
            return False

    # 保存到数据库中
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

    # 更新
    def update(self, value_dict):
        if isinstance(value_dict, dict) and len(value_dict) > 0:
            try:
                for key, value in value_dict.items():
                    setattr(self, key, value)
                db.session.commit()
                return True
            except:
                return False
        return False

    # 将对象封装成字典格式，方便json化
    def json(self):
        return Utils.to_json(self, self.__class__)

    def __repr__(self):
        return '<PrimaryLink %r>' % self.json()


# 值得推荐的链接
class WorthyLink(db.Model):
    __tablename__ = 'tb_worthy_link'
    id = db.Column(db.INT, primary_key=True, nullable=False, autoincrement=True)
    # 链接ID
    link_id = db.Column(db.INT,
                        db.ForeignKey('tb_link.id', onupdate='CASCADE', ondelete='CASCADE'),
                        nullable=False)
    add_datetime = db.Column(db.DATETIME, nullable=False, server_default=func.now())

    def get_link(self):
        return Link.query.filter_by(id=self.link_id).first()

    @staticmethod
    def add_link(link_id):
        try:
            link = Link.query.filter_by(id=link_id).first()
            if link is not None:
                worthy = WorthyLink()
                worthy.link_id = link.id
                db.session.add(worthy)
                db.session.commit()
                return True
            return False
        except:
            return False

    @staticmethod
    def add_links(link_ids):
        try:
            links = Link.query.filter(Link.id.in_(link_ids)).all()
            if links is not None:
                for link in links:
                    worthy = WorthyLink()
                    worthy.link_id = link.id
                    db.session.add(worthy)
                db.session.commit()
                return True
            return False
        except:
            traceback.print_exc()
            return False

    @staticmethod
    def delete_links(worthy_ids=list()):
        try:
            WorthyLink.query.filter(WorthyLink.id.in_(worthy_ids)).delete(synchronize_session=False)
            db.session.commit()
            return True
        except:
            return False

    # 将对象封装成字典格式，方便json化
    def json(self):
        return Utils.to_json(self, self.__class__)

    def __repr__(self):
        return '<WorthyLink %r>' % self.json()
