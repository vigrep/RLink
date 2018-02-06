"""
业务层接口函数
"""
import traceback

from sqlalchemy import or_, func

from app import db
from app.model import MsgCode, StatusCode, ActionCode
from app.model.ActionResult import DictData, ActionResult
from app.model.Models import User, Link, Category, WorthyLink, PrimaryLink


def get_primary_link(action=ActionCode.GET_PRIMARY_LINK):
    try:
        primary_links = PrimaryLink.query.order_by(PrimaryLink.add_datetime.desc()).all()
        total_count = len(primary_links)
        links_list = list()
        for primary in primary_links:
            links_list.append({"url": primary.get_url(), "img": primary.get_img()})

        result = DictData()
        result.add("total_record", total_count)
        result.add("data", links_list)
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, result)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.QUERY_FAILED)


def get_worthy_link(page, page_size, action=ActionCode.GET_WORTHY_LINK):
    try:
        paginate = WorthyLink.query.order_by(WorthyLink.add_datetime.desc()).paginate(int(page), int(page_size), False)
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


def search_category(word, action=ActionCode.SEARCH_CATEGORY):
    try:
        wd = '%%%s%%' % word
        result = db.session.query(Link.category_id, Category.name, func.count(Link.category_id)) \
            .filter(or_(Link.name.like(wd),  Link.description.like(wd)))\
            .group_by(Link.category_id). \
            join(Category).all()

        if result is not None and isinstance(result, list):
            total_category_count = len(result)
            result_list = []
            for res in result:
                if len(res) == 3:
                    sub = dict()
                    sub["category_id"] = res[0]
                    sub["category_name"] = res[1]
                    sub["count"] = res[2]
                    result_list.append(sub)

            data = DictData()
            data.add("total_record", total_category_count)
            data.add("data", result_list)
            data.add("word", word)
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, data)
    except:
        traceback.print_exc()
        return ActionResult(action, StatusCode.FAILED, MsgCode.QUERY_FAILED)


def search(page, page_size, word, category_id=None, action=ActionCode.SEARCH_CATEGORY):
    try:
        wd = '%%%s%%' % word
        query = Link.query.filter(or_(Link.name.like(wd),  Link.description.like(wd)))
        if category_id is not None:
            query = query.filter_by(category_id=int(category_id))

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


def get_links_by_name(user_name, action=ActionCode.GET_LINK_BY_ID):
    action_result = get_user_model_by_name(user_name)

    if action_result.success():
        user_db = action_result.data

        users = user_db.links.all()
        user_list = list()
        for user in users:
            user_list.append(user.json())

        data = DictData()
        data.add("total_record", user_db.links.count())
        data.add("data", user_list)

        return ActionResult(action, StatusCode.SUCCESS, MsgCode.QUERY_SUCC, data)
    else:
        return action_result


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
