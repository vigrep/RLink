"""
    请求访问保护层
防止恶意输入、SQL注入和无权限操作
"""
from flask import json, request, abort
from functools import wraps
from app.model import ActionCode, StatusCode, MsgCode
from app.model.ActionResult import ActionResult
import traceback
from flask_login import current_user

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
    ActionCode.GET_LINK_BY_ID,
    ActionCode.ADD_CATEGORY,
    ActionCode.DELETE_CATEGORY,
    ActionCode.UPDATE_CATEGORY,
    ActionCode.GET_CATEGORY,
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


# def administrator_required(func):
#     @wraps(func)
#     def decorated_view(*args, **kwargs):
#         if not current_user.is_authenticated or current_user.id != 1:
#             # 用户没有认证
#             return abort(401)
#         print("不是管理员")
#         return func(*args, **kwargs)
#     return decorated_view


def permission_required(permissions):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.can(permissions):
                abort(403)
            return func(*args, **kwargs)
        return decorated_view
    return decorator


# def operator_required(func):
#     return permission_required(Roles.get_administrator_permissions())(func)

def logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                print("warn %s" % func.__name__)
            return func(*args)
        return wrapper
    return decorator


