"""
链接Link 相关操作
"""
from app import db
from app.dao.DbUtil import add_conditions
from app.model.Models import Link
from app.model.Models import User
from app.model.ActionResult import ActionResult
from app.model.ActionResult import DictData
from app.model import ActionCode, StatusCode, MsgCode
from app.dao import DbUtil
from sqlalchemy.sql import text
import json
import traceback


# 添加链接
def add_link(link_dict, action=ActionCode.ADD_LINK):
    try:
        # 判断链接信息是否传入
        if link_dict is None or not isinstance(link_dict, dict):
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

        # 将dict中封装的链接信息，更新填充到新建的Link对象中
        link = Link()
        link.setvalue(link_dict)

        # 保存到数据库中
        ok = link.save()
        if ok:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.ADD_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)


# 根据link_ids 删除多个链接
def del_links_by_ids(link_ids, action=ActionCode.DELETE_MULTI_LINK):
    try:
        if link_ids is None or not isinstance(link_ids, list):
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

        Link.query.filter(Link.id.in_(link_ids)).delete(synchronize_session=False)
        db.session.commit()
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.DELETE_SUCC)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.DELETE_FAILED)


# 修改用户信息
# link_json: 要要修改的字段和值, dict格式
def update_link(link_dict, action=ActionCode.UPDATE_LINK):
    try:
        if link_dict is None or not isinstance(link_dict, dict):
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

        if "id" in link_dict:
            try:
                link_id = int(link_dict["id"])
            except ValueError:     # 转换int错误会进到这里
                traceback.print_exc()
                return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_ID_DISMISS)

        if link_id is None or link_id < 0:
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

        # 判断link_id 对应的数据是否存在数据库中
        db_link = Link.query.filter_by(id=link_id).first()
        if db_link is None:
            return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_NOT_EXIST)

        # 更新到数据库中
        ok = db_link.update(link_dict)
        if ok:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.UPDATE_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)


# 根据page和pageSize 获取所有链接
def get_links_by_page(page, page_size, conditions_dict, action=ActionCode.GET_LINKS_BY_PAGE):
    try:
        query = add_conditions(Link, conditions_dict)
        paginate = query.order_by(Link.update_datetime.desc()).paginate(int(page), int(page_size), False)
        total_count = paginate.total
        links = paginate.items
        links_list = list()
        for link in links:
            links_list.append(link.json())

        result = DictData()
        result.add("total_record", total_count)
        result.add("total_pages", paginate.pages)
        result.add("current_page", paginate.page)
        result.add("current_page_size", paginate.per_page)
        result.add("has_prev", paginate.has_prev)
        result.add("has_next", paginate.has_next)
        result.add("data", links_list)
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, result)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.QUERY_FAILED)


# 获取某个用户保存的所有链接
def get_user_links_by_page(user_id, page, page_size, action=ActionCode.GET_LINKS_BY_PAGE):
    try:
        user_id = int(user_id)
        page = int(page)
        page_size = int(page_size)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.PAGE_INVALID)

    try:
        user = User.query.filter_by(id=user_id).first()
    except:
        traceback.print_exc()
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
            traceback.print_exc()
            return ActionResult(action, StatusCode.FAILED, MsgCode.QUERY_FAILED)


# 根据ID获取链接信息
def get_link_by_id(link_id, action=ActionCode.GET_LINK_BY_ID):
    if link_id is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        link_id = int(link_id)
        link = Link.query.filter_by(id=link_id).first()
        if link is not None:
            data = list()
            data.append(link.json())

            result = DictData()
            result.add("total_record", 1)
            result.add("data", data)
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, result)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_NOT_EXIST)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_NOT_EXIST)


# TODO[JJ]: 需要完善
# 检测链接的合法性
def check_link_valid(link):
    if link is None:
        return False
    return True


# TODO[jj]: 需要完善
# 检测link是否存在
def link_is_exist(link):
    result = Link.query.filter_by(id=link.id).first()
    return result is not None


# 根据link_id 删除链接
def del_link_by_id(link_id, action=ActionCode.DELETE_LINK):
    if link_id is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    try:
        link_id = int(link_id)  # 如果传入的值不能转换为int, 返回参数错误
    except:
        traceback.print_exc()
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
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.DELETE_FAILED)


# 通过json文件批量添加用户
def add_link_batch(json_file, action=ActionCode.BATCH_ADD_LINK_BY_FILE):
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
        for link in json_content['data']:
            action_result = add_link(json.dumps(link))
            if action_result.status_code != StatusCode.SUCCESS:
                failed_data = dict()
                failed_data['error_msg'] = MsgCode.get_message(action_result.msg_code)
                failed_data['link_info'] = link
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
        return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_IS_NULL)


