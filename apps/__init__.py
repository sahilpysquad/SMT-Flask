import os

from flask import Flask
from flask_migrate import Migrate
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])  # export APP_SETTINGS="config.DevelopmentConfig"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

with app.app_context():
    from apps.user.models import User

    db.create_all()

    # db.session.add(User(username="example"))
    # db.session.commit()
    #
    # users = db.session.execute(db.select(User)).scalars()

from apps.user.views import user_blueprint

app.register_blueprint(user_blueprint)
