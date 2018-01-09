from flask import render_template
from flask import request
from flask import jsonify
from app import app
from app import DbManager
from app.Models import User
from app import RequestProtection
from app import ActionCode
from app import MsgCode

@app.route('/')
@app.route('/index')
def index():
    user = {"name": "任帅"}
    return render_template("index.html")


# 查询用户
@app.route('/userSelectAll', methods=['POST'])
def get_users_by_page(action=ActionCode.GET_USERS_BY_PAGE):
    request_id = request.values.get("request_id")
    page = request.values.get("page")
    page_size = request.values.get("pageSize")
    name = request.values.get("name")
    print(request_id)
    print(page)
    print(page_size)
    print(action)
    print(name)

    if RequestProtection.is_allow(action, request_id):
        action_result = DbManager.get_users_by_page(page, page_size)
        if action_result.msg_code == MsgCode.QUERY_SUCC:
            resp = jsonify({
                "action": action_result.action_code,
                "status": action_result.msg_code,
                "resp_msg": MsgCode.get_message(action_result.msg_code),
                "total_record": len(action_result.data),
                "data": action_result.data
            })
        else:
            resp = jsonify({
                "action": action_result.action_code,
                "status": action_result.msg_code,
                "resp_msg": MsgCode.get_message(action_result.msg_code)
            })
    else:
        # 访问被拒绝
        resp = jsonify({
            "action": action,
            "status": MsgCode.REQUEST_DENY,
            "resp_msg": MsgCode.get_message(MsgCode.REQUEST_DENY)
            })
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/getUserById', methods=['POST'])
def get_user_by_id(action=ActionCode.GET_USER_BY_ID):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        user_id = request.values.get("user_id")
        action_result = DbManager.get_user_by_id(user_id)
        if action_result.msg_code == MsgCode.QUERY_SUCC:
            resp = jsonify({
                "action": action_result.action_code,
                "status": action_result.msg_code,
                "resp_msg": MsgCode.get_message(action_result.msg_code),
                "total_record": len(action_result.data),
                "data": action_result.data
            })
        else:
            resp = jsonify({
                "action": action_result.action_code,
                "status": action_result.msg_code,
                "resp_msg": MsgCode.get_message(action_result.msg_code)
            })
    else:
        # 访问被拒绝
        resp = jsonify({
            "action": action,
            "status": MsgCode.REQUEST_DENY,
            "resp_msg": MsgCode.get_message(MsgCode.REQUEST_DENY)
        })
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 添加用户
@app.route('/userAdd', methods=['POST'])
def user_add(action=ActionCode.ADD_USER):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        name = request.values.get("name")
        password = request.values.get("password")
        gender = request.values.get("gender")
        birth = request.values.get("birth")
        nickname = request.values.get("nickname")
        avatar = request.values.get("avatar")
        introduce = request.values.get("introduce")
        email = request.values.get("email")
        phone = request.values.get("phone")

        user = User(name=name,
                    password=password,
                    gender=gender,
                    birth=birth,
                    nickname=nickname,
                    avatar=avatar,
                    introduce=introduce,
                    email=email,
                    phone=phone
                    )
        action_result = DbManager.add_user(user)

        resp = jsonify({
            "action": action_result.action_code,
            "status": action_result.msg_code,
            "resp_msg": MsgCode.get_message(action_result.msg_code)
        })
    else:
        # 访问被拒绝
        resp = jsonify({
            "action": action,
            "status": MsgCode.REQUEST_DENY,
            "resp_msg": MsgCode.get_message(MsgCode.REQUEST_DENY)
        })

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 修改用户信息
@app.route('/userUpdate', methods=['POST'])
def user_update(action=ActionCode.UPDATE_USER):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        user_id = request.values.get("user_id")

        action_result = DbManager.get_user_model_by_id(user_id)
        if action_result.msg_code == MsgCode.QUERY_SUCC and action_result.data is not None:
            name = request.values.get("name")
            password = request.values.get("password")
            gender = request.values.get("gender")
            birth = request.values.get("birth")
            nickname = request.values.get("nickname")
            avatar = request.values.get("avatar")
            introduce = request.values.get("introduce")
            email = request.values.get("email")
            phone = request.values.get("phone")

            user = action_result.data    # 只会存在一条,id 唯一，出现多个时请检查用户添加模块
            if name is not None:
                user.name = name
            if password is not None:
                user.password = password
            if gender is not None:
                user.gender = gender
            if birth is not None:
                user.birth = birth
            if nickname is not None:
                user.nickname = nickname
            if avatar is not None:
                user.avatar = avatar
            if introduce is not None:
                user.introduce = introduce
            if email is not None:
                user.email = email
            if phone is not None:
                user.phone = phone

            action_result = DbManager.update_user(user)
            resp = jsonify({
                "action": action_result.action_code,
                "status": action_result.msg_code,
                "resp_msg": MsgCode.get_message(action_result.msg_code)
            })
        else:
            # 用户不存在
            resp = jsonify({
                "action": action_result.action_code,
                "status": action_result.msg_code,
                "resp_msg": MsgCode.get_message(action_result.msg_code)
            })
    else:
        # 访问被拒绝
        resp = jsonify({
            "action": action,
            "status": MsgCode.REQUEST_DENY,
            "resp_msg": MsgCode.get_message(MsgCode.REQUEST_DENY)
        })

    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@app.route('/userDel', methods=['POST'])
def user_del(action=ActionCode.DELETE_USER):
    request_id = request.values.get("request_id")

    if RequestProtection.is_allow(action, request_id):
        user_id = request.values.get("user_id")
        action_result = DbManager.del_user_by_id(user_id)
        if action_result.msg_code == MsgCode.DELETE_SUCC:
            resp = jsonify({
                "action": action_result.action_code,
                "status": action_result.msg_code,
                "resp_msg": MsgCode.get_message(action_result.msg_code)
            })
        else:
            resp = jsonify({
                "action": action_result.action_code,
                "status": action_result.msg_code,
                "resp_msg": MsgCode.get_message(action_result.msg_code)
            })
    else:
        # 访问被拒绝
        resp = jsonify({
            "action": action,
            "status": MsgCode.REQUEST_DENY,
            "resp_msg": MsgCode.get_message(MsgCode.REQUEST_DENY)
        })
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
