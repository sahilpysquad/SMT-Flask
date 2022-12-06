from flask import Blueprint, render_template, request, redirect, flash, session
from flask.views import View
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from apps import db
from apps.user.forms import UserForm, UserLoginForm
from apps.user.models import User

user_blueprint = Blueprint("user", __name__, template_folder="templates")


class CommonView:

    def __init__(self, model, template_name):
        self.model = model
        self.template_name = template_name


class UserList(CommonView, View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        users = self.model.query.all()
        return render_template(self.template_name, users=users)


class AddUser(CommonView, View):
    methods = ["POST", "GET"]

    def dispatch_request(self):
        form = UserForm()
        if request.method == "POST":
            if form.is_submitted():
                data = request.form.to_dict()
                data.pop("csrf_token")
                # usertype = data.get("usertype")
                # if usertype == "manager":
                #     data.pop("supervisor_id")
                #     data.pop("ass_supervisor_id")
                # elif usertype == "supervisor":
                #     if not data.get("manager_id"):
                #         flash("If you are supervisor then you must select manager.")
                #     else:
                #         data.pop("ass_supervisor_id")
                # elif usertype == "ass_supervisor":
                #     if not data.get("manager_id") or not data.get("supervisor_id"):
                #         flash("Please choose manager and supervisor both.")
                # elif usertype in ["cleaning_worker", "employee_worker", "shop_owner"]:
                #     data.pop("supervisor_id")
                #     data.pop("ass_supervisor_id")
                #     data.pop("manager_id")
                user_obj = User(**data)
                user_obj.password = user_obj.set_password(user_obj.password)
                db.session.add(user_obj)
                db.session.commit()
                return redirect("/user/user-list/")
        return render_template(self.template_name, form=form)


class LoginUser(CommonView, View):
    methods = ["POST", "GET"]

    def dispatch_request(self):
        form = UserLoginForm()
        if request.method == "POST":
            if form.validate_on_submit():
                username = request.form.get("username")
                password = request.form.get("password")
                remember_me = request.form.get("remember_me")
                remember_me = True if remember_me in ["y", "Y"] else False
                user_obj = User.query.filter_by(username=username).first()
                if user_obj and check_password_hash(user_obj.password, password):
                    login_user(user_obj, remember=remember_me)
                    return redirect("/user/user-list/")
                else:
                    flash("Username or Password is incorrect, Please try again..!")
                    return render_template(self.template_name, form=form)
            else:
                return render_template(self.template_name, form=form)
        return render_template(self.template_name, form=form)


class LogoutUser(CommonView, View):
    decorators = [login_required]
    methods = ["GET"]

    def __init__(self, model=None, template_name=None):
        super().__init__(model, template_name)

    def dispatch_request(self):
        logout_user()
        return redirect("/user/login/")
