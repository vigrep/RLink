from flask import render_template
from flask import request
from flask import jsonify
from app import app
from app.dao import LinkManager, UserManager, CategoryManager
from app.model.Models import User
from app.model.Models import Link
from app.utils import RequestProtection
from app.model import StatusCode, MsgCode
from app.model import ActionCode
from app.model.ActionResult import ActionResult
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


# 添加用户
@app.route('/userAdd', methods=['POST'])
def user_add(action=ActionCode.ADD_USER):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        user_json = request.values.get("msg_body")
        action_result = UserManager.add_user(user_json)

        resp = jsonify(action_result.pack())
    else:
        # 访问被拒绝
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/userDel', methods=['POST'])
def user_del(action=ActionCode.DELETE_USER):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        user_ids = request.values.get("user_ids")

        action_result = UserManager.del_users_by_ids(user_ids)
        resp = jsonify(action_result.pack())
    else:
        # 访问被拒绝
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 修改用户信息
@app.route('/userUpdate', methods=['POST'])
def user_update(action=ActionCode.UPDATE_USER):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        user_json = request.values.get("msg_body")
        action_result = UserManager.update_user(user_json)

        resp = jsonify(action_result.pack())
    else:
        # 访问被拒绝
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 查询用户
@app.route('/userSelectAll', methods=['POST'])
def get_users_by_page(action=ActionCode.GET_USERS_BY_PAGE):
    request_id = request.values.get("request_id")

    # TODO: 把权限检查功能放到装饰器中
    if RequestProtection.is_allow(action, request_id):
        page = request.values.get("page")
        page_size = request.values.get("page_size")
        conditions_json = request.values.get("conditions")

        action_result = UserManager.get_users_by_page(page, page_size, conditions_json)
        resp = jsonify(action_result.pack())
    else:
        # 访问被拒绝
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/getUserById', methods=['POST'])
def get_user_by_id(action=ActionCode.GET_USER_BY_ID):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        user_id = request.values.get("user_id")

        action_result = UserManager.get_user_by_id(user_id)
        resp = jsonify(action_result.pack())
    else:
        # 访问被拒绝
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 添加链接Link
@app.route('/linkAdd', methods=['POST'])
def link_add(action=ActionCode.ADD_LINK):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        msg_body = request.values.get("msg_body")
        action_result = LinkManager.add_link(msg_body)

        resp = jsonify(action_result.pack())
    else:
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 删除链接
@app.route('/linkDel', methods=['POST'])
def link_del(action=ActionCode.DELETE_MULTI_LINK):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        link_ids_json = request.values.get("link_ids")
        action_result = LinkManager.del_links_by_ids(link_ids_json)

        resp = jsonify(action_result.pack())
    else:
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 修改链接信息
@app.route('/linkUpdate', methods=['POST'])
def link_update(action=ActionCode.UPDATE_LINK):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        link_json = request.values.get("msg_body")
        action_result = LinkManager.update_link(link_json)

        resp = jsonify(action_result.pack())
    else:
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 查询所有链接
@app.route('/linkSelectAll', methods=['POST'])
def get_links_by_page(action=ActionCode.GET_LINKS_BY_PAGE):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        page = request.values.get("page")
        page_size = request.values.get("page_size")
        conditions_json = request.values.get("conditions")

        action_result = LinkManager.get_links_by_page(page, page_size, conditions_json)
        resp = jsonify(action_result.pack())
    else:
        # 访问被拒绝
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 添加类别
@app.route('/categoryAdd', methods=['POST'])
def category_add(action=ActionCode.ADD_CATEGORY):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        category_json = request.values.get("msg_body")
        action_result = CategoryManager.add_category(category_json)

        resp = jsonify(action_result.pack())
    else:
        # 访问被拒绝
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 删除类别
@app.route('/categoryDel', methods=['POST'])
def category_del(action=ActionCode.DELETE_CATEGORY):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        category_ids_json = request.values.get("category_ids")
        action_result = CategoryManager.del_category_by_ids(category_ids_json)

        resp = jsonify(action_result.pack())
    else:
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 修改链接信息
@app.route('/categoryUpdate', methods=['POST'])
def category_update(action=ActionCode.UPDATE_LINK):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        category_json = request.values.get("msg_body")
        action_result = CategoryManager.update_category(category_json)

        resp = jsonify(action_result.pack())
    else:
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 查询所有链接
@app.route('/categorySelectAll', methods=['POST'])
def get_categories_by_page(action=ActionCode.GET_CATEGORY):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        page = request.values.get("page")
        page_size = request.values.get("page_size")
        conditions_json = request.values.get("conditions")

        action_result = CategoryManager.get_categories_by_page(page, page_size, conditions_json)
        resp = jsonify(action_result.pack())
    else:
        # 访问被拒绝
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# FIXME
@app.route('/<name>', methods=['POST', 'GET'])
def get_links(name, action=ActionCode.GET_USER_BY_NAME):
    action_result = UserManager.get_user_model_by_name(name)
    print(name)
    user = action_result.data
    print(user)
    print(user.links.all())
    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/searchResCategory', methods=['POST'])
@RequestProtection.logging(level="warn")
@RequestProtection.allow(action=ActionCode.SEARCH_CATEGORY)
def search(action=ActionCode.SEARCH_CATEGORY):
    # request_id = request.values.get("request_id")
    return "ddddd"


@app.route('/addUsersFromFile', methods=['POST'])
def add_users_from_json_file(action=ActionCode.BATCH_ADD_USER_BY_FILE):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        file = request.files['json_file']

        # FIXME debug: need delete
        # basedir = os.path.abspath(os.path.dirname(__file__))
        # file = basedir + "\\batch_add_example.json"

        action_result = UserManager.add_user_batch(file)
        resp = jsonify(action_result.pack())
    else:
        # 访问被拒绝
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/addLinksFromFile', methods=['POST'])
def add_links_from_json_file(action=ActionCode.BATCH_ADD_LINK_BY_FILE):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        file = request.files['json_file']

        action_result = UserManager.add_user_batch(file)
        resp = jsonify(action_result.pack())
    else:
        # 访问被拒绝
        resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
