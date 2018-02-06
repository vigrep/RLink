from flask import request, json


class PostMeta(type):
    """
    创建类时，预先将类中含有_post_field属性的属性添加进 cls._param_fields
    """
    def __init__(cls, name, bases, attrs):
        type.__init__(cls, name, bases, attrs)
        cls._param_fields = None

    def __call__(cls, *args, **kwargs):
        """
        dir(cls): 罗列类中的所有属性和方法
        hasattr(cls, 'xxxx'): cls 中是否含有xxxx属性
        """
        if cls._param_fields is None:
            fields = []
            for name in dir(cls):
                if not name.startswith('_'):
                    param_field = getattr(cls, name)
                    if hasattr(param_field, '_request_param_field'):
                        fields.append((name, param_field))
            cls._param_fields = fields

        return type.__call__(cls, *args, **kwargs)


class RequestParam(object, metaclass=PostMeta):
    SUBMIT_METHODS = set(('POST', 'PUT', 'PATCH', 'DELETE'))

    def __init__(self):
        self._fields = self._param_fields
        self._errors = None
        self.success = False

    def is_submitted(self):
        """Consider the form submitted if there is an active request and
        the method is ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
        """
        return bool(request) and request.method in self.SUBMIT_METHODS

    def validate_on_submit(self):
        return self.is_submitted() and self.validate()

    def validate(self):
        """
        检测子类中各个字段是否符合预设要求
        """
        self._errors = None
        self.success = False
        success = True
        for name, field in self._fields:
            # 将子类中定义的 validate_xxx 方法加载进来，传入field.validate（）中
            validator = getattr(self.__class__, 'validate_%s' % name, None)
            if validator is not None:
                extra_validator = validator
            else:
                extra_validator = None

            value = request.values.get(field.key)
            # 检查过程中出现一处错误，均认定检查结果为False
            if not field.validate(self, value, extra_validator):
                success = False
        self.success = success
        return success

    def is_validate(self):
        return self.success

    @property
    def check_result(self):
        if self.pack_result() is None:
            if self._errors is not None and len(self._errors) > 0:
                return self._errors
            else:
                return True
        return self.pack_result()

    def pack_result(self):
        pass

    @property
    def data(self):
        """
        注意：调用validate_on_submit() 方法为False时，不能确保数据正确性
        :return:
        """
        return dict((f.key, f.data) for name, f in self._fields)

    @property
    def errors(self):
        if self._errors is None:
            self._errors = dict((f.key, f.errors) for name, f in self._fields if f.errors)
        return self._errors


# 单值形式的参数，如：name="xxx"
class Field(object):
    _request_param_field = True

    def __init__(self, key=None, nullable=False, default=None):
        self.key = key
        self.nullable = nullable
        self.default = default

        self.data = None
        self.errors = dict()

    def validate(self, request_param, submit_value, extra_validator):
        self.data = None
        self.errors = {}

        # 1. 检查参数是否缺失、格式是否有误
        if submit_value is None or submit_value == "":
            if self.nullable is not None and not self.nullable:
                self.errors[self.key] = "参数为空"
                return False
            elif self.default is not None:
                self.data = self.default
                return True
            else:
                self.data = None
                return True
        # 2. 赋值
        self.data = submit_value

        # 以上检查未通过，不往下走
        if len(self.errors) > 0:
            return False

        # 3. 检查参数值是否合法、有效

        # 实际上调用的是各个继承Field的子类中定义的validate_xxx 方法，其中xxx需要与成员变量名一致
        if extra_validator is not None:
            try:
                extra_validator(request_param, self)
            except StopValidation as e:
                if e.args and e.args[0] and e.args[1]:
                    self.errors[e.args[0]] = e.args[1]
                return True
            except ValueError as e:
                if e.args and e.args[0] and e.args[1]:
                    self.errors[e.args[0]] = e.args[1]

        return len(self.errors) == 0


# 数组形式的参数, 如：ids=[1,2,3]
class ListField(object):
    _request_param_field = True

    def __init__(self, key=None, nullable=False, default=list()):
        self.key = key
        self.nullable = nullable
        self.default = default

        self.data = None
        self.errors = dict()

    def validate(self, request_param, submit_value, extra_validator):
        self.data = None
        self.errors = {}

        # 1. 检查参数是否缺失、格式是否有误
        if submit_value is None or submit_value == "":
            if self.nullable is not None and not self.nullable:
                self.errors[self.key] = "参数为空"
                return False
            elif self.default is not None:
                self.data = self.default
                return True
            else:
                self.data = None
                return True
        try:
            value_list = json.loads(submit_value)
        except:
            self.errors[self.key] = "数组格式有误"
            return False
        if not isinstance(value_list, list):
            self.errors[self.key] = "要求数组格式"
            return False

        # 2. 赋值
        self.data = value_list

        # 以上检查未通过，不往下走
        if len(self.errors) > 0:
            return False

        # 3. 检查参数值是否合法、有效

        # 实际上调用的是各个继承Field的子类中定义的validate_xxx 方法，其中xxx需要与成员变量名一致
        if extra_validator is not None:
            try:
                extra_validator(request_param, self)
            except StopValidation as e:
                if e.args and e.args[0] and e.args[1]:
                    self.errors[e.args[0]] = e.args[1]
                return True
            except ValueError as e:
                if e.args and e.args[0] and e.args[1]:
                    self.errors[e.args[0]] = e.args[1]

        return len(self.errors) == 0


# json格式的参数，如：msg={"xx":""}
class JsonField(object):
    _request_param_field = True

    def __init__(self, key=None, nullable=False, default= None, must_include=list()):
        self.key = key
        self.nullable = nullable
        self.default = default
        self.must_include = must_include

        self.errors = dict()
        self.data = None

    def validate(self, request_param, submit_json, extra_validator):
        """

        :param request_param: RequestParam 引用
        :param submit_json: 需要校验的值
        :param extra_validator: 额外的定义在子类中的具体的校验函数
        :return:
        """
        self.data = None
        self.errors = {}

        # 1. 检查参数是否缺失、格式是否有误
        if submit_json is None or submit_json == "":
            if self.nullable is not None and not self.nullable:
                self.errors[self.key] = "参数为空"
                return False
            elif self.default is not None:
                self.data = self.default
                return True
            else:
                self.data = None
                return True

        try:
            json_dict = json.loads(submit_json)
        except:
            self.errors[self.key] = "json格式有误"
            return False

        if self.must_include is not None and isinstance(self.must_include, list) \
                and len(self.must_include) > 0:
            for filed_key in self.must_include:
                if filed_key not in json_dict:
                    self.errors[filed_key] = "缺失"

        # 2. 赋值
        self.data = json_dict

        # 以上检查未通过，不往下走
        if len(self.errors) > 0:
            return False

        # 3. 检查参数值是否合法、有效

        # 实际上调用的是各个继承Field的子类中定义的validate_xxx 方法，其中xxx需要与成员变量名一致
        if extra_validator is not None:
            try:
                extra_validator(request_param, self)
            except StopValidation as e:
                if e.args and e.args[0] and e.args[1]:
                    self.errors[e.args[0]] = e.args[1]
                return True
            except ValueError as e:
                if e.args and e.args[0] and e.args[1]:
                    self.errors[e.args[0]] = e.args[1]

        return len(self.errors) == 0


class ValidationError(ValueError):
    """
    Raised when a validator fails to validate its input.
    """
    def __init__(self, flag='', message='', *args, **kwargs):
        ValueError.__init__(self, flag, message, *args, **kwargs)


class StopValidation(Exception):
    """
    Causes the validation chain to stop.

    If StopValidation is raised, no more validators in the validation chain are
    called. If raised with a message, the message will be added to the errors
    list.
    """
    def __init__(self, flag='', message='', *args, **kwargs):
        Exception.__init__(self, flag, message, *args, **kwargs)
