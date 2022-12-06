from sqlalchemy import func

from apps import db


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    cities = db.relationship("City", backref="state")

    def __repr__(self):
        return '<State: {}>'.format(self.name)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey("state.id"), nullable=False)
    areazones = db.relationship("AreaZone", backref="city")

    def __repr__(self):
        return '<City: {}>'.format(self.name)


class AreaZone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"), nullable=False)
    shop = db.relationship("Shop", backref="areazone")

    def __repr__(self):
        return '<AreaZone: {}>'.format(self.name)

class ShopCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    shop = db.relationship("Shop", backref="shop_category")

    def __repr__(self):
        return '<ShopCategory: {}>'.format(self.name)


shop_employee = db.Table(
    "shop_employee",
    db.Column("employee_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("shop_id", db.Integer, db.ForeignKey("shop.id"), primary_key=True),
)


class Shop(db.Model):
    from apps.user.models import User
    SHOP_STATUS = (
        ("created", "Created"),
        ("bought", "Bought"),
        ("bought_and_rent", "Bought and On Rent")
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    areazone_id = db.Column(db.Integer, db.ForeignKey(AreaZone.id), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey(ShopCategory.id), nullable=False)
    created = db.Column(db.DateTime, nullable=False, server_default=func.now())
    updated = db.Column(db.DateTime, nullable=False, onupdate=func.now(), server_default=func.now())
    employees = db.relationship(User, secondary=shop_employee)

    def __repr__(self):
        return '<Shop: {}>'.format(self.name)
