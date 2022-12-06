import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="/templates")

app.config.from_object(os.environ['APP_SETTINGS'])  # export APP_SETTINGS=config.DevelopmentConfig
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

login_manager = LoginManager(app=app)
login_manager.login_view = "user_login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    from apps.user.models import User
    from apps.shop.models import *

    db.create_all()

    # db.session.add(User(username="example"))
    # db.session.commit()
    #
    # users = db.session.execute(db.select(User)).scalars()

from apps.user.views import user_blueprint
from apps.shop.views import shop_blueprint

app.register_blueprint(user_blueprint)
app.register_blueprint(shop_blueprint)
