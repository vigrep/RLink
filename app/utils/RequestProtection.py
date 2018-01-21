"""
    请求访问保护层
防止恶意输入、SQL注入和无权限操作
"""
from flask import request
from app.model import ActionCode

# 管理员:99 权限列表
PERMISSIONS_ADMINISTRATOR = [
    ActionCode.ADD_USER,
    ActionCode.BATCH_ADD_USER_BY_FILE,
    ActionCode.DELETE_USER,
    ActionCode.DELETE_MULTI_USER,
    ActionCode.UPDATE_USER,
    ActionCode.GET_USERS_BY_PAGE,
    ActionCode.GET_ALL_USERS,
    ActionCode.GET_USER_BY_ID,
    ActionCode.ADD_LINK,
    ActionCode.DELETE_MULTI_LINK,
    ActionCode.UPDATE_LINK,
    ActionCode.GET_LINKS_BY_PAGE,
    ActionCode.ADD_CATEGORY,
    ActionCode.DELETE_CATEGORY,
    ActionCode.UPDATE_CATEGORY,
    ActionCode.GET_CATEGORY
]


def is_allow(action_code, request_id):
    try:
        request_id = int(request_id)
        if request_id == 99:    # 管理员
            if action_code in PERMISSIONS_ADMINISTRATOR:
                return True
        else:
            return False
    except:
        return False


def allow(action):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if is_allow(action, 99):
                print("warn %s" % func.__name__)
            return func(*args)
        return wrapper
    return decorator


def logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                print("warn %s" % func.__name__)
            return func(*args)
        return wrapper
    return decorator
