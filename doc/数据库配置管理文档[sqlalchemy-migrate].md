## 数据库管理(MySql + PyMySQL + sqlalchemy-migrate)
> 注：该工程已不使用该方式管理数据库，废弃
>
> 推荐使用：[通过MySql + PyMySQL + alembic方式管理数据库](./数据库配置管理文档%5Balembic%5D.md)

本文档包含以下内容：
1. 搭建数据库环境
2. 安装数据库操作相关的flask扩展
3. 创建数据库
4. 创建表
5. 数据库迁移
6. 数据库升级

>注：
>1. 首次搭建时，按照以上1-6依序操作(**仅需执行一次**)
>2. 以后每次修改了表结构，都需要进行数据库升级，依序执行5,6步骤即可
>3. 修改表结构时，尽量避免重命名已存在的字段(sqlalchemy-migrate对此支持不好)
>4. 定期备份数据库

### 1. 搭建数据库环境
1. 在服务器上安装MySql数据库
2. 开放对外端口（判断是否已经开放）
3. 设置数据库默认字符集为UTF-8
4. 创建非root用户和密码

### 2. 安装数据库操作相关的flask扩展
1. 安装数据库ORM框架: flask-sqlalchemy

		命令行: pip3 install flask-sqlalchemy
		PyCharm[IDE]: Setting->Project:xxx -> Project Interpreter: 添加扩展->输入：flask-sqlalchemy
	
2. 安装数据库迁移扩展:sqlalchemy-migrate

		命令行:pip3 install sqlalchemy-migrate[需先安装pbr: pip3 install pbr]
		PyCharm[IDE]: Setting->Project:xxx -> Project Interpreter: 添加扩展->输入：qlalchemy-migrate

3. 安装python驱动mysql的驱动: PyMySql

		命令行: pip3 install PyMySQL
		PyCharm[IDE]: Setting->Project:xxx -> Project Interpreter: 添加扩展->输入：PyMySql

### 3. 创建数据库
因为我们使用的是MySql数据库，项目通过驱动程序连接数据库时，数据库必须存在，所以需要我们先在服务器上通过mysql语句创建数据库

	create database xxxxx;
	
### 4. 创建表
Flask-sqlalchemy会根据Model去创建表，如果存在，就不在去创建
1. 在项目根目录下的config.py 中配置数据库URI、数据库迁移路径等配置参数
2. 在app/model/Models.py 中添加表结构
3. 运行脚本：db_create.py
>运行成功：
>1. 数据库中已经生成了表，检查一下
>2. 项目中生成了数据库迁移升级目录和相关文件，不可删除

### 5. 数据库迁移
运行脚本：db_migrate.py
>运行成功：输出当前数据库版本

### 6. 数据库升级
运行脚本：db_upgrade.py
>运行成功：输出当前数据库版本

### 7. MySQL相关指令
- 查看表结构(包含索引信息)：desc tb_user;
- 创建数据库本地用户: grant all on *.* to rlink@'localhost' identified by "123456";
- 创建数据库远程用户: grant all on *.* to rlink@'%' identified by "123456";
