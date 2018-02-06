from flask import request
from flask import jsonify
from app.admin import admin
from app.admin.dao import LinkManager, UserManager, RoleManager, CategoryManager, LinkRecommendManager
from app.model.Permission import Permission
from app.admin.params import UserAddParam, UserDeleteParam, UserUpdateParam, UserQueryParam, UserQueryByIdParam, \
    LinkAddParam, LinkDeleteParam, LinkUpdateParam, LinkQueryParam, LinkQueryByIdParam, CategoryAddParam, \
    CategoryDeleteParam, CategoryUpdateParam, CategoryQueryParam, RoleQueryParam, RoleAddParam, RoleDeleteParam, \
    RoleUpdateParam, WorthyAddParam, WorthyDeleteParam, WorthyQueryParam, WorthyUpdateParam
from flask_login import login_required
from app.utils.RequestProtection import permission_required


# 添加用户
@admin.route('/userAdd', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_USER)
def user_add():
    post = UserAddParam()
    if post.validate_on_submit():
        action_result = UserManager.add_user(post.user_info.data)
    else:
        action_result = post.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/userDel', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_USER)
def user_del():
    post = UserDeleteParam()
    if post.validate_on_submit():
        action_result = UserManager.del_users_by_ids(post.user_ids.data)
    else:
        action_result = post.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 修改用户信息
@admin.route('/userUpdate', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_USER)
def user_update():
    param = UserUpdateParam()
    if param.validate_on_submit():
        action_result = UserManager.update_user(param.user_info.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 查询用户
@admin.route('/userSelectAll', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_USER)
def get_users_by_page():
    param = UserQueryParam()
    if param.validate_on_submit():
        action_result = UserManager.get_users_by_page(param.page.data, param.page_size.data, param.conditions.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/getUserById', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_USER)
def get_user_by_id():
    param = UserQueryByIdParam()
    if param.validate_on_submit():
        action_result = UserManager.get_user_by_id(param.user_id.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 添加链接Link
@admin.route('/linkAdd', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_LINK)
def link_add():
    param = LinkAddParam()
    if param.validate_on_submit():
        action_result = LinkManager.add_link(param.link_info.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 删除链接
@admin.route('/linkDel', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_LINK)
def link_del():
    param = LinkDeleteParam()
    if param.validate_on_submit():
        action_result = LinkManager.del_links_by_ids(param.link_ids.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 修改链接信息
@admin.route('/linkUpdate', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_LINK)
def link_update():
    param = LinkUpdateParam()
    if param.validate_on_submit():
        action_result = LinkManager.update_link(param.link_info.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 查询所有链接
@admin.route('/linkSelectAll', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_LINK)
def get_links_by_page():
    param = LinkQueryParam()
    if param.validate_on_submit():
        action_result = LinkManager.get_links_by_page(param.page.data, param.page_size.data, param.conditions.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/getLinkById', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_LINK)
def get_link_by_id():
    param = LinkQueryByIdParam()
    if param.validate_on_submit():
        action_result = LinkManager.get_link_by_id(param.link_id.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 添加类别
@admin.route('/categoryAdd', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_CATEGORY)
def category_add():
    param = CategoryAddParam()
    if param.validate_on_submit():
        action_result = CategoryManager.add_category(param.category_info.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 删除类别
@admin.route('/categoryDel', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_CATEGORY)
def category_del():
    param = CategoryDeleteParam()
    if param.validate_on_submit():
        action_result = CategoryManager.del_category_by_ids(param.category_ids.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 修改类别信息
@admin.route('/categoryUpdate', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_CATEGORY)
def category_update():
    param = CategoryUpdateParam()
    if param.validate_on_submit():
        action_result = CategoryManager.update_category(param.category_info.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 查询所有类别
@admin.route('/categorySelectAll', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_CATEGORY)
def get_categories_by_page():
    param = CategoryQueryParam()
    if param.validate_on_submit():
        action_result = CategoryManager.get_categories_by_page(param.page.data,
                                                               param.page_size.data,
                                                               param.conditions.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/getPermissions', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_ROLE)
def get_permissions():
    action_result = RoleManager.get_permissions()
    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/roleAdd', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_ROLE)
def role_add():
    param = RoleAddParam()
    if param.validate_on_submit():
        action_result = RoleManager.add_role(param.role_info.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/roleDel', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_ROLE)
def role_del():
    param = RoleDeleteParam()
    if param.validate_on_submit():
        action_result = RoleManager.del_roles_by_ids(param.role_ids.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/roleUpdate', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_ROLE)
def role_update():
    param = RoleUpdateParam()
    if param.validate_on_submit():
        action_result = RoleManager.update_role(param.role_info.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/roleSelectAll', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_ROLE)
def get_roles():
    param = RoleQueryParam()
    if param.validate_on_submit():
        action_result = RoleManager.query_roles(param.page.data, param.page_size.data, param.conditions.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# @admin.route('/searchResCategory', methods=['POST'])
# @RequestProtection.logging(level="warn")
# @RequestProtection.allow(action=ActionCode.SEARCH_CATEGORY)
# def search(action=ActionCode.SEARCH_CATEGORY):
#     # request_id = request.values.get("request_id")
#     return "ddddd"


@admin.route('/addUsersFromFile', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_USER)
def add_users_from_json_file():
    # FIXME need test
    file = request.files['json_file']

    action_result = UserManager.add_user_batch(file)

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/addLinksFromFile', methods=['OPTIONS'])
@login_required
@permission_required(Permission.MANAGE_LINK)
def add_links_from_json_file():
    # FIXME need test
    file = request.files['json_file']

    action_result = UserManager.add_user_batch(file)
    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/primaryLinkAdd', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_PRIMARY)
def add_primary_link():
    param = WorthyAddParam()
    if param.validate_on_submit():
        action_result = LinkRecommendManager.add_link_to_primary_table(param.link_ids.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/primaryLinkDel', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_PRIMARY)
def del_primary_link():
    param = WorthyDeleteParam()
    if param.validate_on_submit():
        action_result = LinkRecommendManager.delete_link_from_primary_table(param.worthy_ids.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/primaryLinkUpdate', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_PRIMARY)
def update_primary_link():
    param = WorthyUpdateParam()
    if param.validate_on_submit():
        action_result = LinkRecommendManager.update_primary_link(param.worthy_info.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/primaryLinkSelectAll', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_PRIMARY)
def get_primary_links():
    param = WorthyQueryParam()
    if param.validate_on_submit():
        action_result = LinkRecommendManager.get_link_from_primary_table(param.page.data,
                                                                         param.page_size.data,
                                                                         param.conditions.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/worthyLinkAdd', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_WORTHY)
def add_worthy_link():
    param = WorthyAddParam()
    if param.validate_on_submit():
        action_result = LinkRecommendManager.add_link_to_worthy_table(param.link_ids.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/worthyLinkDel', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_WORTHY)
def del_worthy_link():
    param = WorthyDeleteParam()
    if param.validate_on_submit():
        action_result = LinkRecommendManager.delete_link_from_worthy_table(param.worthy_ids.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@admin.route('/worthyLinkSelectAll', methods=['POST'])
@login_required
@permission_required(Permission.MANAGE_WORTHY)
def get_worthy_links():
    param = WorthyQueryParam()
    if param.validate_on_submit():
        action_result = LinkRecommendManager.get_link_from_worthy_table(param.page.data,
                                                                     param.page_size.data,
                                                                     param.conditions.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
