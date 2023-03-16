from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class QuestionForm(FlaskForm):
    title = StringField("Title of the Question: ", validators=[DataRequired()])
    body = TextAreaField("Your question: ", validators=[DataRequired()])
    submit = SubmitField("Authorize")