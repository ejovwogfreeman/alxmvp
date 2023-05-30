import email
from email.mime import application
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from hirehub import db
from hirehub.models import JobApplication, JobPost, User
from hirehub.jobposts.forms import JobPostForm
from hirehub.jobposts.utils import save_image_flyer, save_job_file

job_posts = Blueprint('job_posts', __name__)

@job_posts.route("/my_job_posts")
def my_job_posts():
    users = User.query.all()
    page = request.args.get('page', 1, type=int)
    job_posts = JobPost.query.filter_by(user_id=current_user.id).order_by(JobPost.date_updated.desc()).paginate(page=page, per_page=5)
    applications = JobApplication.query.all()
    return render_template('job_posts.html', job_posts=job_posts, users=users, applications=applications)

@job_posts.route("/job_post/new", methods=['GET', 'POST'])
@login_required
def new_job_post():
    if current_user.role != 'recruiter':
        abort(401)
    form = JobPostForm()
    if form.validate_on_submit():
        if form.job_desc_image.data:
            image_flyer = save_image_flyer(form.job_desc_image.data)
        file = request.files.get('job_file')
        if not file:
            flash('No file selected', 'danger')
            return redirect(url_for('job_posts.new_job_post'))
        if form.job_file.data:
            job_file_doc = save_job_file(file)
        job_post = JobPost(job_title=form.job_title.data, company_name=form.company_name.data, desired_major=form.desired_major.data, job_desc=form.job_desc.data, job_desc_image=image_flyer, job_file=job_file_doc, email=form.email.data, position=form.position.data, user_id=current_user.id)
        db.session.add(job_post)
        db.session.commit()
        flash('Your job post has been created successfully!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_job_post.html', title='New Job Post', form=form, legend='New Job Post')


@job_posts.route("/job_post/<int:job_post_id>")
def job_post(job_post_id):
    job_post = JobPost.query.get_or_404(job_post_id)
    return render_template('job_post.html', title=job_post.job_title, job_post=job_post)


@job_posts.route("/job_post/<int:job_post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(job_post_id):
    job_post = JobPost.query.get_or_404(job_post_id)
    if job_post.owner != current_user and current_user.role != 'recruiter':
        abort(403)
    form = JobPostForm()
    if form.validate_on_submit():
        if form.job_desc_image.data:
            image_flyer = save_image_flyer(form.job_desc_image.data)
            job_post.job_desc_image = image_flyer
        file = request.files.get('job_file')
        if form.job_file.data:
            job_file_doc = save_job_file(file)
            job_post.job_file = job_file_doc
        job_post.job_title = form.job_title.data
        job_post.company_name = form.company_name.data
        job_post.desired_major = form.desired_major.data
        job_post.job_desc = form.job_desc.data
        job_post.email = form.email.data
        job_post.position = form.position.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('job_posts.job_post', job_post_id=job_post.id))

    elif request.method == 'GET':
        form.job_title.data = job_post.job_title
        form.company_name.data = job_post.company_name
        form.desired_major.data = job_post.desired_major
        form.job_desc.data = job_post.job_desc
        form.job_desc_image.data = job_post.job_desc_image
        form.job_file.data = job_post.job_file
        form.email.data = job_post.email
        form.position.data = job_post.position
    image_file = url_for('static', filename='job_desc_images/' + job_post.job_desc_image)
    job_desc_file = url_for('static', filename = 'job_flyers/' + job_post.job_file)
    return render_template('create_job_post.html', title='Update Post',
                           form=form, legend='Update Post', image_file=image_file, job_desc_file=job_desc_file)


@job_posts.route("/job_post/<int:job_post_id>/delete", methods=['POST'])
@login_required
def delete_job_post(job_post_id):
    job_post = JobPost.query.get_or_404(job_post_id)
    if job_post.owner != current_user:
        abort(403)
    db.session.delete(job_post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))       
