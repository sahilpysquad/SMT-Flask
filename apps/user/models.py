from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import generate_password_hash, check_password_hash

from apps import db


class User(db.Model):
    USER_TYPE = (
        ("manager", "Manager"),
        ("supervisor", "Supervisor"),
        ("ass_supervisor", "Ass. Supervisor"),
        ("cleaning_worker", "Cleaning Worker"),
        ("employee_worker", "Employee Worker"),
        ("shop_owner", "Shop Owner"),
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    usertype = db.Column(db.String(20), nullable=False)

    manager_id = db.Column(db.ForeignKey("user.id"), nullable=True)
    manager = db.relationship("User", remote_side=id, backref="user_manager", foreign_keys=[manager_id])

    supervisor_id = db.Column(db.ForeignKey("user.id"), nullable=True)
    supervisor = db.relationship("User", remote_side=id, backref="user_supervisor", foreign_keys=[supervisor_id])

    ass_supervisor_id = db.Column(db.ForeignKey("user.id"), nullable=True)
    ass_supervisor = db.relationship("User", remote_side=id, backref="user_ass_supervisor", foreign_keys=[ass_supervisor_id])

    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated = db.Column(db.DateTime, nullable=False, onupdate=func.now(), server_default=func.now())

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def set_password(self, password):
        password = generate_password_hash(password=password, method="sha256")
        return password

    def check_password(self, user_password, given_password):
        valid = check_password_hash(user_password, given_password)
        return valid

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

    @property
    def is_authenticated(self):
        return True
