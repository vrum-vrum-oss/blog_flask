from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField


class PostForm(FlaskForm):
    title = StringField('Title')
    body = TextAreaField('Body')
    submit = SubmitField('Create')