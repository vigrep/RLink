from flask import json
from app import db
from app.dao.DbUtil import add_conditions
from app.model.Models import User
from app.model.ActionResult import ActionResult
from app.model.ActionResult import DictData
from app.model import ActionCode, StatusCode, MsgCode
import traceback


# 添加用户
def add_user(user_dict, action=ActionCode.ADD_USER):
    try:
        # 判断用户信息是否传入
        if user_dict is None or not isinstance(user_dict, dict):
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

        # 将dict中封装的用户信息，更新填充到新建的user对象中
        user = User()
        user.setvalue(user_dict)

        # 保存到数据库中
        ok = user.save()
        if ok:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.ADD_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)


# 根据user_ids 删除多个用户
def del_users_by_ids(user_ids, action=ActionCode.DELETE_MULTI_USER):
    try:
        if user_ids is None or not isinstance(user_ids, list):
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

        User.query.filter(User.id.in_(user_ids)).delete(synchronize_session=False)
        db.session.commit()
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.DELETE_SUCC)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.DELETE_FAILED)


# 修改用户信息
def update_user(user_dict, action=ActionCode.UPDATE_USER):
    try:
        # 判断用户信息是否传入
        if user_dict is None or not isinstance(user_dict, dict):
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)
        try:
            user_id = int(user_dict["id"])
        except ValueError:
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

        # 判断user_id 对应的用户是否存在数据库中
        db_user = User.query.filter_by(id=user_id).first()
        if db_user is None:
            return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)

        # user_dict为字典类型（key必须对应User表中的字段名)
        ok = db_user.update(user_dict)
        if ok:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.UPDATE_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)


# 根据页数和每页的个数，获取用户信息
def get_users_by_page(page, page_size, conditions_dict, action=ActionCode.GET_USERS_BY_PAGE):
    try:
        query = add_conditions(User, conditions_dict)
        paginate = query.order_by(User.register_datetime.desc()).paginate(int(page), int(page_size), False)

        total_count = paginate.total
        users = paginate.items
        user_list = list()
        for user in users:
            user_list.append(user.json())

        result = DictData()
        result.add("total_record", total_count)
        result.add("total_pages", paginate.pages)
        result.add("current_page", paginate.page)
        result.add("current_page_size", paginate.per_page)
        result.add("has_prev", paginate.has_prev)
        result.add("has_next", paginate.has_next)
        result.add("data", user_list)
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, result)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.QUERY_FAILED)


# 根据ID获取用户, 返回实体对象User
def get_user_model_by_id(user_id):
    if user_id is None:
        return None

    try:
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).first()
        return user
    except:
        traceback.print_exc()
        return None


# 根据ID获取用户, 返回实体对象User
def get_user_model_by_name(user_name, action=ActionCode.GET_USER_BY_NAME):
    if user_name is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        user_name = str(user_name)
        user = User.query.filter_by(name=user_name).first()
        if user is not None:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, user)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)


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
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)


# TODO[jj]: 完善方法
def check_user_name_valid(name):
    """
    检测用户名是否非法
    
    以下情况均视为非法：
    系统保留名称（Rlink等）、政治性、
    :param name: 
    :return: 
    """

    # FIXME: 具体实现
    return True


def check_user_name_duplicate(name, except_id=None):
    """
    检测用户名是否已经存在
    :param name: 要检测的用户名
    :param except_id: 排除的用户，不参与用户名是否存在的比较，一般更新用户名时传入该参数
    :return: True: 重复，False：没有重复
    """
    if except_id is not None:
        result = User.query.filter(User.name == name).filter(User.id != except_id).first()
    else:
        result = User.query.filter_by(name=name).first()
    return result is not None


# TODO[jj]: 完善方法
def check_user_email_valid(email):
    """
    检测邮箱账号是否非法

    :param name:
    :return:
    """

    # FIXME: 具体实现
    return True


def check_user_email_duplicate(email, except_id=None):
    """
    检测邮箱是否已经存在
    :param email: 要检测的邮箱
    :return: True: 重复，False：没有重复
    """
    if except_id is not None:
        result = User.query.filter(User.email == email).filter(User.id != except_id).first()
    else:
        result = User.query.filter_by(email=email).first()
    return result is not None

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
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.DELETE_FAILED)


# 通过json文件批量添加用户
def add_user_batch(json_file, action=ActionCode.BATCH_ADD_USER_BY_FILE):
    if json_file is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        file = open(json_file, encoding='utf-8')
        json_content = json.load(file)
        if json_content is None:
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    if json_content['data'] is not None and len(json_content['data']) > 0:
        # 记录添加失败的id
        failed_list = list()
        for user in json_content['data']:
            action_result = add_user(json.dumps(user))
            if action_result.status_code != StatusCode.SUCCESS:
                failed_data = dict()
                failed_data['error_msg'] = MsgCode.get_message(action_result.msg_code)
                failed_data['user_info'] = user
                failed_list.append(failed_data)
        if len(failed_list) > 0:
            result = DictData()
            result.add("about", "未添加成功的数据")
            result.add("total_record", len(failed_list))
            result.add("failed_data", failed_list)
            if len(failed_list) == len(json_content['data']):
                return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED, result)
            else:
                return ActionResult(action, StatusCode.SUCCESS, MsgCode.ADD_PART_SUCC, result)
        else:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.ADD_SUCC)
    else:
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_IS_NULL)


