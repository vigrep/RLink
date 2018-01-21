from sqlalchemy import func
from app import db
from app.utils import Utils


# 用户表
class User(db.Model):
    __tablename__ = 'tb_user'
    id = db.Column(db.INT, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.VARCHAR(20), nullable=False, index=True)
    password = db.Column(db.String(128), nullable=False)
    # 性别
    gender = db.Column(db.CHAR(1), nullable=True)
    # 出生日期
    birth = db.Column(db.DATE, nullable=True)
    # 昵称
    nickname = db.Column(db.VARCHAR(20), nullable=True, index=True)
    # 头像
    avatar = db.Column(db.VARCHAR(300), nullable=True)
    # 自我介绍
    introduce = db.Column(db.VARCHAR(100), nullable=True)
    # 邮箱
    email = db.Column(db.VARCHAR(50), nullable=True)
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

    # 以下不对表结构产生影响
    # 定义查询规则
    LIKE_COLUMNS = ["name", "nickname"]
    EQ_COLUMNS = ["id", "gender"]
    # 下行代码作用：User.links 可以获取到属于该用户的所有链接, Link.user 可以获取到该链接所有者的信息
    # links = db.relationship('Link', backref=db.backref('user'))

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
    # 定义查询规则
    LIKE_COLUMNS = ["name"]
    EQ_COLUMNS = ["id"]

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

