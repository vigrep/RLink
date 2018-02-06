from app.dao.DbUtil import add_conditions
from app.model.Models import Role
from app.model.ActionResult import ActionResult
from app.model import ActionCode, StatusCode, MsgCode
import traceback
from flask import json
from app import db
from app.model.ActionResult import ActionResult
from app.model.ActionResult import DictData
from app.model import ActionCode, StatusCode, MsgCode
from app.dao import DbUtil
from sqlalchemy.sql import text
import traceback

from app.model.Permission import Permission


def get_permissions(action=ActionCode.GET_PERMISSIONS):
    data = DictData()
    data.add("permissions", Permission.get_permissions())
    return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, data)


def add_role(role_dict, action=ActionCode.ADD_ROLE):
    try:
        role = Role()
        role.name = role_dict["name"]
        role.permissions = role_dict["permissions"]

        ok = role.save()
        if ok:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.ADD_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)
    except:
        return ActionResult(action, StatusCode.FAILED, MsgCode.ADD_FAILED)


# 根据role_ids 删除多个角色
def del_roles_by_ids(role_ids, action=ActionCode.DELETE_ROLE):
    try:
        if role_ids is None or not isinstance(role_ids, list):
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

        Role.query.filter(Role.id.in_(role_ids)).delete(synchronize_session=False)
        db.session.commit()
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.DELETE_SUCC)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.DELETE_FAILED)


def update_role(role_dict, action=ActionCode.UPDATE_ROLE):
    try:
        # 判断角色信息是否传入
        if role_dict is None or not isinstance(role_dict, dict):
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)
        try:
            role_id = int(role_dict["id"])
        except:
            return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_ERROR)

        # 判断role_id 对应的用户是否存在数据库中
        db_role = Role.query.filter_by(id=role_id).first()
        if db_role is None:
            return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NOT_EXIST)

        # role_dict为字典类型（key必须对应User表中的字段名)
        ok = db_role.update(role_dict)
        if ok:
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.UPDATE_SUCC)
        else:
            return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.UPDATE_FAILED)


def query_roles(page, page_size, conditions_dict, action=ActionCode.GET_ROLES):
    try:
        query = add_conditions(Role, conditions_dict)
        paginate = query.order_by(Role.id.asc()).paginate(int(page), int(page_size), False)

        total_count = paginate.total
        roles = paginate.items

        role_list = list()
        for role in roles:
            role_list.append(role.json())

        result = DictData()
        result.add("total_record", total_count)
        result.add("total_pages", paginate.pages)
        result.add("current_page", paginate.page)
        result.add("current_page_size", paginate.per_page)
        result.add("has_prev", paginate.has_prev)
        result.add("has_next", paginate.has_next)
        result.add("data", role_list)
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, result)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.QUERY_FAILED)


def check_role_name_duplicate(name, except_id=None):
    """
    检测角色名是否已经存在
    :param name: 要检测的角色名
    :param except_id: 排除的角色，不参与角色名是否存在的比较，一般更新角色名时传入该参数
    :return: True: 重复，False：没有重复
    """
    if except_id is not None:
        result = Role.query.filter(Role.name == name).filter(Role.id != except_id).first()
    else:
        result = Role.query.filter_by(name=name).first()
    return result is not None
