"""
动作的执行结果封装类
1. 动作代码
2. 动作执行结果信息码
3. 动作执行的结果(数据)

"""
from app import ActionCode
from app import MsgCode


# 返回的数据类型
class DataType:
    OBJECT = 0
    LIST_OBJECT = 1
    LIST_DICT = 2
    DICT_OBJECT = 3
    JSON = 4
    STRING = 5
    NUMBER = 6


class ActionResult:
    action_code = ActionCode.ACTION_UNDEFINED
    msg_code = MsgCode.MSG_UNDEFINED
    # data = list()
    data = None

    def __init__(self, action_code, msg_code, data=None):
        self.action_code = action_code
        self.msg_code = msg_code
        self.data = data


