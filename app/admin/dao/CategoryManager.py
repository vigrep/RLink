from app.dao.DbUtil import add_conditions
from app.model.Models import Category
from app import db
from app.model.ActionResult import ActionResult
from app.model.ActionResult import DictData
from app.model import ActionCode, StatusCode, MsgCode
import traceback


# 添加用户
def add_category(category_dict, action=ActionCode.ADD_CATEGORY):
    try:
        # 判断类别信息是否传入
        if category_dict is None or not isinstance(category_dict, dict):
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

        # 将dict中封装的类别信息，更新填充到新建的category对象中
        category = Category()
        category.setvalue(category_dict)

        # 保存到数据库中
        ok = category.save()
        if ok:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.ADD_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)


# 根据category_ids 删除1个或多个用户
def del_category_by_ids(category_ids, action=ActionCode.DELETE_CATEGORY):
    try:
        if category_ids is None or not isinstance(category_ids, list):
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

        Category.query.filter(Category.id.in_(category_ids)).delete(synchronize_session=False)
        db.session.commit()
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.DELETE_SUCC)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.DELETE_FAILED)


# 修改类别信息
def update_category(category_dict, action=ActionCode.UPDATE_CATEGORY):
    # category_dict为字典类型（key必须对应Category表中的字段名)
    try:
        if category_dict is None or not isinstance(category_dict, dict):
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

        try:
            category_id = int(category_dict["id"])
        except ValueError:
            traceback.print_exc()
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

        # 判断category_id 对应的类别是否存在数据库中
        db_category = Category.query.filter_by(id=category_id).first()
        if db_category is None:
            return ActionResult(action, StatusCode.FAILED, MsgCode.CATEGORY_NOT_EXIST)

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
def get_categories_by_page(page, page_size, conditions_dict, action=ActionCode.GET_CATEGORY):
    try:
        query = add_conditions(Category, conditions_dict)
        paginate = query.order_by(Category.id.asc()).paginate(int(page), int(page_size), False)

        total_count = paginate.total
        categories = paginate.items

        category_list = list()
        for category in categories:
            category_list.append(category.json())

        result = DictData()
        result.add("total_record", total_count)
        result.add("total_pages", paginate.pages)
        result.add("current_page", paginate.page)
        result.add("current_page_size", paginate.per_page)
        result.add("has_prev", paginate.has_prev)
        result.add("has_next", paginate.has_next)
        result.add("data", category_list)
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, result)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.QUERY_FAILED)


def check_category_name_duplicate(category_name, except_id=None):
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
    return result is not None


