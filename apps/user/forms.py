import wtforms
from flask import flash
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email

from apps.user.models import User


class UserForm(FlaskForm):
    initial = [("", "---------")]
    MANAGER_CHOICES = initial + [(manager_user.id, manager_user.username) for manager_user in
                       User.query.filter(User.usertype == "manager").all()]
    SUPERVISOR_CHOICES = initial + [(user.id, user.username) for user in User.query.filter(User.usertype == "supervisor").all()]
    ASS_SUPERVISOR_CHOICES = initial + [
        (user.id, user.username) for user in User.query.filter(User.usertype == "ass_supervisor").all()]

    first_name = wtforms.StringField("First Name", validators=[DataRequired()])
    last_name = wtforms.StringField("Last Name", validators=[DataRequired()])
    username = wtforms.StringField("Username", validators=[DataRequired()])
    email = wtforms.EmailField("Email", validators=[Email()])
    phone = wtforms.StringField("Phone")
    password = wtforms.PasswordField("Password", validators=[DataRequired()])
    usertype = wtforms.SelectField("User Type", validators=[DataRequired()], choices=User.USER_TYPE, coerce=str)
    manager_id = wtforms.SelectField("Manager", choices=tuple(MANAGER_CHOICES))
    supervisor_id = wtforms.SelectField("Supervisor", choices=tuple(SUPERVISOR_CHOICES))
    ass_supervisor_id = wtforms.SelectField("Assistant Supervisor", choices=tuple(ASS_SUPERVISOR_CHOICES))


class UserLoginForm(FlaskForm):
    username = wtforms.StringField("Username", validators=[DataRequired()])
    password = wtforms.PasswordField("Password", validators=[DataRequired()])
    remember_me = wtforms.BooleanField("Remember Me", default=False)
