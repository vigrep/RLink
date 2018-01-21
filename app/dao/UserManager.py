from flask import json
from app import db
from app.model.Models import User
from app.model.ActionResult import ActionResult
from app.model.ActionResult import DictData
from app.model import ActionCode, StatusCode, MsgCode
from app.dao import DbUtil
from sqlalchemy.sql import text
import traceback


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
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    # 如果传入了id, 删除掉，因为添加时id字段设置为自增
    if "id" in user_dict:
        user_dict.pop("id")

    # 将dict中封装的用户信息，更新填充到新建的user对象中
    user = User()
    user.setvalue(user_dict)

    # 检查是否缺少必要的信息
    if user.name is None or user.name == "":
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NAME_IS_NULL)
    if user.password is None or user.password == "":
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_PASSWORD_IS_NULL)

    # 合法性检测
    if check_user_name_valid(user.name) and not user_is_exist(user):
        # 保存到数据库中
        ok = user.save()
        # ret = user_is_exist(user)     # FIXME: 添加后，是否需要再检测是否已经插入到数据库中
        if ok:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.ADD_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)
    else:
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NAME_DUPLICATE)


# 根据user_ids 删除多个用户
def del_users_by_ids(user_ids, action=ActionCode.DELETE_MULTI_USER):
    if user_ids is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        user_ids = json.loads(user_ids)
        if len(user_ids) <= 0:
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    try:
        User.query.filter(User.id.in_(user_ids)).delete(synchronize_session=False)
        db.session.commit()
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.DELETE_SUCC)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.DELETE_FAILED)


# 修改用户信息
def update_user(user_json, action=ActionCode.UPDATE_USER):
    # 判断用户信息是否传入
    if user_json is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    # 将传入的json格式的用户信息，传换成dict格式
    # user_dict为字典类型（key必须对应User表中的字段名)
    try:
        user_dict = json.loads(user_json)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    if "id" in user_dict:
        try:
            user_id = int(user_dict["id"])
        except:     # 转换int错误会进到这里
            traceback.print_exc()
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)
    else:
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_ID_DISMISS)

    # user_id 是否合法
    if user_id is None or user_id < 0:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    # 判断user_id 对应的用户是否存在数据库中
    db_user = User.query.filter_by(id=user_id).first()
    if db_user is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)

    # 检查要修改的值是否符合要求
    if "name" in user_dict:
        if user_dict["name"] == "":
            return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NAME_IS_NULL)
        if not check_user_name_valid(user_dict["name"], except_id=user_id):
            return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NAME_DUPLICATE)
    if "password" in user_dict and user_dict["password"] == "":
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_PASSWORD_IS_NULL)

    try:
        # 使用User自身的update方法修改并提交到数据库, user_dict为字典类型（key必须对应User表中的字段名)
        ok = db_user.update(user_dict)
        if ok:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.UPDATE_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)


# 根据页数和每页的个数，获取用户信息
def get_users_by_page(page, page_size, conditions_json, action=ActionCode.GET_USERS_BY_PAGE):
    try:
        page = int(page)
        page_size = int(page_size)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.PAGE_INVALID)

    if page <= 0:
        return ActionResult(action, StatusCode.FAILED, MsgCode.PAGE_INVALID)

    try:
        query = add_conditions(User.query, conditions_json)
        paginate = query.order_by(User.register_datetime.desc()).paginate(int(page), int(page_size), False)

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
        traceback.print_exc()
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
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)


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


# 检查用户名是否已被使用
def check_user_name_valid(name, except_id=None):
    """
    检测用户名是否合法、已经存在
    :param name: 要检测的用户名
    :param except_id: 排除的用户，不参与用户名是否存在的比较，一般更新用户名时传入该参数
    :return:
    """
    if except_id is not None:
        result = User.query.filter(User.name == name).filter(User.id != except_id).first()
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


def add_conditions(query, conditions_json):
    """
    为query添加查询条件
    conditions_json 转换dict 错时，不会添加查询条件, 直接返回query

    :param query: User.query
    :param conditions_json: json格式, 如 {"name" : "xxx", "gender": "1"}
    :return:
    """
    if conditions_json is None:
        return query

    try:
        # 将客户端传入的json格式的条件转换成dict
        conditions_dict = json.loads(conditions_json)

        # 开始拼接sql的where语句
        where_statement = ""
        for key, value in conditions_dict.items():
            if hasattr(User, key):      # 加一层判断: 判断传入的条件字段是否是表中的某一个字段
                if key in User.LIKE_COLUMNS:
                    clause = DbUtil.create_sql_where_like_statement(key, value)
                # elif key == User.EQ_COLUMNS:
                #     clause = DbUtil.create_sql_where_eq_statement(key, value)
                else:
                    clause = DbUtil.create_sql_where_eq_statement(key, value)
                where_statement = DbUtil.and_sql_statement(where_statement, clause)
            else:
                # 走到这里的话，检查客户端传入的conditions字段
                print("表中没有该字段: %r[没有走到这里的话，检查客户端传入的conditions字段]" % key)

        # 使用sqlalchemy框架提供的text() 方法格式化 自己拼成的sql语句
        where_statement = text(where_statement)

        # 为查询添加上条件，并返回
        return query.filter(where_statement)
    except:
        traceback.print_exc()
        return query
