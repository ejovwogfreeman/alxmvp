from datetime import datetime, timedelta
from email.mime import application
from email.policy import default
import pytz
import jwt
from flask import current_app
from hirehub import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(64))
    profile = db.relationship('Profile', backref='owner', uselist=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    job_posts = db.relationship('JobPost', backref='owner', lazy=True)
    application = db.relationship('JobApplication', backref='applicant', lazy=True)


    '''Function to generate user token
    Using pyjwt but authlib is also a good candidate for this functionality'''
    def get_reset_token(self, expiration=600):
        without_timezone = datetime.now()
        timezone = pytz.timezone("UTC")
        with_timezone = timezone.localize(without_timezone)
        reset_token = jwt.encode(
           {
               "confirm": self.id,
               "exp": with_timezone
               + timedelta(seconds=expiration)
                       },
                       current_app.config['SECRET_KEY'],
                       algorithm="HS256"
        )
        return reset_token

    ''' Using pyjwt instead'''
    @staticmethod
    def verify_reset_token(token):
        try:
            data = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                leeway=timedelta(seconds=10),
                algorithms=["HS256"]
            )
            user_id = data.get('confirm')
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class JobPost(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(90), nullable=False)
    company_name = db.Column(db.String(128), nullable=False)
    desired_major = db.Column(db.String(128), nullable=False)
    job_desc = db.Column(db.Text, nullable=False)
    job_desc_image = db.Column(db.String(128), nullable=False, default='default.jpg')
    job_file = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(64), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_application = db.relationship('JobApplication', backref='jobpost', lazy='dynamic')


    def __repr__(self):
        return f"JobPost('{self.company_name}', '{self.desired_major}', '{self.job_title}', '{self.job_desc}', '{self.email}', '{self.position}', '{self.date_created}', '{self.date_updated}', '{self.user_id}')"

class Profile(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    major = db.Column(db.String(128))
    company_name = db.Column(db.String(128))
    email = db.Column(db.String(90), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    resume = db.Column(db.String(20), nullable=False)
    resume_description = db.Column(db.Text)
    address = db.Column(db.String(256), nullable=False)
    address_two = db.Column(db.String(256))
    occupation = db.Column(db.String(64))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Profile('{self.first_name}', '{self.last_name}', '{self.major}', '{self.company_name}', '{self.email}', '{self.phone}', '{self.resume}', '{self.resume_description}', '{self.address}', '{self.address_two}', '{self.occupation}', '{self.date_created}', '{self.date_updated}', '{self.user_id}')"



class JobApplication(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(90))
    phone = db.Column(db.String(30))
    cover_letter_name = db.Column(db.String(45))
    cover_letter = db.Column(db.String(20), nullable=False)
    resume_name = db.Column(db.String(45))
    resume = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_post_id = db.Column(db.Integer, db.ForeignKey('job_post.id'), nullable=False)

    def __repr__(self):
        return f"JobApplication('{self.first_name}', '{self.last_name}', '{self.email}', '{self.phone}', '{self.cover_letter_name}', '{self.cover_letter}', '{self.resume_name}', '{self.resume}', '{self.date_created}', '{self.date_updated}', '{self.user_id}', '{self.job_post_id}')"