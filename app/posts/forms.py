from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import SubmitField, TextAreaField, StringField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    """
    a form for submitting a post
    """
    post_text = TextAreaField('პოსტის ტექსტი')
    media = FileField('ასატვირთი სურათი')
    submit_post = SubmitField('დაპოსტვა')


class CommentForm(FlaskForm):
    """
    a form for submitting comments
    """
    comment_text = TextAreaField('კომენტარის ტექსტი', validators=[DataRequired()])
    post_id = StringField()
    submit_comment = SubmitField('⏎')
