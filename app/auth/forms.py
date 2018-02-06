from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.model.Models import User


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()],
                           render_kw={"class": "text",
                                      "style": "color: #FFFFFF !important",
                                      "type": "text",
                                      "placeholder": "用户名/邮箱",
                                      "required": "required"})
    password = PasswordField('密码', validators=[DataRequired()],
                             render_kw={"class": "text",
                                        "style": "color: #FFFFFF !important; position:absolute; z-index:100;",
                                        "type": "password",
                                        "placeholder": "密码",
                                        "required": "required"})
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录',
                         render_kw={"class": "text",
                                    "style": "margin:0px; font-size:24px; color:white;",
                                    "type": "submit"})


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(name=username.data).first()
        if user is not None:
            raise ValidationError('用户名重复')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('邮箱已注册')
