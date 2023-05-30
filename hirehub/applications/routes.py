import email
from email.mime import application
import os
from fileinput import filename
from sqlite3 import apilevel
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from hirehub import db, bcrypt
from hirehub.jobposts.routes import job_post
from hirehub.models import User, JobPost, Profile, JobApplication
from flask import current_app
from werkzeug.utils import secure_filename
from hirehub.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm, UpdateProfileForm, ProfileForm,
                                   RequestResetForm, ResetPasswordForm)
from hirehub.applications.forms import JobApplicationForm
from hirehub.users.routes import profile
from hirehub.users.utils import save_picture, send_reset_email, save_file
from hirehub.applications.utils import save_file_cover_letter, save_file_resume

applications = Blueprint('applications', __name__)

@applications.route("/apply/<job_post_id>", methods=['GET', 'POST'])
@login_required
def apply(job_post_id):
    if current_user.role != 'student':
        abort(403)
    #@TODO
    # application = JobApplication.query.filter_by(user_id=current_user.id).first()
    # if application.job_post_id:
    #     flash('You already applied for this job', 'danger')
    job_post = JobPost.query.get(job_post_id)
    form = JobApplicationForm()
    if form.validate_on_submit():
        cover_letter = request.files.get('cover_letter')
        resume = request.files.get('resume')
        if not cover_letter and not resume:
            flash('No file selected', 'danger')
            return redirect(url_for('users.new_profile'))
        if form.resume.data:
            cover_letter_file = save_file_cover_letter(cover_letter)
            resume_file = save_file_resume(resume)
        job_application = JobApplication(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, phone=form.phone.data, cover_letter_name=form.cover_letter_name.data, cover_letter=cover_letter_file, resume_name=form.resume_name.data, resume=resume_file, user_id=current_user.id, job_post_id=job_post_id)
        #print(nothing)
        db.session.add(job_application)
        db.session.commit()
        flash('Your application has been sent successfully', 'success')
        #return redirect(url_for('applications.my_applications'))
    return render_template('job_application.html', job_post=job_post, form=form, legend='Application Form')

@applications.route("/my_applications/<string:username>")
@login_required
def my_applications(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    # job_post = JobPost.query.filter_by(user_id=user.id).first()
    # job_applications = JobApplication.query.filter_by(applicant=user).order_by(JobApplication.date_updated.desc())
    # paginated_results = job_applications.paginate(page=page, per_page=5)
    applications = JobApplication.query.filter_by(user_id=user.id)
    temp_arr = []
    for app in applications:
        temp_arr.append(app.job_post_id)
    final_new_temp_arr = list(dict.fromkeys(temp_arr))
    selected_jobs = []
    for i in final_new_temp_arr:
        job = JobPost.query.get(i)
        selected_jobs.append(job)
    #print(nothing)
    return render_template('my_applications.html', selected_jobs=selected_jobs, user=user)

@applications.route("/applicant/<int:job_post_id>/<int:user_id>")
@login_required
def applicant(job_post_id, user_id):
    page = request.args.get('page', 1, type=int)
    user = User.query.get_or_404(user_id)
    application = JobApplication.query.filter_by(user_id=user_id,job_post_id=job_post_id).all()[0]
    #profile = Profile.query.get_or_404()
    #print(nothing)
    #job_posts = JobPost.query.filter_by(user_id=current_user.id).order_by(JobPost.date_updated.desc()).paginate(page=page, per_page=5)
    image_file = url_for('static', filename='profile_pics/' + user.image_file)
    cover_letter_file = url_for('static', filename = 'cover_letters/' + application.cover_letter)
    resume_file = url_for('static', filename = 'resume_application_files/' + application.resume)
    return render_template('applicant.html', application=application, cover_letter_file=cover_letter_file, resume_file=resume_file, user=user, image_file=image_file)



# @users.route("/register", methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user = User(username=form.username.data, email=form.email.data, role=form.role.data, password=hashed_password)
#         db.session.add(user)
#         db.session.commit()
#         flash('Your account has been created! You are now able to log in', 'success')
#         return redirect(url_for('users.login'))
#     return render_template('register.html', title='Register', form=form)


# @users.route("/login", methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get('next')
#             return redirect(next_page) if next_page else redirect(url_for('main.home'))
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('login.html', title='Login', form=form)


# @users.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for('main.home'))


# @users.route("/account", methods=['GET', 'POST'])
# @login_required
# def account():
#     form = UpdateAccountForm()
#     if form.validate_on_submit():
#         if form.picture.data:
#             picture_file = save_picture(form.picture.data)
#             current_user.image_file = picture_file
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('Your account has been updated!', 'success')
#         return redirect(url_for('users.account'))
#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
#     return render_template('account.html', title='Account',
#                            image_file=image_file, form=form)

# @users.route("/profile/new", methods=['GET', 'POST'])
# @login_required
# def new_profile():
#     if current_user.profile:
#         return redirect(url_for('users.profile'))
#     form = ProfileForm()
#     if form.validate_on_submit():
#         file = request.files.get('resume')
#         if not file:
#             flash('No file selected', 'danger')
#             return redirect(url_for('users.new_profile'))
#         if form.resume.data:
#             resume_file = save_file(file)
#         profile = Profile(first_name=form.first_name.data, last_name=form.last_name.data, major=form.major.data, company_name=form.company_name.data, email=form.email.data, phone=form.phone.data, resume=resume_file, resume_description=form.resume_description.data, address=form.address.data, address_two=form.address_two.data, occupation=form.occupation.data, owner=current_user)
#         db.session.add(profile)
#         db.session.commit()
#         flash('Your profile has been created!', 'success')
#         return redirect(url_for('users.profile'))
#     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
#     return render_template('create_profile.html', title='Create Profile',
#                            form=form, legend='Create Profile', image_file=image_file)

# @users.route("/profile", methods=['GET', 'POST'])
# @login_required
# def profile():
#     form = UpdateProfileForm()
#     if not current_user.profile:
#         return redirect(url_for('users.new_profile'))
#     if form.validate_on_submit():
#         file = request.files.get('resume')
#         # print(nothing)
#         if form.resume.data:
#             doc_file = save_file(file)
#             current_user.profile.resume = doc_file
#         current_user.profile.first_name = form.first_name.data
#         current_user.profile.last_name = form.last_name.data
#         current_user.profile.major = form.major.data
#         current_user.profile.company_name = form.company_name.data
#         current_user.profile.email = form.email.data
#         current_user.profile.phone = form.phone.data
#         current_user.profile.resume_description = form.resume_description.data
#         current_user.profile.address = form.address.data
#         current_user.profile.address_two = form.address_two.data
#         current_user.profile.occupation = form.occupation.data
#         db.session.commit()
#         flash('Your profile has been updated!', 'success')
#         return redirect(url_for('users.profile'))
#     elif request.method == 'GET':
#         form.first_name.data = current_user.profile.first_name
#         form.last_name.data = current_user.profile.last_name
#         form.major.data = current_user.profile.major
#         form.company_name.data = current_user.profile.company_name
#         form.email.data = current_user.profile.email
#         form.phone.data = current_user.profile.phone
#         form.resume_description.data = current_user.profile.resume_description
#         form.address.data = current_user.profile.address
#         form.address_two.data = current_user.profile.address_two
#         form.occupation.data = current_user.profile.occupation
#     image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
#     resume_file = url_for('static', filename = 'resume_files/' + current_user.profile.resume)
#     return render_template('profile.html', title='Update Profile Info.', form=form, resume_file=resume_file, image_file=image_file, legend='Profile Info')


# @users.route("/user/<string:username>")
# def user_posts(username):
#     page = request.args.get('page', 1, type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     job_posts = JobPost.query.filter_by(owner=user)\
#         .order_by(JobPost.date_posted.desc())\
#         .paginate(page=page, per_page=5)
#     return render_template('user_job_posts.html', job_posts=job_posts, user=user)


# @users.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent with instructions to reset your password.', 'info')
#         return redirect(url_for('users.login'))
#     return render_template('reset_request.html', title='Reset Password', form=form)


# @users.route("/reset_password/<token>", methods=['GET', 'POST'])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for('main.home'))
#     user = User.verify_reset_token(token)
#     print(f'User is', user)
#     if user is None:
#         flash('That is an invalid or expired token', 'warning')
#         return redirect(url_for('users.reset_request'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         user.password = hashed_password
#         db.session.commit()
#         flash('Your password has been updated! You are now able to log in', 'success')
#         return redirect(url_for('users.login'))
#     return render_template('reset_token.html', title='Reset Password', form=form)

