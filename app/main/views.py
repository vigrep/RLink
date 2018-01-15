from flask import render_template
from flask import request
from flask import jsonify
from app import app
from app.dao import LinkManager, UserManager
from app.model.Models import User
from app.model.Models import Link
from app.utils import RequestProtection
from app.model import ActionCode, StatusCode, MsgCode
from app.model.ActionResult import ActionResult

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

        # name = request.values.get("name")
        # password = request.values.get("password")
        # gender = request.values.get("gender")
        # birth = request.values.get("birth")
        # nickname = request.values.get("nickname")
        # avatar = request.values.get("avatar")
        # introduce = request.values.get("introduce")
        # email = request.values.get("email")
        # phone = request.values.get("phone")
        #
        # user = User(name=name, password=password, gender=gender,
        #             birth=birth, nickname=nickname, avatar=avatar,
        #             introduce=introduce, email=email, phone=phone)
        # action_result = UserManager.add_user(user)

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

        # user_id = request.values.get("user_id")
        # action_result = UserManager.get_user_model_by_id(user_id)
        # if action_result.msg_code == MsgCode.QUERY_SUCC and action_result.data is not None:
        #     name = request.values.get("name")
        #     password = request.values.get("password")
        #     gender = request.values.get("gender")
        #     birth = request.values.get("birth")
        #     nickname = request.values.get("nickname")
        #     avatar = request.values.get("avatar")
        #     introduce = request.values.get("introduce")
        #     email = request.values.get("email")
        #     phone = request.values.get("phone")
        #
        #     user = action_result.data    # 只会存在一条,id 唯一，出现多个时请检查用户添加模块
        #     if name is not None:
        #         user.name = name
        #     if password is not None:
        #         user.password = password
        #     if gender is not None:
        #         user.gender = gender
        #     if birth is not None:
        #         user.birth = birth
        #     if nickname is not None:
        #         user.nickname = nickname
        #     if avatar is not None:
        #         user.avatar = avatar
        #     if introduce is not None:
        #         user.introduce = introduce
        #     if email is not None:
        #         user.email = email
        #     if phone is not None:
        #         user.phone = phone
        #
        #     action_result = UserManager.update_user(user)
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

        action_result = UserManager.get_users_by_page(page, page_size)
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

        action_result = LinkManager.get_links_by_page(page, page_size)
        resp = jsonify(action_result.pack())
    else:
        print(request_id)
        page = request.values.get("page")
        page_size = request.values.get("page_size")

        action_result = LinkManager.get_user_links_by_page(request_id, page, page_size)
        resp = jsonify(action_result.pack())
        # 访问被拒绝
        # resp = jsonify(ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_DENY).pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/searchResCategory', methods=['POST'])
@RequestProtection.logging(level="warn")
@RequestProtection.allow(action=ActionCode.SEARCH_CATEGORY)
def search(action=ActionCode.SEARCH_CATEGORY):
    # request_id = request.values.get("request_id")
    return "ddddd"
