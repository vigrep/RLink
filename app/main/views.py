from flask import render_template, g
from sqlalchemy import func
from datetime import datetime
from flask import request
from flask import jsonify

from app.email.Email import send_account_confirm_email
from app.main import main, business
from flask_login import current_user
from app.main.params import SearchParam, SearchCategoryParam, WorthyLinkGetParam

# @main.before_app_request
# def before_request():
#     if current_user.is_authenticated:
#         current_user.last_login_datetime = datetime.now()
#         current_user.save()
#         # g.search_form = SearchForm()
#     # g.locale = str(get_locale())
from app.model.Models import User


@main.route('/')
@main.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@main.route('/getPrimaryLink', methods=['POST'])
def get_primary_link():
    action_result = business.get_primary_link()

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@main.route('/getWorthyLink', methods=['POST'])
def get_worthy_link():
    param = WorthyLinkGetParam()
    if param.validate_on_submit():
        action_result = business.get_worthy_link(param.page.data, param.page_size.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@main.route('/searchCategory', methods=['POST'])
def search_category():
    param = SearchCategoryParam()
    if param.validate_on_submit():
        action_result = business.search_category(param.wd.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@main.route('/search', methods=['GET', 'POST'])
def search():
    param = SearchParam()
    if param.validate_on_submit():
        action_result = business.search(word=param.wd.data,
                                        page=param.page.data,
                                        page_size=param.page_size.data,
                                        category_id=param.category_id.data)
    else:
        action_result = param.check_result

    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


@main.route('/user/<name>', methods=['POST', 'GET'])
def get_links(name):
    action_result = business.get_links_by_name(name)
    resp = jsonify(action_result.pack())
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp




