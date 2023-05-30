from os import environ

from dotenv import load_dotenv
load_dotenv()

import os
#     #Mail
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = environ.get('MAIL_USERNAME')
MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
MAIL_SENDER_NAME = environ.get('MAIL_SENDER_NAME')
# print("****START****")
# print(MAIL_USERNAME)
# print(MAIL_PASSWORD)
# print(MAIL_SENDER_NAME)
# print("****END******")

SECRET_KEY = environ.get('SECRET_KEY')
uri = environ.get('DATABASE_URL')
if uri.startswith("postgres://"):
    uri = uri.replace('postgres://', 'postgresql://', 1)

SQLALCHEMY_DATABASE_URI = uri
SQLALCHEMY_TRACK_MODIFICATIONS = False