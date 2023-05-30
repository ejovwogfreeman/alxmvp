from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, EmailField, RadioField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired


class JobPostForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired()])
    company_name = StringField('Company Name', validators=[DataRequired()])
    desired_major = StringField('Desired Major', validators=[DataRequired()])
    job_desc = TextAreaField('Job Description', validators=[DataRequired()])
    job_desc_image = FileField('Upload Job Description Flyre', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    job_file = FileField('Upload Job Description File', validators=[FileAllowed(['pdf', 'docx'])])
    email = EmailField('Email', validators=[DataRequired()])
    position = RadioField('Position', choices=[('Full-Time','Full-Time'),('Part-Time','Part-Time'),('Internship','Internship')], validators=[DataRequired()])
    submit = SubmitField('Create Job Post')
