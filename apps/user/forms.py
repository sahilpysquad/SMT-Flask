import wtforms
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email


class UserForm(FlaskForm):
    first_name = wtforms.StringField("First Name", validators=[DataRequired()])
    last_name = wtforms.StringField("Last Name", validators=[DataRequired()])
    username = wtforms.StringField("Username", validators=[DataRequired()])
    email = wtforms.EmailField("Email", validators=[Email()])
