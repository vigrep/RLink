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
    # 添加链接Link
    ADD_LINK = 10
    # 更新链接
    UPDATE_LINK = 11
    # 删除链接
    DELETE_LINK = 12
    # 删除多个链接
    DELETE_MULTI_LINK = 13

    # 添加类别
    ADD_CATEGORY = 14
    # 删除类别
    DELETE_CATEGORY = 15
    # 更新类别信息
    UPDATE_CATEGORY = 16
    # 查询类别
    GET_CATEGORY = 17

    # 按关键字搜索
    SEARCH_BY_KEY_WORDS = 18

    # 搜索结果的类别
    SEARCH_CATEGORY = 19

    # 通过json格式的文件批量添加用户
    BATCH_ADD_USER_BY_FILE = 20

    # 通过json格式的文件批量添加链接
    BATCH_ADD_LINK_BY_FILE = 21



