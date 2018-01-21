"""
状态信息码定义
"""
from enum import Enum, unique


@unique
class StatusCode(Enum):

    # 成功
    SUCCESS = "00"

    # 操作需要用户确认
    WAIT_CONFIRM = "A0"

    # 失败
    FAILED = "30"

    # 未知
    UNKNOWN = "90"
