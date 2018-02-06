from app.auth import auth, business
from flask import redirect, request, url_for, flash, render_template, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app.email.Email import send_account_confirm_email
from app.model import ActionCode, MsgCode
from app.auth.forms import LoginForm, RegistrationForm


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed', methods=['POST'])
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data

        result = business.login(username, password, remember_me)
        if result.success():
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                print(current_user.confirmed)
                if not current_user.confirmed:
                    print("需要确认 %r" % url_for('auth.unconfirmed'))
                    next_page = url_for('auth.unconfirmed')
                else:
                    print("已经确认")
                    next_page = url_for('main.index')
            print("重定向: %r" % next_page)
            return redirect(next_page)
        else:
            print("失败")
            resp = jsonify(result.pack())
            resp.headers['Access-Control-Allow-Origin'] = '*'
            flash("你输入的帐号或密码不正确，请重新输入。")
            # return resp
            return render_template("auth/login.html", form=form)
    else:
        print("重定向到登录页面")
        # return redirect("auth/login_test.html")
        return render_template("auth/login.html", form=form)


@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        result = business.register_user(username, email, password)
        if result.success():
            return redirect(url_for('auth.login'))
        else:
            resp = jsonify(result.pack())
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp
    else:
        return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm_account(token, action=ActionCode.CONFRIM_ACCOUNT):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm_email_account(token):
        print("确认成功")
    else:
        print("确认失败：链接失效或非法")
    return redirect(url_for('main.index'))


@auth.route('/resendConfirmEmail', methods=['GET', 'POST'])
@login_required
def resend_confirm_email():
    if current_user.is_authenticated and not current_user.confirmed:
        send_account_confirm_email(current_user)
        login_user(current_user)
    return redirect(url_for('auth.login'))


# FIXME
@auth.route('/test', methods=['GET', 'POST'])
def test(action=1):
    print(current_user.id)
    print(current_user.role)
    print(current_user.links)
    return "test..........."

"""
@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
"""
