
import os
from os import environ
from random import random
import secrets
from sqlite3 import connect
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from hirehub import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def save_file(form_file):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_file.filename)
    file_fn = random_hex + f_ext
    file_path = os.path.join(current_app.root_path, 'static/resume_files', file_fn)
    form_file.save(file_path, buffer_size=16384)
    form_file.close()
    return file_fn

def send_reset_email(user):
    token = user.get_reset_token()
    url = url_for('users.reset_token', token=token, _external=True)
    print(url)
#     msg = Message('Password Reset Request',
#                   sender='noreply@demo.com',
#                   recipients=[user.email])
#     msg.body = f'''To reset your password, visit the following link:
# {url_for('users.reset_token', token=token, _external=True)}
# If you did not make this request then simply ignore this email and no changes will be made.
# '''
#     mail.send(msg)

    body = ("Here is a link to reset you password: {}".format(url_for('users.reset_token', token=token, _external=True)))
    # msg = MIMEMultipart('alternative')
    msg = MIMEText(''.join(body))
    msg['Subject'] = "'Password Reset Request"
    msg['From']    = "essaypoint2019@gmail.com"
    msg['To']      = "denniskiplangat.dk@gmail.com"


    s = smtplib.SMTP('smtp.mailgun.org', 587)
    MAIL_GUN_USERNAME = environ.get('MAIL_GUN_USERNAME')
    MAIL_GUN_PASSWORD = environ.get('MAIL_GUN_PASSWORD')

    s.login(MAIL_GUN_USERNAME, MAIL_GUN_PASSWORD)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
