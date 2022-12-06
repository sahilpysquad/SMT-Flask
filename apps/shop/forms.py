import wtforms
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired

from apps.user.models import User
from apps.shop.models import State, City, Shop, AreaZone, ShopCategory


class StateForm(FlaskForm):
    name = wtforms.StringField("Name", validators=[DataRequired()])


class CityForm(FlaskForm):
    STATE_CHOICES = [(state.id, state.name) for state in State.query.all()]
    name = wtforms.StringField("Name", validators=[DataRequired()])
    state_id = wtforms.SelectField("State", validators=[DataRequired()], choices=STATE_CHOICES)


class AreaZoneForm(FlaskForm):
    CITY_CHOICES = [(city.id, city.name) for city in City.query.all()]
    name = wtforms.StringField("Name", validators=[DataRequired()])
    city_id = wtforms.SelectField("City", validators=[DataRequired()], choices=CITY_CHOICES)


class ShopCategoryForm(FlaskForm):
    name = wtforms.StringField("Name", validators=[DataRequired()])


class ShopForm(FlaskForm):
    AREA_ZONE_CHOICES = [(areazone.id, f"{areazone.name} ({areazone.city.name})") for areazone in AreaZone.query.all()]
    OWNER_CHOICES = [(owner.id, owner.username) for owner in User.query.filter_by(usertype="shop_owner")]
    ASS_SUPERVISOR_CHOICES = [(ass_supervisor.id, ass_supervisor.username) for ass_supervisor in User.query.filter_by(usertype="ass_supervisor")]
    SHOP_CATEGORY_CHOICES = [(category.id, category.name) for category in ShopCategory.query.all()]
    EMPLOYEE_CHOICE = [(employee.id, employee.username) for employee in User.query.filter_by(usertype="employee_worker")]

    name = wtforms.StringField("Name", validators=[DataRequired()])
    areazone_id = wtforms.SelectField("Area Zone", validators=[DataRequired()], choices=AREA_ZONE_CHOICES)
    owner_id = wtforms.SelectField("Owner", validators=[DataRequired()], choices=OWNER_CHOICES)
    ass_supervisor_id = wtforms.SelectField("Ass. Supervisor", validators=[DataRequired()], choices=ASS_SUPERVISOR_CHOICES)
    category_id = wtforms.SelectField("Shop Category", validators=[DataRequired()], choices=SHOP_CATEGORY_CHOICES)
    employees = wtforms.SelectMultipleField("Employee", choices=EMPLOYEE_CHOICE)
