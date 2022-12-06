from flask import request, redirect, render_template, Blueprint, flash
from flask.views import View
from flask_login import login_required

from apps import db, login_user
from apps.shop.forms import StateForm, CityForm, AreaZoneForm, ShopCategoryForm, ShopForm
from apps.shop.models import State, City, AreaZone, ShopCategory, Shop
from apps.user.models import User
from apps.user.views import CommonView

shop_blueprint = Blueprint("shop", __name__, template_folder="templates")


class StateView(CommonView, View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = StateForm()
        states = self.model.query.all()
        if request.method == "POST":
            if form.validate_on_submit():
                name = request.form.get("name")
                state_obj = State(name=name)
                db.session.add(state_obj)
                db.session.commit()
                return redirect("/states/")
        return render_template(self.template_name, states=states, form=form)


class CityView(CommonView, View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = CityForm()
        cities = self.model.query.all()
        if request.method == "POST":
            data = request.form.to_dict()
            data.pop("csrf_token")
            city_obj = City(**data)
            db.session.add(city_obj)
            db.session.commit()
            return redirect("/cities/")
        return render_template(self.template_name, cities=cities, form=form)


class AreaZoneView(CommonView, View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = AreaZoneForm()
        areazones = self.model.query.all()
        if request.method == "POST":
            data = request.form.to_dict()
            data.pop("csrf_token")
            areazone_obj = AreaZone(**data)
            db.session.add(areazone_obj)
            db.session.commit()
            return redirect("/area-zones/")
        return render_template(self.template_name, areazones=areazones, form=form)


class ShopCategoryView(CommonView, View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = ShopCategoryForm()
        shop_categories = self.model.query.all()
        if request.method == "POST":
            name = request.form.get("name")
            shop_category_obj = ShopCategory(name=name)
            db.session.add(shop_category_obj)
            db.session.commit()
            return redirect("/shop-category/")
        return render_template(self.template_name, shop_categories=shop_categories, form=form)


class ShopView(CommonView, View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        form = ShopForm()
        shops = self.model.query.all()
        if request.method == "POST":
            data = request.form.to_dict()
            data.pop("csrf_token")
            ass_supervisor_id = data.get("ass_supervisor_id")
            shop_count = Shop.query.filter_by(ass_supervisor_id=int(ass_supervisor_id)).count()
            print(shop_count)
            if shop_count > 15:
                flash("This assistant supervisor has 15 shop already. Please select other assistant supervisor.")
                return render_template(self.template_name, shops=shops, form=form)
            owner = data.get("owner_id")
            data.pop("employees") if data.get("employees") else None
            if owner:
                data.update({"status": "bought"})
            else:
                data.update({"status": "created"})
            shop_obj = Shop(**data)
            employees = dict(request.form.lists()).get("employees")
            if employees and data.get("status") == "bought":
                employees = list(map(int, employees))
                employees = User.query.filter(User.id.in_(employees)).all()
                shop_obj.employees.extend(employees)
            db.session.add(shop_obj)
            db.session.commit()
            return redirect("/shop/shop-list/")
        return render_template(self.template_name, shops=shops, form=form)


class ShopUpdateView(CommonView, View):
    methods = ["GET", "POST"]

    def dispatch_request(self, shop_id):
        shop = Shop.query.filter_by(id=shop_id)
        form  = ShopForm()
        if request.method == "POST":
            data = request.form.to_dict()
            data.pop("csrf_token")
            data.pop("employees")
            employees = dict(request.form.lists()).get("employees")
            if employees:
                employees = list(map(int, employees))
                employees = User.query.filter(User.id.in_(employees)).all()
                shop.first().employees = employees
            shop.update(data)
            return redirect("/shop/shop-list/")
        return render_template(self.template_name, shop=shop.first(), form=form)


class ShopDetailView(CommonView, View):

    def dispatch_request(self, shop_id):
        shop = Shop.query.filter_by(id=shop_id).first()
        return render_template(self.template_name, shop=shop)


class ShopDeleteView(CommonView, View):

    def __init__(self, model=None, template_name=None):
        super().__init__(model, template_name)

    def dispatch_request(self, shop_id):
        Shop.query.filter_by(id=shop_id).delete()
        db.session.commit()
        return redirect("/shop/shop-list/")
