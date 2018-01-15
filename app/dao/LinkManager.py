"""
链接Link 相关操作
"""
from app import db
from app.model.Models import Link
from app.model.Models import User
from app.model.ActionResult import ActionResult
from app.model.ActionResult import DictData
from app.model import ActionCode, StatusCode, MsgCode
import json


# 添加链接
def add_link(link_json, action=ActionCode.ADD_LINK):
    # 判断链接信息是否传入
    if link_json is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    # 将传入的json格式的链接信息，传换成dict格式
    try:
        link_dict = json.loads(link_json)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    # 通过dict本身的update方法，将dict中封装的链接信息，更新填充到新建的Link对象中
    link = Link()
    link.__dict__.update(link_dict)

    # 检查是否缺少必要的信息
    if link.name is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_NAME_IS_NULL)
    if link.link is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_IS_NULL)

    # 合法性检测
    if check_link_valid(link):
        try:
            db.session.add(link)
            db.session.commit()
            ret = link_is_exist(link)
            if ret:
                return ActionResult(action, StatusCode.SUCCESS, MsgCode.ADD_SUCC)
            else:
                return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)
        except:
            return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)
    else:
        return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_INVALID)


# FIXME: 目前删除时，暂未考虑外键因素
# 根据link_ids 删除多个链接
def del_links_by_ids(link_ids_json, action=ActionCode.DELETE_MULTI_LINK):
    if link_ids_json is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        link_ids = json.loads(link_ids_json)
        if len(link_ids) <= 0:
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    try:
        Link.query.filter(Link.id.in_(link_ids)).delete(synchronize_session=False)
        db.session.commit()
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.DELETE_SUCC)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.DELETE_FAILED)


# 修改用户信息
# link_json: 要要修改的字段和值, dict格式
def update_link(link_json, action=ActionCode.UPDATE_LINK):
    # 判断链接信息是否传入
    if link_json is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    # 将传入的json格式的链接信息，传换成dict格式
    try:
        link_dict = json.loads(link_json)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    if "id" in link_dict:
        try:
            link_id = int(link_dict["id"])
        except:     # 转换int错误会进到这里
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)
    else:
        return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_NOT_EXIST)

    if link_id is None or link_id < 0:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    # 判断link_id 对应的数据是否存在数据库中
    db_link = Link.query.filter_by(id=link_id).first()
    if db_link is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_NOT_EXIST)

    # 检查要修改的值是否符合要求
    if "name" in link_dict and link_dict["name"] == "":
        return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_NAME_IS_NULL)
    if "link" in link_dict:
        if link_dict["link"] == "":
            return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_IS_NULL)
        # 合法性检测
        if not check_link_valid(link_dict["link"]):
            return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_INVALID)

    try:
        # 使用dict同时修改多值, 返回受修改影响的个数
        update_count = Link.query.filter(Link.id == link_id).update(link_dict)
        db.session.commit()
        if update_count >= 1:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.UPDATE_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)


# 根据page和pageSize 获取所有链接
def get_links_by_page(page, page_size, action=ActionCode.GET_LINKS_BY_PAGE):
    try:
        page = int(page)
        page_size = int(page_size)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.PAGE_INVALID)

    if page <= 0:
        return ActionResult(action, StatusCode.FAILED, MsgCode.PAGE_INVALID)
    else:
        try:
            paginate = Link.query.order_by(Link.datetime.desc()).paginate(int(page), int(page_size), False)
            total_count = paginate.total
            links = paginate.items
            links_list = list()
            for link in links:
                links_list.append(link.json())

            result = DictData()
            result.add("total_record", total_count)
            result.add("data", links_list)
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, result)
        except:
            return ActionResult(action, StatusCode.FAILED, MsgCode.QUERY_FAILED)


# 获取某个用户保存的所有链接
def get_user_links_by_page(user_id, page, page_size, action=ActionCode.GET_LINKS_BY_PAGE):
    try:
        user_id = int(user_id)
        page = int(page)
        page_size = int(page_size)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.PAGE_INVALID)

    try:
        user = User.query.filter_by(id=user_id).first()
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)

    if page <= 0:
        return ActionResult(action, StatusCode.FAILED, MsgCode.PAGE_INVALID)
    else:
        try:
            paginate = user.shared_links().paginate(int(page), int(page_size), False)
            # paginate = Link.query.order_by(Link.datetime.desc()).paginate(int(page), int(page_size), False)
            links = paginate.items
            links_total_count = paginate.total
            links_list = list()
            for link in links:
                links_list.append(link.json())

            result = DictData()
            result.add("total_record", links_total_count)
            result.add("data", links_list)
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, result)
        except:
            return ActionResult(action, StatusCode.FAILED, MsgCode.QUERY_FAILED)
# FIXME: 需要完善
# 检测链接的合法性
def check_link_valid(link):
    if link is None:
        return False
    return True
    # if str(link.name).find("龚哲") or str(link.name).find("俊杰"):
    #    return False
    # else:
    #    return True


# 检测link是否存在 FIXME: 方法不完善
def link_is_exist(link):
    result = Link.query.filter_by(id=link.id).first()
    return result is not None


# 获取所有链接的个数
def get_all_links_count():
    try:
        return Link.query.count()
    except:
        return 0


# 根据link_id 删除链接
def del_link_by_id(link_id, action=ActionCode.DELETE_LINK):
    if link_id is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        link_id = int(link_id)  # 如果传入的值不能转换为int, 返回参数错误
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

    try:
        link = Link.query.filter_by(id=link_id).first()
        if link is not None:
            db.session.delete(link)
            db.session.commit()
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.DELETE_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_NOT_EXIST)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.DELETE_FAILED)

