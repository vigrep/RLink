from app.model import ActionCode, StatusCode, MsgCode
from app.model.ActionResult import ActionResult, DictData
from app.request.RequestParam import RequestParam, Field, JsonField, ValidationError


class WorthyLinkGetParam(RequestParam):
    page = Field(key='page', nullable=False)
    page_size = Field(key='page_size', nullable=False)

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
            return ActionResult(ActionCode.GET_SECOND_LINK, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.GET_SECOND_LINK, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)


class SearchCategoryParam(RequestParam):
    wd = Field(key='wd', nullable=False)


class SearchParam(RequestParam):
    wd = Field(key='wd', nullable=False)
    page = Field(key='page', nullable=False)
    page_size = Field(key='page_size', nullable=False)
    category_id = Field(key='category_id', nullable=False)

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

    def validate_category_id(self, category_id):
        try:
            category_id_int = int(category_id.data)
            category_id.data = category_id_int
        except:
            raise ValidationError("category_id", "category_id不是整数")
        else:
            if category_id.data <= 0:
                raise ValidationError("category_id", "category_id必须大于0")

    def pack_result(self):
        if self.is_validate():
            return ActionResult(ActionCode.SEARCH_CATEGORY, StatusCode.SUCCESS, MsgCode.REQUEST_PARAM_CHECK_VALID)
        else:
            data = DictData()
            data.add("errors_info", self.errors)
            return ActionResult(ActionCode.SEARCH_CATEGORY, StatusCode.FAILED, MsgCode.REQUEST_PARAM_CHECK_INVALID, data)
