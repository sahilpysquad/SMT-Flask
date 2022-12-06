import wtforms
from flask import flash
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email

from apps.user.models import User


class UserForm(FlaskForm):
    MANAGER_CHOICES = ((user.id, user.username) for user in User.query.filter(User.usertype == "manager").all())
    SUPERVISOR_CHOICES = ((user.id, user.username) for user in User.query.filter(User.usertype == "supervisor").all())
    ASS_SUPERVISOR_CHOICES = (
        (user.id, user.username) for user in User.query.filter(User.usertype == "ass_supervisor").all())

    first_name = wtforms.StringField("First Name", validators=[DataRequired()])
    last_name = wtforms.StringField("Last Name", validators=[DataRequired()])
    username = wtforms.StringField("Username", validators=[DataRequired()])
    email = wtforms.EmailField("Email", validators=[Email()])
    phone = wtforms.StringField("Phone")
    password = wtforms.PasswordField("Password", validators=[DataRequired()])
    usertype = wtforms.SelectField("User Type", validators=[DataRequired()], choices=User.USER_TYPE, coerce=str)
    manager_id = wtforms.SelectField("Manager", choices=MANAGER_CHOICES)
    supervisor_id = wtforms.SelectField("Supervisor", choices=SUPERVISOR_CHOICES)
    ass_supervisor_id = wtforms.SelectField("Assistant Supervisor", choices=ASS_SUPERVISOR_CHOICES)

    def validate(self, *args, **kwargs):
        manager, supervisor, ass_supervisor = self.manager_id.raw_data, self.supervisor_id.raw_data, self.ass_supervisor_id.raw_data
        usertype = self.usertype.raw_data[0]
        valid = True
        if usertype == "manager":
            self.supervisor_id.data, self.ass_supervisor_id.data = None, None
        elif usertype == "supervisor":
            if not manager:
                flash("If you are supervisor then you must select manager.")
                valid = False
            else:
                self.ass_supervisor_id.data = None
        elif usertype == "ass_supervisor":
            if not manager or not supervisor:
                flash("Please choose manager and supervisor both.")
                valid = False
        elif usertype in ["cleaning_worker", "employee_worker", "shop_owner"]:
            self.manager_id.data, self.supervisor_id.data, self.ass_supervisor_id.data = None, None, None
        return valid

    def validate_usertype(self, usertype):
        usertype_data = usertype.data
        if usertype_data == "shop_owner":
            self.manager_id.data, self.manager_id.raw_data = None, None
            self.supervisor_id.data, self.supervisor_id.raw_data = None, None
            self.ass_supervisor_id.data, self.ass_supervisor_id.raw_data = None, None


class UserLoginForm(FlaskForm):
    username = wtforms.StringField("Username", validators=[DataRequired()])
    password = wtforms.PasswordField("Password", validators=[DataRequired()])
    remember_me = wtforms.BooleanField("Remember Me", default=False)
