from flask_login import current_user
from app.admin.dao.CategoryManager import check_category_name_duplicate
from app.admin.dao.LinkManager import check_link_valid
from app.admin.dao.RoleManager import check_role_name_duplicate
from app.admin.dao.UserManager import check_user_name_valid, check_user_name_duplicate, check_user_email_valid, \
    check_user_email_duplicate
from app.model import ActionCode, StatusCode, MsgCode
from app.model.ActionResult import ActionResult, DictData
from app.model.Permission import Permission
from app.request.RequestParam import RequestParam, JsonField, Field, ValidationError, ListField


class UserAddParam(RequestParam):
    user_info = JsonField(key='msg_body',
                          nullable=False,
                          must_include=['name', 'password', 'email'])

    def validate_user_info(self, user_info):
        user_info_dict = user_info.data

        # 如果传入了id, 删除掉，因为添加时id字段设置为自增
        if "id" in user_info_dict:
            user_info_dict.pop("id")

        # 检查是否缺少必要的信息
        # 用户名不能为空
        if "name" not in user_info_dict or user_info_dict["name"] == "":
            raise ValidationError("name", "用户名不能为空")
        # 用户名合法
        if not check_user_name_valid(user_info_dict["name"]):
            raise ValidationError("name", "用户名非法")
        # 用户名不能重复
        if check_user_name_duplicate(user_info_dict["name"]):
            raise ValidationError("name", "用户名重复")
        # 密码不能为空
        if "password" not in user_info_dict or user_info_dict["password"] == "":
            raise ValidationError("password", "密码不能为空")
        # 邮箱不能为空
        if "email" not in user_info_dict or user_info_dict["email"] == "":
            raise ValidationError("email", "邮箱不能为空")
        # 邮箱合法
        if not check_user_email_valid(user_info_dict["email"]):
            raise ValidationError("email", "邮箱不合法")
        # 邮箱已注册
        if check_user_email_duplicate(user_info_dict["email"]):
            raise ValidationError("email", "邮箱已注册")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.ADD_USER, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.ADD_USER, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class UserDeleteParam(RequestParam):
    user_ids = ListField(key='user_ids', nullable=False)

    # def validate_user_ids(self, user_ids):
    #     pass

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.DELETE_USER, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.DELETE_USER, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class UserUpdateParam(RequestParam):
    user_info = JsonField(key='msg_body',
                          nullable=False,
                          must_include=['id'])

    def validate_user_info(self, user_info):
        user_info_dict = user_info.data

        # user_id 是否合法
        user_id = user_info_dict["id"]
        try:
            user_id = int(user_id)
        except ValueError:
            raise ValidationError("id", "用户名ID不正确")
        else:
            if user_id <= 0:
                raise ValidationError("id", "用户名ID不正确")

        # 判断user_id 对应的用户是否存在数据库中
        # db_user = UserManager.get_user_model_by_id(user_id)
        # if db_user is None:
        #     raise ValidationError("id", "用户不存在")

        # 检查要修改的值是否符合要求
        if "name" in user_info_dict:
            if user_info_dict["name"] == "":
                raise ValidationError("name", "用户名不能为空")
            if not check_user_name_valid(name=user_info_dict["name"]):
                raise ValidationError("name", "用户名非法")
            if check_user_name_duplicate(user_info_dict["name"], except_id=user_id):
                raise ValidationError("name", "用户名重复")
        if "password" in user_info_dict and user_info_dict["password"] == "":
            raise ValidationError("password", "密码不能为空")
        if "email" in user_info_dict:
            if user_info_dict["email"] == "":
                raise ValidationError("email", "邮箱不能为空")
            if not check_user_email_valid(user_info_dict["email"]):
                raise ValidationError("email", "邮箱不合法")
            if check_user_email_duplicate(user_info_dict["email"], except_id=user_id):
                raise ValidationError("email", "邮箱已注册")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.UPDATE_USER, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.UPDATE_USER, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class UserQueryParam(RequestParam):
    page = Field(key='page', nullable=False)
    page_size = Field(key='page_size', nullable=False)
    conditions = JsonField(key='conditions', nullable=True)

    def validate_page(self, page):
        try:
            page_int = int(page.data)
            page.data = page_int
        except:
            raise ValidationError("page", "page不是整数")
        else:
            if page.data <= 0:
                raise ValidationError("page", "page必须大于0")

    def validate_page_size(self, page_size):
        try:
            page_size_int = int(page_size.data)
            page_size.data = page_size_int
        except:
            raise ValidationError("page_size", "page_size不是整数")
        else:
            if page_size.data <= 0:
                raise ValidationError("page_size", "page_size必须大于0")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.GET_USERS_BY_PAGE, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.GET_USERS_BY_PAGE, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class UserQueryByIdParam(RequestParam):
    user_id = Field(key='user_id', nullable=False)

    def validate_user_id(self, user_id):
        try:
            user_id_int = int(user_id.data)
            user_id.data = user_id_int
        except:
            raise ValidationError("id", "用户ID不正确")
        else:
            if user_id.data <= 0:
                raise ValidationError("id", "用户ID不正确")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.GET_USER_BY_ID, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.GET_USER_BY_ID, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class LinkAddParam(RequestParam):
    link_info = JsonField(key='msg_body',
                          nullable=False,
                          must_include=['name', 'link', 'category_id'])

    def validate_link_info(self, link_info):
        link_info_dict = link_info.data

        # 如果传入了id, 删除掉，因为添加时id字段设置为自增
        if "id" in link_info_dict:
            link_info_dict.pop("id")

        # 检查是否缺少必要的信息
        if "name" not in link_info_dict or link_info_dict["name"] == "":
            raise ValidationError("name", "链接名称不能为空")
        if "link" not in link_info_dict or link_info_dict["link"] == "":
            raise ValidationError("link", "链接地址不能为空")
        if not check_link_valid(link_info_dict["link"]):
            raise ValidationError("link", "链接地址非法")
        if "category_id" not in link_info_dict or link_info_dict["category_id"] == "":
            raise ValidationError("category_id", "类别ID不能为空")

        # 添加操作者ID：当前登录的用户ID
        try:
            link_info_dict["user_id"] = current_user.id
        except:
            raise ValidationError("user_id", "用户ID获取失败，请检查登录状态")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.ADD_LINK, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.ADD_LINK, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class LinkDeleteParam(RequestParam):
    link_ids = ListField(key='link_ids', nullable=False)

    # def validate_link_ids(self, link_ids):
    #     pass

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.DELETE_LINK, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.DELETE_LINK, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class LinkUpdateParam(RequestParam):
    link_info = JsonField(key='msg_body',
                          nullable=False,
                          must_include=['id'])

    def validate_link_info(self, link_info):
        link_info_dict = link_info.data

        # link_id 是否合法
        link_id = link_info_dict["id"]
        try:
            link_id = int(link_id)
        except ValueError:
            raise ValidationError("id", "链接ID不正确")
        else:
            if link_id <= 0:
                raise ValidationError("id", "链接ID不正确")

        # 检查要修改的值是否符合要求
        if "name" in link_info_dict and link_info_dict["name"] == "":
            raise ValidationError("name", "链接名称不能为空")
        if "link" in link_info_dict:
            if link_info_dict["link"] == "":
                raise ValidationError("link", "链接地址不能为空")
            if not check_link_valid(link_info_dict["link"]):
                raise ValidationError("link", "链接地址非法")
        if "category_id" in link_info_dict and link_info_dict["category_id"] == "":
            raise ValidationError("category_id", "类别ID不能为空")
        if "user_id" in link_info_dict:
            link_info_dict.pop("user_id")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.UPDATE_LINK, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.UPDATE_LINK, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class LinkQueryParam(RequestParam):
    page = Field(key='page', nullable=False)
    page_size = Field(key='page_size', nullable=False)
    conditions = JsonField(key='conditions', nullable=True)

    def validate_page(self, page):
        try:
            page_int = int(page.data)
            page.data = page_int
        except:
            raise ValidationError("page", "page不是整数")
        else:
            if page.data <= 0:
                raise ValidationError("page", "page必须大于0")

    def validate_page_size(self, page_size):
        try:
            page_size_int = int(page_size.data)
            page_size.data = page_size_int
        except:
            raise ValidationError("page_size", "page_size不是整数")
        else:
            if page_size.data <= 0:
                raise ValidationError("page_size", "page_size必须大于0")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.GET_LINKS_BY_PAGE, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.GET_LINKS_BY_PAGE, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class LinkQueryByIdParam(RequestParam):
    link_id = Field(key='link_id', nullable=False)

    def validate_link_id(self, link_id):
        try:
            link_id_int = int(link_id.data)
            link_id.data = link_id_int
        except:
            raise ValidationError("id", "链接ID不正确")
        else:
            if link_id.data <= 0:
                raise ValidationError("id", "链接ID不正确")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.GET_LINK_BY_ID, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.GET_LINK_BY_ID, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class CategoryAddParam(RequestParam):
    category_info = JsonField(key='msg_body',
                              nullable=False,
                              must_include=['name'])

    def validate_category_info(self, category_info):
        category_info_dict = category_info.data

        # 如果传入了id, 删除掉，因为添加时id字段设置为自增
        if "id" in category_info_dict:
            category_info_dict.pop("id")

        # 检查是否缺少必要的信息
        if "name" not in category_info_dict or category_info_dict["name"] == "":
            raise ValidationError("name", "类别名称不能为空")
        if check_category_name_duplicate(category_info_dict["name"]):
            raise ValidationError("name", "类别名称重复")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.ADD_CATEGORY, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.ADD_CATEGORY, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class CategoryDeleteParam(RequestParam):
    category_ids = ListField(key='category_ids', nullable=False)

    # def validate_category_ids(self, category_ids):
    #     pass

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.DELETE_CATEGORY, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.DELETE_CATEGORY, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class CategoryUpdateParam(RequestParam):
    category_info = JsonField(key='msg_body', nullable=False, must_include=['id'])

    def validate_category_info(self, category_info):
        category_info_dict = category_info.data

        # category_id 是否合法
        category_id = category_info_dict["id"]
        try:
            category_id = int(category_id)
        except:
            raise ValidationError("id", "类别ID不正确")
        else:
            if category_id <= 0:
                raise ValidationError("id", "类别ID不正确")

        # 检查要修改的值是否符合要求
        if "name" in category_info_dict:
            if category_info_dict["name"] == "":
                raise ValidationError("name", "类别名称不能为空")
            if check_category_name_duplicate(category_info_dict['name'], except_id=category_id):
                raise ValidationError("name", "类别名称重复")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.UPDATE_CATEGORY, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.UPDATE_CATEGORY, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class CategoryQueryParam(RequestParam):
    page = Field(key='page', nullable=False)
    page_size = Field(key='page_size', nullable=False)
    conditions = JsonField(key='conditions', nullable=True)

    def validate_page(self, page):
        try:
            page_int = int(page.data)
            page.data = page_int
        except:
            raise ValidationError("page", "page不是整数")
        else:
            if page.data <= 0:
                raise ValidationError("page", "page必须大于0")

    def validate_page_size(self, page_size):
        try:
            page_size_int = int(page_size.data)
            page_size.data = page_size_int
        except:
            raise ValidationError("page_size", "page_size不是整数")
        else:
            if page_size.data <= 0:
                raise ValidationError("page_size", "page_size必须大于0")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.GET_CATEGORY, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.GET_CATEGORY, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class RoleAddParam(RequestParam):
    role_info = JsonField(key='msg_body',
                              nullable=False,
                              must_include=['name', "permissions"])

    def validate_role_info(self, role_info):
        role_info_dict = role_info.data

        # 如果传入了id, 删除掉，因为添加时id字段设置为自增
        if "id" in role_info_dict:
            role_info_dict.pop("id")

        # 检查是否缺少必要的信息
        if "name" not in role_info_dict or role_info_dict["name"] == "":
            raise ValidationError("name", "角色名称不能为空")
        if check_role_name_duplicate(role_info_dict["name"]):
            raise ValidationError("name", "角色名称重复")
        if "permissions" not in role_info_dict or role_info_dict["permissions"] == "":
            raise ValidationError("name", "角色权限不能为空")
        if not isinstance(role_info_dict["permissions"], list):
            raise ValidationError("name", "角色权限要求数组格式")

        # 将单个权限列表组合成一个权限值(二进制位置1，表示拥有某权限，具体权限原理，详见Permission.py文件）
        role_info.data["permissions"] = Permission.combine_permissions(role_info_dict["permissions"])

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.ADD_ROLE, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.ADD_ROLE, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class RoleDeleteParam(RequestParam):
    role_ids = ListField(key='role_ids', nullable=False)

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.DELETE_ROLE, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.DELETE_ROLE, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class RoleUpdateParam(RequestParam):
    role_info = JsonField(key='msg_body',
                          nullable=False,
                          must_include=['id'])

    def validate_role_info(self, role_info):
        role_info_dict = role_info.data

        # 检查是否缺少必要的信息
        if "name" in role_info_dict:
            if role_info_dict["name"] == "":
                raise ValidationError("name", "角色名称不能为空")
            if check_role_name_duplicate(role_info_dict["name"], except_id=role_info_dict["id"]):
                raise ValidationError("name", "角色名称重复")
        if "permissions" in role_info_dict:
            if role_info_dict["permissions"] == "":
                raise ValidationError("name", "角色权限不能为空")
            if not isinstance(role_info_dict["permissions"], list):
                raise ValidationError("name", "角色权限要求数组格式")
            # 将单个权限列表组合成一个权限值(二进制位置1，表示拥有某权限，具体权限原理，详见Permission.py文件）
            role_info.data["permissions"] = Permission.combine_permissions(role_info_dict["permissions"])

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.UPDATE_ROLE, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.UPDATE_ROLE, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class RoleQueryParam(RequestParam):
    page = Field(key='page', nullable=False)
    page_size = Field(key='page_size', nullable=False)
    conditions = JsonField(key='conditions', nullable=True)

    def validate_page(self, page):
        try:
            page_int = int(page.data)
            page.data = page_int
        except:
            raise ValidationError("page", "page不是整数")
        else:
            if page.data <= 0:
                raise ValidationError("page", "page必须大于0")

    def validate_page_size(self, page_size):
        try:
            page_size_int = int(page_size.data)
            page_size.data = page_size_int
        except:
            raise ValidationError("page_size", "page_size不是整数")
        else:
            if page_size.data <= 0:
                raise ValidationError("page_size", "page_size必须大于0")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.GET_ROLES, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.GET_ROLES, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class WorthyAddParam(RequestParam):
    link_ids = ListField(key='link_ids', nullable=False)

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.ADD_LINK_TO_WORTHY, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.ADD_LINK_TO_WORTHY, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class WorthyDeleteParam(RequestParam):
    worthy_ids = ListField(key='worthy_ids', nullable=False)

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.DELETE_LINK_FROM_WORTHY, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.DELETE_LINK_FROM_WORTHY, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class WorthyUpdateParam(RequestParam):
    worthy_info = JsonField(key='msg_body',
                            nullable=False,
                            must_include=['id'])

    def validate_worthy_info(self, worthy_info):
        worthy_info_dict = worthy_info.data

        # worthy_id 是否合法
        worthy_id = worthy_info_dict["id"]
        try:
            worthy_id = int(worthy_id)
        except ValueError:
            raise ValidationError("id", "推荐ID不正确")
        else:
            if worthy_id <= 0:
                raise ValidationError("id", "推荐ID不正确")

        # 检查要修改的值是否符合要求
        if "img_url" in worthy_info_dict and worthy_info_dict["img_url"] == "":
            raise ValidationError("img_url", "图片URL不能为空")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.UPDATE_PRIMARY_LINK, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.UPDATE_PRIMARY_LINK, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class WorthyQueryParam(RequestParam):
    page = Field(key='page', nullable=False)
    page_size = Field(key='page_size', nullable=False)
    conditions = JsonField(key='conditions', nullable=True)

    def validate_page(self, page):
        try:
            page_int = int(page.data)
            page.data = page_int
        except:
            raise ValidationError("page", "page不是整数")
        else:
            if page.data <= 0:
                raise ValidationError("page", "page必须大于0")

    def validate_page_size(self, page_size):
        try:
            page_size_int = int(page_size.data)
            page_size.data = page_size_int
        except:
            raise ValidationError("page_size", "page_size不是整数")
        else:
            if page_size.data <= 0:
                raise ValidationError("page_size", "page_size必须大于0")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.GET_LINK_FROM_WORTHY, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.GET_LINK_FROM_WORTHY, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)
