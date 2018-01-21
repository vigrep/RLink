from app.model.Models import Category
from flask import json
from app import db
from app.model.ActionResult import ActionResult
from app.model.ActionResult import DictData
from app.model import ActionCode, StatusCode, MsgCode
from app.dao import DbUtil
from sqlalchemy.sql import text
import traceback


# 添加用户
def add_category(category_json, action=ActionCode.ADD_CATEGORY):
    # FIXME: 以下判断并初始化对象的代码，多处使用，考虑复用
    # 判断类别信息是否传入
    if category_json is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    # 将传入的json格式的类别信息，传换成dict格式
    try:
        category_dict = json.loads(category_json)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    # 如果传入了id, 删除掉，因为添加时id字段设置为自增
    if "id" in category_dict:
        category_dict.pop("id")

    # 将dict中封装的类别信息，更新填充到新建的category对象中
    category = Category()
    category.setvalue(category_dict)

    # 检查是否缺少必要的信息
    if category.name is None or category.name == "":
        return ActionResult(action, StatusCode.FAILED, MsgCode.CATEGORY_NAME_IS_NULL)

    # 合法性检测
    if check_category_name_is_exist(category.name):
        # 保存到数据库中
        ok = category.save()
        if ok:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.ADD_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)
    else:
        return ActionResult(action, StatusCode.FAILED, MsgCode.CATEGORY_NAME_DUPLICATE)


# 根据category_ids 删除1个或多个用户
def del_category_by_ids(category_ids_json, action=ActionCode.DELETE_CATEGORY):
    if category_ids_json is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        category_ids = json.loads(category_ids_json)
        if len(category_ids) <= 0:
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    try:
        Category.query.filter(Category.id.in_(category_ids)).delete(synchronize_session=False)
        db.session.commit()
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.DELETE_SUCC)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.DELETE_FAILED)


# 修改类别信息
def update_category(category_json, action=ActionCode.UPDATE_CATEGORY):
    # 判断类别信息是否传入
    if category_json is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    # 将传入的json格式的类别信息，传换成dict格式
    # category_dict为字典类型（key必须对应Category表中的字段名)
    try:
        category_dict = json.loads(category_json)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    # 更新必须要有id字段
    if "id" in category_dict:
        try:
            category_id = int(category_dict["id"])
        except:     # 转换int错误会进到这里
            traceback.print_exc()
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)
    else:
        return ActionResult(action, StatusCode.FAILED, MsgCode.CATEGORY_ID_DISMISS)

    # category_id 是否合法
    if category_id is None or category_id < 0:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    # 判断category_id 对应的类别是否存在数据库中
    db_category = Category.query.filter_by(id=category_id).first()
    if db_category is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.CATEGORY_NOT_EXIST)

    # 检查要修改的值是否符合要求
    if "name" in category_dict:
        if category_dict["name"] == "":
            return ActionResult(action, StatusCode.FAILED, MsgCode.CATEGORY_NAME_IS_NULL)
        if not check_category_name_is_exist(category_dict["name"], except_id=category_id):
            return ActionResult(action, StatusCode.FAILED, MsgCode.CATEGORY_NAME_DUPLICATE)

    try:
        # 使用Category自身的update方法修改并提交到数据库, category_dict为字典类型（key必须对应Category表中的字段名)
        ok = db_category.update(category_dict)
        if ok:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.UPDATE_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)


# 根据页数和每页的个数，获取用户信息
def get_categories_by_page(page, page_size, conditions_json, action=ActionCode.GET_CATEGORY):
    try:
        page = int(page)
        page_size = int(page_size)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.PAGE_INVALID)

    if page <= 0:
        return ActionResult(action, StatusCode.FAILED, MsgCode.PAGE_INVALID)

    try:
        query = add_conditions(Category.query, conditions_json)
        paginate = query.order_by(Category.id.asc()).paginate(int(page), int(page_size), False)

        total_count = paginate.total
        categories = paginate.items

        category_list = list()
        for category in categories:
            category_list.append(category.json())

        result = DictData()
        result.add("total_record", total_count)
        result.add("data", category_list)
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, result)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.QUERY_FAILED)


def check_category_name_is_exist(category_name, except_id=None):
    """
    检测类别名是否合法、已经存在
    :param category_name: 要检测的类别名
    :param except_id: 排除的类别，不参与类别名是否存在的比较，一般更新类别名时传入该参数
    :return:
    """
    if except_id is not None:
        result = Category.query.filter(Category.name == category_name).filter(Category.id != except_id).first()
    else:
        result = Category.query.filter(Category.name == category_name).first()
    return result is None


def add_conditions(query, conditions_json):
    """
    为query添加查询条件
    conditions_json 转换dict 错时，不会添加查询条件, 直接返回query

    :param query: Category.query
    :param conditions_json: json格式, 如 {"name" : "xxx"}
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
            if hasattr(Category, key):      # 加一层判断: 判断传入的条件字段是否是表中的某一个字段
                if key in Category.LIKE_COLUMNS:
                    clause = DbUtil.create_sql_where_like_statement(key, value)
                # elif key == Category.EQ_COLUMNS:
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
