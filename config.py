import os
basedir = os.path.abspath(os.path.dirname(__file__))

# FIXME debug模式开启
DEBUG = True

# 正式数据库
if DEBUG:
    # 测试环境
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:''@127.0.0.1:3306/rlink'
else:
    # 生产环境
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://rlink:rlink422@127.0.0.1:3306/rlink'

# SQLALCHEMY_COMMIT_ON_TEARDOWN = True   # 自动提交
SQLALCHEMY_TRACK_MODIFICATIONS = True

# 数据库迁移文件保存路径
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
