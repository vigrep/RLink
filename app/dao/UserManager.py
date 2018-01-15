from flask import json
from app import db
from app.model.Models import User
from app.model.ActionResult import ActionResult
from app.model.ActionResult import DictData
from app.model import ActionCode, StatusCode, MsgCode


# 添加用户
def add_user(user_json, action=ActionCode.ADD_USER):
    # FIXME: 以下判断并初始化对象的代码，多处使用，考虑复用
    # 判断用户信息是否传入
    if user_json is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    # 将传入的json格式的用户信息，传换成dict格式
    try:
        user_dict = json.loads(user_json)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    # 通过dict本身的update方法，将dict中封装的用户信息，更新填充到新建的user对象中
    user = User()
    user.__dict__.update(user_dict)

    # 检查是否缺少必要的信息
    if user.name is None or user.name == "":
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NAME_IS_NULL)
    if user.password is None or user.password == "":
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_PASSWORD_IS_NULL)

    # 合法性检测
    if check_user_name_valid(user.name) and not user_is_exist(user):
        try:
            user.save()
            # ret = user_is_exist(user)     # FIXME: 添加后，是否需要再检测是否已经插入到数据库中
            # if ret:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.ADD_SUCC)
            # else:
            #     return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)
        except:
            return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)
    else:
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NAME_DUPLICATE)


# FIXME: 目前删除时，暂未考虑外键因素
# 根据user_ids 删除多个用户
def del_users_by_ids(user_ids, action=ActionCode.DELETE_MULTI_USER):
    if user_ids is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        user_ids = json.loads(user_ids)
        if len(user_ids) <= 0:
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    try:
        User.query.filter(User.id.in_(user_ids)).delete(synchronize_session=False)
        db.session.commit()
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.DELETE_SUCC)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.DELETE_FAILED)


# 修改用户信息
def update_user(user_json, action=ActionCode.UPDATE_USER):
    # 判断用户信息是否传入
    if user_json is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    # 将传入的json格式的用户信息，传换成dict格式
    try:
        user_dict = json.loads(user_json)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    if "id" in user_dict:
        try:
            user_id = int(user_dict["id"])
        except:     # 转换int错误会进到这里
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)
    else:
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)

    if user_id is None or user_id < 0:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    # 判断user_id 对应的数据是否存在数据库中
    db_user = User.query.filter_by(id=user_id).first()
    if db_user is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)

    # 检查要修改的值是否符合要求
    if "name" in user_dict:
        if user_dict["name"] == "":
            return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NAME_IS_NULL)
        if not check_user_name_valid(user_dict["name"], user_id):
            return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NAME_DUPLICATE)
    if "password" in user_dict and user_dict["password"] == "":
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_PASSWORD_IS_NULL)

    try:
        # 使用dict同时修改多值, 返回受修改影响的个数
        update_count = User.query.filter(User.id == user_id).update(user_dict)
        db.session.commit()
        if update_count >= 1:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.UPDATE_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)


# 根据页数和每页的个数，获取用户信息
def get_users_by_page(page, page_size, action=ActionCode.GET_USERS_BY_PAGE):
    try:
        page = int(page)
        page_size = int(page_size)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.PAGE_INVALID)

    if page <= 0:
        return ActionResult(action, StatusCode.FAILED, MsgCode.PAGE_INVALID)
    else:
        try:
            paginate = User.query.order_by(User.register_datetime.desc()).paginate(int(page), int(page_size), False)
            total_count = paginate.total
            users = paginate.items
            user_list = list()
            for user in users:
                user_list.append(user.json())

            result = DictData()
            result.add("total_record", total_count)
            result.add("data", user_list)
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, result)
        except:
            return ActionResult(action, StatusCode.FAILED, MsgCode.QUERY_FAILED)


# 根据ID获取用户, 返回实体对象User
def get_user_model_by_id(user_id, action=ActionCode.GET_USER_BY_ID):
    if user_id is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, user)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)



# 获取所有用户个数
def get_all_users_count():
    try:
        return User.query.count()
    except:
        return 0


# 根据ID获取用户, 返回User.json()
def get_user_by_id(user_id, action=ActionCode.GET_USER_BY_ID):
    if user_id is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            data = list()
            data.append(user.json())

            result = DictData()
            result.add("total_record", 1)
            result.add("data", data)
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, result)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)


# 检查用户名是否已被使用
def check_user_name_valid(name, user_id=None):
    if user_id is not None:
        result = User.query.filter(User.name == name).filter(User.id != user_id).first()
    else:
        result = User.query.filter_by(name=name).first()
    return result is None


# 检测用户是否存在 FIXME: 方法不完善
def user_is_exist(user):
    result = User.query.filter_by(name=user.name).first()
    return not(result is None)


# 根据user_id 删除用户
def del_user_by_id(user_id, action=ActionCode.DELETE_USER):
    if user_id is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.DELETE_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.DELETE_FAILED)
