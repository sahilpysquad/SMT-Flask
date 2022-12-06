from apps import app
from apps.shop.views import StateView, CityView, AreaZoneView, ShopCategoryView, ShopView, ShopUpdateView, ShopDetailView, ShopDeleteView

from apps.shop.models import State, City, AreaZone, ShopCategory, Shop

app.add_url_rule("/states/", view_func=StateView.as_view("states", State, "states.html"))
app.add_url_rule("/cities/", view_func=CityView.as_view("cities", City, "cities.html"))
app.add_url_rule("/area-zones/", view_func=AreaZoneView.as_view("area_zones", AreaZone, "areazones.html"))

app.add_url_rule("/shop/shop-category/", view_func=ShopCategoryView.as_view("shop_category", ShopCategory, "shop_category.html"))

app.add_url_rule("/shop/shop-add/", view_func=ShopView.as_view("shop_add", Shop, "add_shop_form.html"))
app.add_url_rule("/shop/shop-list/", view_func=ShopView.as_view("shop_list", Shop, "shop_list.html"))
app.add_url_rule("/shop/shop-update/<int:shop_id>", view_func=ShopUpdateView.as_view("shop_update", Shop, "shop_update_form.html"))
app.add_url_rule("/shop/shop-detail/<int:shop_id>", view_func=ShopDetailView.as_view("shop_detail", Shop, "shop_details.html"))
app.add_url_rule("/shop/shop-delete/<int:shop_id>", view_func=ShopDeleteView.as_view("shop_delete"))
