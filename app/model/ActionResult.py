"""
动作的执行结果封装类
1. 动作代码
2. 动作执行结果信息码
3. 动作执行的结果(数据)

"""
from app.model import ActionCode, StatusCode, MsgCode
from flask import jsonify


# 返回的数据类型
class DataType:
    OBJECT = 0
    LIST_OBJECT = 1
    LIST_DICT = 2
    DICT_OBJECT = 3
    JSON = 4
    STRING = 5
    NUMBER = 6


# 字典类型的数据
# 在python原有dict上再封装了一下
# 使用场景：需要返回多个字段

class DictData:
    data_dict = None

    def __init__(self):
        self.data_dict = dict()

    # 添加key,value
    def add(self, key, value):
        self.data_dict[key] = value
        return self.data_dict

    # 返回key,value
    def items(self):
        return self.data_dict.items()


# Object类型
# 使用场景：原生对象

class ObjData:
    obj = None

    def __init__(self, obj):
        self.obj = obj


class ActionResult:
    action_code = ActionCode.ACTION_UNDEFINED
    status_code = StatusCode.UNKNOWN
    msg_code = MsgCode.MSG_UNDEFINED
    data = None

    def __init__(self, action_code, status_code, msg_code, data=None):
        self.action_code = action_code
        self.status_code = status_code
        self.msg_code = msg_code
        self.data = data

    # 将必要信息和数据打包成dict, 方便应答层使用jsonify() 转换成json
    def pack(self):
        package = dict()
        package["action"] = self.action_code
        package["resp_cd"] = self.status_code
        package["resp_msg_code"] = self.msg_code
        package["resp_msg"] = MsgCode.get_message(self.msg_code)

        # if self.data is not None:
        #     if isinstance(self.data, (list, dict)):
        #         package["total_record"] = len(self.data)
        #     package["data"] = self.data
        if self.data is not None:
            if isinstance(self.data, DictData):
                for key, value in self.data.items():
                    package[key] = value
                return package
            elif isinstance(self.data, ObjData):
                package["obj"] = ObjData
            else:
                raise Exception("pack时data类型目前支持: DictData[字典(dict)]、ObjData[原生对象]")
        else:
            return package

    # FIXME: debug
    # 将必要信息和数据打包成json
    def pack_to_json(self):
        package_json = jsonify(self.pack())
        package_json.headers['Access-Control-Allow-Origin'] = '*'

        return package_json

