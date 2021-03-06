"""
消息类型代码
"""

###################################
# 常见信息码 负数 - 99
###################################

# 成功
SUCCESS = 00
# 失败
FAILED = -1
# 未知错误
UNKNOWN_ERROR = -2
# 未定义
MSG_UNDEFINED = -3

# 添加成功
ADD_SUCC = 10
# 添加失败
ADD_FAILED = 11

# 查询成功
QUERY_SUCC = 12
# 查询失败
QUERY_FAILED = 13

# 修改成功
UPDATE_SUCC = 14
# 修改失败
UPDATE_FAILED = 15

# 删除成功
DELETE_SUCC = 16
# 删除失败
DELETE_FAILED = 17

# 页数非法
PAGE_INVALID = 18

# 批量添加时部分成功
ADD_PART_SUCC = 19

# 用户注册成功
REGISTER_SUCC = 20
# 注册失败
REGISTER_FAILED = 21

###################################
# 用户操作相关 100-199
###################################

# 用户名重复
USER_NAME_DUPLICATE = 102
# 用户名非法
USER_NAME_INVALID = 103
# 用户密码非法
USER_PASSWORD_INVALID = 104
# 用户不存在
USER_NOT_EXIST = 105
# 用户为空
USER_IS_NULL = 106
# 用户名为空
USER_NAME_IS_NULL = 107
# 用户密码为空
USER_PASSWORD_IS_NULL = 108
# 缺少用户ID
USER_ID_DISMISS = 109
# 邮箱为空
EMAIL_IS_NULL = 110
# 邮箱非法
EMAIL_IS_INVALID = 111
# 邮箱已注册
EMAIL_DUPLICATE = 112
# 登录成功
LOGIN_SUCC = 113
# 登录失败
LOGIN_FAILED = 114

####################################
# 链接操作相关 200 - 299
####################################

# 链接名称为空
LINK_NAME_IS_NULL = 200
# 链接地址为空
LINK_IS_NULL = 201
# 链接非法，不能添加
LINK_INVALID = 202
# 链接实体不存在
LINK_NOT_EXIST = 203
# 缺少链接ID
LINK_ID_DISMISS = 204

####################################
# 分类/类别相关 300 - 399
####################################

# 分类名称为空
CATEGORY_NAME_IS_NULL = 300
# 分类ID缺少
CATEGORY_ID_DISMISS = 301
# 分类名称重复
CATEGORY_NAME_DUPLICATE = 302
# 分类不存在
CATEGORY_NOT_EXIST = 303

####################################
# 搜索相关 400 - 499
####################################

# 搜索成功
SEARCH_SUCC = 400

####################################
# 访问/请求/回应 1000 - 1099
####################################

# 访问被拒绝
REQUEST_DENY = 1001

# 缺少参数
REQUEST_PARAM_NOT_FOUND = 1002

# 参数格式错误
REQUEST_PARAM_ERROR = 1003

# 参数检查通过
REQUEST_PARAM_CHECK_VALID = 1004

# 参数检查未通过
REQUEST_PARAM_CHECK_INVALID = 1005

# 信息码对应的文本信息
MSG_CODE_DICT = {
    # 常见信息
    SUCCESS: "成功",
    UNKNOWN_ERROR: "未知错误",
    MSG_UNDEFINED: "未定义",

    ADD_SUCC: "添加成功",
    ADD_PART_SUCC: "一部分添加成功",
    ADD_FAILED: "添加失败",
    QUERY_SUCC: "查询成功",
    QUERY_FAILED: "查询失败",
    UPDATE_SUCC: "修改成功",
    UPDATE_FAILED: "修改失败",
    DELETE_SUCC: "删除成功",
    DELETE_FAILED: "删除失败",
    PAGE_INVALID: "页数非法",

    # 用户操作
    USER_NAME_DUPLICATE: "用户名重复",
    USER_NAME_INVALID: "用户名非法",
    USER_PASSWORD_INVALID: "用户密码非法",
    USER_NOT_EXIST: "用户不存在",
    USER_IS_NULL: "用户信息为空",
    USER_NAME_IS_NULL: "用户名为空",
    USER_PASSWORD_IS_NULL: "用户密码为空",
    USER_ID_DISMISS: "缺少用户ID",
    EMAIL_IS_NULL: "邮箱为空",
    EMAIL_IS_INVALID: "邮箱账号非法",
    EMAIL_DUPLICATE: "邮箱已注册",
    LOGIN_SUCC: "登录成功",
    LOGIN_FAILED: "登录失败",

    # 链接相关操作
    LINK_IS_NULL: "链接地址为空",
    LINK_NAME_IS_NULL: "链接名称为空",
    LINK_INVALID: "链接非法",
    LINK_NOT_EXIST: "链接不存在",
    LINK_ID_DISMISS: "缺少链接ID",

    # 分类/类别相关
    CATEGORY_ID_DISMISS: "缺少类别ID",
    CATEGORY_NAME_IS_NULL: "类别名为空",
    CATEGORY_NAME_DUPLICATE: "类别名重复",
    CATEGORY_NOT_EXIST: "类别不存在",

    REQUEST_DENY: "访问被拒绝",
    REQUEST_PARAM_NOT_FOUND: "缺少参数",
    REQUEST_PARAM_ERROR: "参数错误",
    REQUEST_PARAM_CHECK_VALID: "参数检查通过",
    REQUEST_PARAM_CHECK_INVALID: "参数检查未通过",
    }


# 信息码转成字符串
def get_message(msg_code):
    if msg_code is not None and msg_code in MSG_CODE_DICT:
        return MSG_CODE_DICT.get(msg_code)
    else:
        return "未定义"


