## 数据库管理(MySql + PyMySQL + Alembic)
>使用Alembic进行数据库迁移升级管理

本文档包含以下内容：
1. 搭建数据库环境
2. 安装数据库操作相关的flask扩展
3. 创建数据库
4. Alembic托管数据库管理: alembic初始化
5. 修改alembic.ini配置文件[第4步生成]
6. 修改alembic生成的env.py[第4步生成]
7. 生成数据库迁移升级脚本
8. 升级数据库
9. 附：生成迁移脚本，并手动添加要修改的内容

>注：
>1. 首次搭建时，按照以上1-8依序操作(**仅需执行一次**)
>2. 以后每次修改了表结构，都需要进行数据库升级，依序执行7,8步骤即可
>3. 修改表结构时，尽量避免重命名已存在的字段
>4. 定期备份数据库

### 1. 搭建数据库环境
1. 在服务器上安装MySql数据库
2. 开放对外端口（判断是否已经开放）
3. 设置数据库默认字符集为UTF-8
4. 创建非root用户和密码

### 2. 安装数据库操作相关的flask扩展
1. 安装数据库ORM框架: flask-sqlalchemy

		命令行[先激活虚拟环境]: pip3 install flask-sqlalchemy
		PyCharm[IDE]: Setting->Project:xxx -> Project Interpreter: 添加扩展->输入：flask-sqlalchemy
	
2. 安装数据库迁移扩展: alembic

		命令行[先激活虚拟环境]:pip3 install alembic
		PyCharm[IDE]: Setting->Project:xxx -> Project Interpreter: 添加扩展->输入：alembic

3. 安装python驱动mysql的驱动: PyMySql

		命令行[先激活虚拟环境]: pip3 install PyMySQL
		PyCharm[IDE]: Setting->Project:xxx -> Project Interpreter: 添加扩展->输入：PyMySql

### 3. 创建数据库
因为我们使用的是MySql数据库，项目通过驱动程序连接数据库时，数据库必须存在，所以需要我们先在服务器上通过mysql语句创建数据库

	create database xxxxx;
	
### 4. Alembic托管数据库管理: alembic初始化
与 Git 类似，使用 Alembic 前需要通过 alembic init 命令创建一个 alembic 项目，该命令创建一个 alembic.ini 配置文件和一个 alembic 档案目录（将要创建的目录名）。在合适的位置运行

	alembic init migrations

此时，工程中生成alembic工具创建的必要文件和目录

在本项目的大致结构为:(在db_repository目录下初始化)
```text
RLink/
|--app
|--...
|--db_repository/
   |--__init__.py
   |--...
   |--alembic.ini            # 配置文件
   |--migrations/
      |--env.py              # 运行alembic会加载该模块
      |--script.py.mako      # 迁移脚本生成模板
      |--...
      |--versions/           # 存放迁移脚本，类似历史库
         |--3512b954651e_create_tables.py
         |--2b1ae634e5cd_add_order_id.py
         |--3adcc9a56557_rename_username_field.py
         |--...
```

附：[Alembic官网教程](http://alembic.zzzcomputing.com/en/latest/tutorial.html)

### 5. 修改alembic.ini配置文件[第4步生成]
```ini
sqlalchemy.url = driver://user:pass@localhost:port/dbname
# 修改成:
sqlalchemy.url = mysql+pymysql://root:''@127.0.0.1:3306/rlink
```

### 6. 修改alembic生成的env.py[第4步生成]
具体参考: [example](alembic_env_example.py) 中的FIXME部分
```text
找到：
target_metadata = None
修改成：
import os
import sys
from sqlalchemy import create_engine
# 定位到app目录
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "\\..\\")
from app import db, app
target_metadata = db.metadata

添加方法：
def get_url():
    return app.config['SQLALCHEMY_DATABASE_URI']
    或者:
    return "mysql+pymysql://%s:%s@%s/%s" % (
        os.getenv("DB_USER", "rlink"),
        os.getenv("DB_PASSWORD", "123456"),
        os.getenv("DB_HOST", "127.0.0.1"),
        os.getenv("DB_NAME", "rlink"),
    )
    
修改方法：
1. def run_migrations_offline():
	该方法中的url = config.get_main_option("sqlalchemy.url") 改为 url = get_url()
2. def run_migrations_online():
	该方法中的：
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool)
    改为:
    connectable = create_engine(get_url())	# 需要导入 from sqlalchemy import create_engine
```
    
### 7. 生成数据库迁移升级脚本
切换到alembic.ini所在目录，用 alembic revision --autogenerate -m "升级日志" 命令来生成数据库迁移升级的脚本

> 升级日志起名约定：版本号_改动说明, 如："v1_create_tables"

	alembic revision --autogenerate -m "v1_create_tables" 
	
成功后，会生成对应的迁移文件，手动检查一下，是否有误，确保无误后，再进行下一步。

>有时可能修改字段名或者字段数据结构时，自动生成的脚本中并没有添加上，此时需要手动添加, 手动添加遵照: 附：生成迁移脚本，并手动添加要修改的内容

### 8. 升级数据库[将数据库更改内容真正应用到数据库，此时数据库才发生改变]
注：每次升级前，都要手动检查一下上一步生成的迁移文件是否正确,然后再升级
	alembic upgrade head
	
### 附：生成迁移脚本，并手动添加要修改的内容
	alembic revision -m "create account table"
成功后，会生成对应的迁移脚本，但是升级和降级操作为空，需手动添加

示例代码如下：具体参考[Alembic官网教程](http://alembic.zzzcomputing.com/en/latest/tutorial.html)
```python
def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
    )

def downgrade():
    op.drop_table('account')
```
