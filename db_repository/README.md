数据库管理目录，请勿删除

目录结构说明：
```text
|--db_repository/
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
