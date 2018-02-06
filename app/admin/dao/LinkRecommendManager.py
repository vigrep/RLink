import traceback

from app import db
from app.dao.DbUtil import add_conditions
from app.model import MsgCode, StatusCode, ActionCode
from app.model.ActionResult import ActionResult, DictData
from app.model.Models import WorthyLink, PrimaryLink


def add_link_to_primary_table(link_ids, action=ActionCode.ADD_LINK_TO_PRIMARY_TABLE):
    ok = PrimaryLink.add_links(link_ids)
    if ok:
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.ADD_SUCC)
    else:
        return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)


def delete_link_from_primary_table(primary_ids, action=ActionCode.DELETE_LINK_FROM_PRIMARY_TABLE):
    ok = PrimaryLink.delete_links(primary_ids)
    if ok:
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.DELETE_SUCC)
    else:
        return ActionResult(action, StatusCode.FAILED, MsgCode.DELETE_FAILED)


def update_primary_link(primary_link_dict, action=ActionCode.UPDATE_PRIMARY_LINK):
    try:
        if primary_link_dict is None or not isinstance(primary_link_dict, dict):
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

        if "id" in primary_link_dict:
            try:
                primary_link_id = int(primary_link_dict["id"])
            except ValueError:     # 转换int错误会进到这里
                traceback.print_exc()
                return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_ID_DISMISS)

        if primary_link_id is None or primary_link_id < 0:
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

        # 判断primary_link_id 对应的数据是否存在数据库中
        db_primary_link = PrimaryLink.query.filter_by(id=primary_link_id).first()
        if db_primary_link is None:
            return ActionResult(action, StatusCode.FAILED, MsgCode.LINK_NOT_EXIST)

        # 更新到数据库中
        ok = db_primary_link.update(primary_link_dict)
        if ok:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.UPDATE_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)


def get_link_from_primary_table(page, page_size, conditions_dict, action=ActionCode.DELETE_LINK_FROM_PRIMARY_TABLE):
    try:
        query = add_conditions(PrimaryLink, conditions_dict)
        paginate = query.order_by(PrimaryLink.add_datetime.desc()).paginate(int(page), int(page_size), False)
        total_count = paginate.total
        primary_links = paginate.items
        links_list = list()
        for primary in primary_links:
            links_list.append(primary.get_link().json())

        result = DictData()
        result.add("total_record", total_count)
        result.add("data", links_list)
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, result)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.QUERY_FAILED)


def add_link_to_worthy_table(link_ids, action=ActionCode.ADD_LINK_TO_WORTHY_TABLE):
    ok = WorthyLink.add_links(link_ids)
    if ok:
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.ADD_SUCC)
    else:
        return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)


def delete_link_from_worthy_table(worthy_ids, action=ActionCode.DELETE_LINK_FROM_WORTHY_TABLE):
    ok = WorthyLink.delete_links(worthy_ids)
    if ok:
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.DELETE_SUCC)
    else:
        return ActionResult(action, StatusCode.FAILED, MsgCode.DELETE_FAILED)


def get_link_from_worthy_table(page, page_size, conditions_dict, action=ActionCode.DELETE_LINK_FROM_WORTHY_TABLE):
    try:
        query = add_conditions(WorthyLink, conditions_dict)
        paginate = query.order_by(WorthyLink.add_datetime.desc()).paginate(int(page), int(page_size), False)
        total_count = paginate.total
        worthy_links = paginate.items
        links_list = list()
        for worthy in worthy_links:
            links_list.append(worthy.get_link().json())

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
