from app.Models import User
from app import db
from app import MsgCode
from app.ActionResult import ActionResult
from app import ActionCode
from app.ActionResult import DataType
from sqlalchemy import and_


# 获取所有用户信息
def get_all_user():
    userlist = User.query.all()
    count = len(userlist)
    json = {"status": "00",
            "resp_msg": "查询成功",
            "totalRecord": count
            }

    if count == 0:
        return json

    data = list()
    for user in userlist:
        data.append(user.json())
    json["data"] = data

    return json


# 根据页数和每页的个数，获取用户信息
def get_users_by_page(page, page_size, action=ActionCode.GET_USERS_BY_PAGE):
    try:
        page = int(page)
        page_size = int(page_size)
    except:
        return ActionResult(action, MsgCode.PAGE_INVALID)

    if page <= 0:
        return ActionResult(action, MsgCode.PAGE_INVALID)
    else:
        paginate = User.query.paginate(int(page), int(page_size), False)
        users = paginate.items
        data = list()
        for user in users:
            data.append(user.json())
        return ActionResult(action, MsgCode.QUERY_SUCC, data)


# 根据页数和每页的个数，获取用户信息
def get_users_by_page_with_condition(page, page_size, action=ActionCode.GET_USERS_BY_PAGE):
    try:
        page = int(page)
        page_size = int(page_size)
    except:
        return ActionResult(action, MsgCode.PAGE_INVALID)

    if page <= 0:
        return ActionResult(action, MsgCode.PAGE_INVALID)
    else:
        paginate = User.query.paginate(page, page_size, False)
        users = paginate.items
        data = list()
        for user in users:
            data.append(user.json())
        return ActionResult(action, MsgCode.QUERY_SUCC, data)


# 添加用户
def add_user(user, action=ActionCode.ADD_USER):
    if user.name is None:
        return ActionResult(action, MsgCode.USER_NAME_INVALID)
    if user.password is None:
        return ActionResult(action, MsgCode.USER_PASSWORD_INVALID)

    # 合法性检测
    if check_user_name_valid(user.name) and not is_exist(user):
        try:
            db.session.add(user)
            db.session.commit()
            ret = is_exist(user)
            if ret:
                return ActionResult(action, MsgCode.USER_ADD_SUCC)
            else:
                return ActionResult(action, MsgCode.USER_ADD_FAILED)
        except:
            return ActionResult(action, MsgCode.USER_ADD_FAILED)
    else:
        return ActionResult(action, MsgCode.USER_NAME_DUPLICATE)


# 检查用户名是否已被使用
def check_user_name_valid(name, user_id=None):
    if user_id is not None:
        result = User.query.filter(User.name == name).filter(User.id != user_id).first()
    else:
        result = User.query.filter_by(name=name).first()
    return result is None


# 检测用户是否存在 FIXME: 方法不完善
def is_exist(user):
    result = User.query.filter_by(name=user.name).first()
    return not(result is None)


# 修改用户信息
def update_user(user, action=ActionCode.UPDATE_USER):

    # 用户信息合法性检测
    if user is None or user.id is None:
        return ActionResult(action, MsgCode.USER_NOT_EXIST)

    db_user = User.query.filter_by(id=user.id).first()
    if db_user is None:
        return ActionResult(action, MsgCode.USER_NOT_EXIST)

    # 合法性检测
    if check_user_name_valid(user.name, user.id):
        try:
            db.session.add(user)
            db.session.commit()
            ret = is_exist(user)
            if ret:
                return ActionResult(action, MsgCode.UPDATE_SUCC)
            else:
                return ActionResult(action, MsgCode.UPDATE_FAILED)
        except:
            return ActionResult(action, MsgCode.USER_ADD_FAILED)
    else:
        return ActionResult(action, MsgCode.USER_NAME_DUPLICATE)


# 根据ID获取用户, 返回实体对象User
def get_user_model_by_id(user_id, action=ActionCode.GET_USER_BY_ID, data_type=DataType.OBJECT):
    if user_id is None:
        return ActionResult(action, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            if data_type == DataType.OBJECT:
                return ActionResult(action, MsgCode.QUERY_SUCC, user)
        else:
            return ActionResult(action, MsgCode.USER_NOT_EXIST)
    except:
        return ActionResult(action, MsgCode.USER_NOT_EXIST)


# 根据ID获取用户, 返回User.json()
def get_user_by_id(user_id, action=ActionCode.GET_USER_BY_ID):
    if user_id is None:
        return ActionResult(action, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            data = list()
            data.append(user.json())
            return ActionResult(action, MsgCode.QUERY_SUCC, data)
        else:
            return ActionResult(action, MsgCode.USER_NOT_EXIST)
    except:
        return ActionResult(action, MsgCode.USER_NOT_EXIST)


# FIXME: 目前暂未考虑外键因素
# 根据user_id 删除用户
def del_user_by_id(user_id, action=ActionCode.DELETE_USER):
    if user_id is None:
        return ActionResult(action, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return ActionResult(action, MsgCode.DELETE_SUCC)
        else:
            return ActionResult(action, MsgCode.USER_NOT_EXIST)
    except:
        return ActionResult(action, MsgCode.DELETE_FAILED)



