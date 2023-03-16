from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class AnswerForm(FlaskForm):
    body = TextAreaField("Your Answer: ", validators=[DataRequired()])
    submit = SubmitField("Authorize")