from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, EmailField, RadioField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, Email


class JobApplicationForm(FlaskForm):
    first_name = StringField('First Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    last_name = StringField('Last Name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    cover_letter_name = StringField('Cover Letter Title',
                            validators=[DataRequired(), Length(min=2, max=128)])
    cover_letter = FileField('Upload Cover Letter', validators=[FileAllowed(['pdf', 'docx']), FileRequired()])

    resume_name = StringField('Resume Title',
                            validators=[DataRequired(), Length(min=2, max=128)])
    resume = FileField('Upload Resume', validators=[FileAllowed(['pdf', 'docx']), FileRequired()])
    submit = SubmitField('Apply')
