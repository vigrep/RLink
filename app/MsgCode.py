"""
消息类型代码
"""

###################################
# 常见信息码 负数 - 99
###################################

# 成功
SUCCESS = 0
# 未知错误
UNKNOWN_ERROR = -1
# 未定义
MSG_UNDEFINED = -2


###################################
# 用户操作相关 100-199
###################################

# 添加成功
USER_ADD_SUCC = 100
# 添加失败
USER_ADD_FAILED = 101
# 用户名重复
USER_NAME_DUPLICATE = 102
# 用户名非法
USER_NAME_INVALID = 103
# 用户密码非法
USER_PASSWORD_INVALID = 104
# 用户不存在
USER_NOT_EXIST = 105


####################################
# 查询相关 200 - 299
####################################

# 查询成功
QUERY_SUCC = 200

# 查询失败
QUERY_FAILED = 201

# 页数非法
PAGE_INVALID = 202

####################################
# 修改相关 300 - 399
####################################

# 修改成功
UPDATE_SUCC = 300

# 修改失败
UPDATE_FAILED = 301


####################################
# 删除相关 400 - 499
####################################

# 删除成功
DELETE_SUCC = 400

# 删除失败
DELETE_FAILED = 401



####################################
# 访问 1000 - 1099
####################################

# 访问被拒绝
REQUEST_DENY = 1001

# 缺少参数
REQUEST_PARAM_NOT_FOUND = 1002


MSG_CODE_DICT = {
    SUCCESS: "成功",
    UNKNOWN_ERROR: "未知错误",
    MSG_UNDEFINED: "未定义",

    # 用户操作
    USER_ADD_SUCC: "添加成功",
    USER_ADD_FAILED: "添加失败",
    USER_NAME_DUPLICATE: "用户名重复",
    USER_NAME_INVALID: "用户名非法",
    USER_PASSWORD_INVALID: "用户密码非法",
    USER_NOT_EXIST: "用户不存在",

    # 查询操作
    QUERY_SUCC: "查询成功",
    QUERY_FAILED: "查询失败",
    PAGE_INVALID: "页数非法",

    # 修改操作
    UPDATE_SUCC: "修改成功",
    UPDATE_FAILED: "修改失败",

    # 删除操作
    DELETE_SUCC: "删除成功",
    DELETE_FAILED: "删除失败",

    REQUEST_DENY: "访问被拒绝",
    REQUEST_PARAM_NOT_FOUND: "缺少参数",
    }


def get_message(msg_code):
    if msg_code in MSG_CODE_DICT:
        return MSG_CODE_DICT.get(msg_code)
    else:
        return "未定义"


