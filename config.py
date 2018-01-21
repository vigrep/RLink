import os
basedir = os.path.abspath(os.path.dirname(__file__))

# FIXME debug模式开启
DEBUG = True

# 正式数据库
if DEBUG:
    # 测试环境
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rlink:123456@127.0.0.1:3306/rlink?charset=utf8'
else:
    # 生产环境
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rlink:rlink422@127.0.0.1:3306/rlink?charset=utf8'

# SQLALCHEMY_COMMIT_ON_TEARDOWN = True   # 自动提交
SQLALCHEMY_TRACK_MODIFICATIONS = True
