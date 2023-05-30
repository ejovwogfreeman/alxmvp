
from os import environ

from flask import Flask
import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
# from hirehub.config import Config
from dotenv import load_dotenv



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app():
    
    app = Flask(__name__)

    # app.cli.add_command(commands.do_work)

    #App configurations
    #app.config.from_object(Config)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from hirehub.main.routes import main
    from hirehub.users.routes import users
    from hirehub.jobposts.routes import job_posts
    from hirehub.applications.routes import applications
    
    

    from hirehub.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(job_posts)
    app.register_blueprint(applications)
    app.register_blueprint(errors)

    @click.command(name='create')
    @with_appcontext
    def create():
        db.drop_all()
        db.create_all()
        print('***** Database created ****')
    app.cli.add_command(create)

    return app