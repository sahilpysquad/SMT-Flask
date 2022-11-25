from flask import Blueprint, render_template, request, redirect
from flask.views import View

from apps.user.forms import UserForm

user_blueprint = Blueprint("user", __name__, template_folder="templates")


class UserList(View):
    methods = ["GET", "POST"]

    def __init__(self, model, template_name):
        self.model = model
        self.template_name = template_name

    def dispatch_request(self):
        users = self.model.query.all()
        return render_template(self.template_name, users=users)


class AddUser(View):
    methods = ["POST", "GET"]

    def __init__(self, model, template_name):
        self.model = model
        self.template_name = template_name

    def dispatch_request(self):
        form = UserForm()
        if request.method == "POST":
            data = request.form
            print(data)
            return redirect("/user/user-list/")
        return render_template(self.template_name, form=form)
