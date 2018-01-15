from app.model.Models import Link
from app.model import ActionCode
from app.model.ActionResult import ActionResult
from app.model.ActionResult import DictData
from app.model import StatusCode
from app.model import MsgCode


# 按关键字搜索
def search(key_words, action=ActionCode.SEARCH_BY_KEY_WORDS):
    if key_words is None:
        return ActionResult(action, StatusCode.FAILED, MsgCode.REQUEST_PARAM_NOT_FOUND)

    # FIXME: 单个关键字，在link的名称和简介中查询匹配的
    result = Link.query.filter(Link.name.like(key_words))
    print(result)
    result = Link.query.filter(Link.name.like(key_words)).all()
    print(result)
    return ActionResult(action, StatusCode.SUCCESS, MsgCode.SEARCH_SUCC)
