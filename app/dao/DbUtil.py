"""
数据库常用操作
"""
import traceback

from sqlalchemy import text

from app import db


def create_sql_where_like_statement(key, value):
    """
    创建 SQL LIKE 语句
    eg:
        key = name, value = "xxx"
        return "name LIKE '%xxx%'"
    :param key: 字段名
    :param value: 匹配值
    :return: LIKE语句
    """
    return "%s LIKE '%%%s%%'" % (key, value)


def create_sql_where_eq_statement(key, value):
    """
    创建 SQL = 语句
    eg:
        key = name, value = "xxx"
        return "name = 'xxx'"
    :param key: 字段名
    :param value: 匹配值
    :return: 等值语句
    """
    return "%s = '%s'" % (key, value)


def create_sql_where_is_statement(key, value):
    """
    创建 SQL is 语句
    is 语句仅支持 is null, is not null
    eg:
        key = name, value = "xxx"
        return "name is NULL"
    :param key: 字段名
    :param value: null or not null
    :return: is语句
    """
    if value.upper() != "NULL" and value.upper() != 'NOT NULL':
        return ""
    return "%s is %s" % (key, value)


def and_sql_statement(statement, clause):
    if statement is None or statement == "":
        return clause
    return statement + " and " + clause


def or_sql_statement(statement, clause):
    if statement is None or statement == "":
        return clause
    return statement + " or " + clause


def add_conditions(cls, conditions_dict):
    """
    为query添加查询条件
    出错时，不会添加查询条件, 直接返回query

    :param cls: db.Model 的子类
    :param conditions_dict: 字典格式, 如 {"name" : "xxx", "gender": "1"}
    :return:
    """
    if not issubclass(cls, db.Model):
        raise Exception("cls 不是db.Model的子类")
    if conditions_dict is None or not isinstance(conditions_dict, dict) or len(conditions_dict) <= 0:
        return cls.query
    if not hasattr(cls, 'IS_COLUMNS'):
        raise Exception("cls 中未定义属性：IS_COLUMNS")
    if not hasattr(cls, 'EQ_COLUMNS'):
        raise Exception("cls 中未定义属性：EQ_COLUMNS")
    if not hasattr(cls, 'LIKE_COLUMNS'):
        raise Exception("cls 中未定义属性：LIKE_COLUMNS")

    try:
        # 开始拼接sql的where语句
        where_statement = ""
        for key, value in conditions_dict.items():
            if hasattr(cls, key) and value is not None and value != "":      # 加一层判断: 判断传入的条件字段是否是表中的某一个字段
                if (str(value).upper() == 'NULL' or str(value).upper() == 'NOT NULL') \
                        and key in cls.IS_COLUMNS:
                    clause = create_sql_where_is_statement(key, value)
                else:
                    if key in cls.LIKE_COLUMNS:
                        clause = create_sql_where_like_statement(key, value)
                    else:
                        clause = create_sql_where_eq_statement(key, value)
                where_statement = and_sql_statement(where_statement, clause)
            else:
                # 走到这里的话，检查客户端传入的conditions字段
                print("表中没有该字段: %r[走到这里的话，检查客户端传入的conditions字段]" % key)

        # 使用sqlalchemy框架提供的text() 方法格式化 自己拼成的sql语句
        where_statement = text(where_statement)

        # 为查询添加上条件，并返回
        return cls.query.filter(where_statement)
    except:
        traceback.print_exc()
        return cls.query
