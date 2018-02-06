"""
行为代码定义
"""
from enum import Enum, unique


@unique
class ActionCode(Enum):
    # 未定义
    ACTION_UNDEFINED = -1

    # 获取所有用户信息
    GET_ALL_USERS = 1
    # 根据用户ID获取用户信息
    GET_USER_BY_ID = 2
    # 根据用户名获取用户信息
    GET_USER_BY_NAME = 3
    # 根据页数和每页条数，获取所有用户信息
    GET_USERS_BY_PAGE = 4
    # 添加用户
    ADD_USER = 5
    # 修改用户
    UPDATE_USER = 6
    # 删除用户
    DELETE_USER = 7
    # 删除多个用户
    DELETE_MULTI_USER = 8

    # 根据页数和每页条数，获取所有链接信息
    GET_LINKS_BY_PAGE = 9
    # 根据链接ID获取链接信息
    GET_LINK_BY_ID = 10
    # 添加链接Link
    ADD_LINK = 11
    # 更新链接
    UPDATE_LINK = 12
    # 删除链接
    DELETE_LINK = 13
    # 删除多个链接
    DELETE_MULTI_LINK = 14

    # 添加类别
    ADD_CATEGORY = 15
    # 删除类别
    DELETE_CATEGORY = 16
    # 更新类别信息
    UPDATE_CATEGORY = 17
    # 查询类别
    GET_CATEGORY = 18

    # 按关键字搜索
    SEARCH_BY_KEY_WORDS = 19

    # 搜索结果的类别
    SEARCH_CATEGORY = 20

    # 通过json格式的文件批量添加用户
    BATCH_ADD_USER_BY_FILE = 21

    # 通过json格式的文件批量添加链接
    BATCH_ADD_LINK_BY_FILE = 22

    # 注册用户
    REGISTER_USER = 23
    # 确认账户
    CONFRIM_ACCOUNT = 24

    # 登录
    LOGIN = 25
    # 登录检查
    LOGIN_CHECK = 26
    # 登出
    LOGOUT = 27
    # 检查参数
    REQUEST_PARAM_CHECK = 28

    # 获取权限列表
    GET_PERMISSIONS = 29
    # 添加角色
    ADD_ROLE = 30
    # 删除角色
    DELETE_ROLE = 31
    # 修改角色
    UPDATE_ROLE = 32
    # 查询角色
    GET_ROLES = 33
    # 同步角色
    SYNC_ROLES = 34

    # 添加链接到首要推荐表中
    ADD_LINK_TO_PRIMARY_TABLE = 35
    # 从首要推荐表中删除链接
    DELETE_LINK_FROM_PRIMARY_TABLE = 36
    # 更新首要推荐表中的链接
    UPDATE_PRIMARY_LINK = 37
    # 从首要推荐表中获取链接
    GET_LINK_FROM_PRIMARY_TABLE = 38

    # 添加链接到推荐表中
    ADD_LINK_TO_WORTHY_TABLE = 39
    # 从推荐表中删除链接
    DELETE_LINK_FROM_WORTHY_TABLE = 40
    # 从推荐表中获取链接
    GET_LINK_FROM_WORTHY_TABLE = 41

    # 获取首要推荐链接
    GET_PRIMARY_LINK = 42
    # 获取次要推荐链接
    GET_WORTHY_LINK = 43


