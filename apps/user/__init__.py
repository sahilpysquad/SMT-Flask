from apps import app
from apps.user.views import UserList, AddUser, LoginUser, LogoutUser
from .models import User

app.add_url_rule("/user/user-list/", view_func=UserList.as_view("user_list", User, "user_list.html"))
app.add_url_rule("/user/user-add/", view_func=AddUser.as_view("user_add", User, "user_add_form.html"))
app.add_url_rule("/user/login/", view_func=LoginUser.as_view("user_login", User, "user_login_form.html"))
app.add_url_rule("/user/logout/", view_func=LogoutUser.as_view("user_logout"))
