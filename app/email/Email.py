from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail
from flask import render_template


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject,
                  sender=sender,
                  recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()


def send_account_confirm_email(user):
    subject = "RLink账号确认"
    # sender = str(current_app.config["MAIL_DEFAULT_SENDER"])
    sender = "yad2206@163.com"
    recipients = [user.email]
    token = user.generate_confirmation_token()

    msg = Message(subject,
                  sender=sender,
                  recipients=recipients)

    msg.body = render_template('auth/email/confirm.txt', user=user, token=token)
    msg.html = render_template('auth/email/confirm.html', user=user, token=token)

    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()

