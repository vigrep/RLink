
# 用户注册
from flask_login import login_user

from app.email.Email import send_account_confirm_email
from app.model import StatusCode, ActionCode, MsgCode
from app.model.ActionResult import ActionResult
from app.model.Models import User


def register_user(username, email, password, action=ActionCode.REGISTER_USER):
    # 判断注册信息是否传入
    if username is None or username == "":
        return ActionResult(action, StatusCode.FAILED, MsgCode.EMAIL_IS_NULL)
    if email is None or email == "":
        return ActionResult(action, StatusCode.FAILED, MsgCode.EMAIL_IS_NULL)
    if password is None or password == "":
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_PASSWORD_IS_NULL)

    # 用户名合法
    if not check_user_name_valid(username):
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NAME_INVALID)
    # 用户名不能重复
    if check_user_name_duplicate(username):
        return ActionResult(action, StatusCode.FAILED, MsgCode.USER_NAME_DUPLICATE)
    # 邮箱合法
    if not check_user_email_valid(email):
        return ActionResult(action, StatusCode.FAILED, MsgCode.EMAIL_IS_INVALID)
    # 邮箱已注册
    if check_user_email_duplicate(email):
        return ActionResult(action, StatusCode.FAILED, MsgCode.EMAIL_DUPLICATE)

    user = User()
    user.name = username
    user.email = email
    user.set_password(password)

    # 保存到数据库中
    ok = user.save()

    if ok:
        # 发送邮箱账户确认邮件
        send_account_confirm_email(user)

        # 静默登录用户, 方便用户从邮箱中点击确认链接时，不用重新登录，即可认证成功, 因为为了确保安全，认证视图函数要求登录权限才能操作
        login_user(user)

        return ActionResult(action, StatusCode.SUCCESS, MsgCode.REGISTER_SUCC)
    else:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REGISTER_FAILED)


def login(username, password, remember_me, action=ActionCode.LOGIN):
    user = User.query.filter_by(name=username).first()
    if user is None:
        print("邮箱")
        user = User.query.filter_by(email=username).first()
        if user is not None and user.check_password(password):
            print("邮箱 密码成功")
            user.login_count += 1
            user.dingding()
            user.save()
            login_user(user, remember=remember_me)
            return ActionResult(action, StatusCode.SUCCESS, MsgCode.LOGIN_SUCC)
        else:
            print("邮箱 密码失败")
            return ActionResult(action, StatusCode.FAILED, MsgCode.LOGIN_FAILED)
    elif user.check_password(password):
        print("用户名 密码成功")
        user.login_count += 1
        user.save()
        login_user(user, remember=remember_me)
        return ActionResult(action, StatusCode.SUCCESS, MsgCode.LOGIN_SUCC)
    else:
        print("用户名 密码失败")
        return ActionResult(action, StatusCode.FAILED, MsgCode.LOGIN_FAILED)


def check_user(username, password):
    user = User.query.filter_by(name=username).first()
    if user is None:
        user = User.query.filter_by(email=username).first()
        return user is not None and user.check_password(password)
    else:
        return user.check_password(password)


def validate_username(username):
    user = User.query.filter_by(name=username).first()
    return user is None


def validate_email(email):
    user = User.query.filter_by(email=email).first()
    return user is None


# TODO[jj]: 完善方法
def check_user_name_valid(name):
    """
    检测用户名是否非法

    以下情况均视为非法：
    系统保留名称（Rlink等）、政治性、
    :param name:
    :return:
    """

    # FIXME: 具体实现
    return True


def check_user_name_duplicate(name, except_id=None):
    """
    检测用户名是否已经存在
    :param name: 要检测的用户名
    :param except_id: 排除的用户，不参与用户名是否存在的比较，一般更新用户名时传入该参数
    :return: True: 重复，False：没有重复
    """
    if except_id is not None:
        result = User.query.filter(User.name == name).filter(User.id != except_id).first()
    else:
        result = User.query.filter_by(name=name).first()
    return result is not None


# TODO[jj]: 完善方法
def check_user_email_valid(email):
    """
    检测邮箱账号是否非法

    :param name:
    :return:
    """

    # FIXME: 具体实现
    return True


def check_user_email_duplicate(email, except_id=None):
    """
    检测邮箱是否已经存在
    :param email: 要检测的邮箱
    :return: True: 重复，False：没有重复
    """
    if except_id is not None:
        result = User.query.filter(User.email == email).filter(User.id != except_id).first()
    else:
        result = User.query.filter_by(email=email).first()
    return result is not None
