"""
数据库常用操作
"""


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


def and_sql_statement(statement, clause):
    if statement is None or statement == "":
        return clause
    return statement + " and " + clause


def or_sql_statement(statement, clause):
    if statement is None or statement == "":
        return clause
    return statement + " or " + clause

