from apps import db


class User(db.Model):
    __tablename__ = "users"

    USER_TYPE = (
        ("manager", "Manager"),
        ("supervisor", "Supervisor"),
        ("ass_manager", "Ass. Supervisor"),
        ("cleaning_worker", "Cleaning Worker"),
        ("employee_worker", "Employee Worker"),
        ("shop_owner", "Shop Owner"),
    )

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    usertype = db.Column(db.String(20), nullable=False)
    manager = db.Column(db.ForeignKey("users.id"), nullable=False)
    supervisor = db.Column(db.ForeignKey("users.id"), nullable=False)
    ass_supervisor = db.Column(db.ForeignKey("users.id"), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=True, nullable=False)

    def __init__(
            self,
            username,
            first_name,
            last_name,
            email,
            password,
            phone,
            user_type,
            manager,
            supervisor,
            ass_supervisor,
            is_active,
            is_verified
    ):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.phone = phone
        self.user_type = user_type
        self.manager = manager
        self.supervisor = supervisor
        self.ass_supervisor = ass_supervisor
        self.is_active = is_active
        self.is_verified = is_verified

    def __repr__(self):
        return '<user {}>'.format(self.username)

    def serializer(self):
        return {
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "password": self.password,
            "phone": self.phone,
            "user_type": dict(self.USER_TYPE).get(self.user_type),
            "manager": self.manager,
            "supervisor": self.supervisor,
            "ass_supervisor": self.ass_supervisor,
            "is_active": self.is_active,
            "is_verified": self.is_verified
        }
