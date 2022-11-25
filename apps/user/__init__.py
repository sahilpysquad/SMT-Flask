from apps import app
from apps.user.views import UserList, AddUser

from .models import User

app.add_url_rule("/user/user-list/", view_func=UserList.as_view("user_list", User, "user_list.html"))
app.add_url_rule("/user/user-add/", view_func=AddUser.as_view("user_add", User, "user_add_form.html"))
