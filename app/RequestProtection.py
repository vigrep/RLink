"""
    请求访问保护层
防止恶意输入、SQL注入和无权限操作
"""
from app import ActionCode


# 管理员:99 权限列表
PERMISSIONS_ADMINISTRATOR = [
    ActionCode.GET_ALL_USERS,
    ActionCode.GET_USERS_BY_PAGE,
    ActionCode.GET_USER_BY_ID,
    ActionCode.ADD_USER,
    ActionCode.UPDATE_USER,
    ActionCode.DELETE_USER
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
