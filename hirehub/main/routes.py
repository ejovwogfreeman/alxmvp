from flask import render_template, request, Blueprint
from flask_login import current_user
from hirehub.models import JobPost

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    job_posts = JobPost.query.order_by(JobPost.date_updated.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', job_posts=job_posts, current_user=current_user)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
