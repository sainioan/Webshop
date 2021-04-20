from django.urls import path
from django.conf.urls import url, include
from django.urls import reverse
from . import views
from .views import *
import Webshop

app_name = "shop"

urlpatterns = [
    path("", products, name="index"),
    path("shopping_cart/", ShoppingCartView.as_view(), name="shopping_cart"),
    path("product/<pk>/", ProductView.as_view(), name="product"),
    url(r"^(?P<id>[\w-]+)/$", views.ProductView.as_view(), name="product"),
    path("product/<pk>/add_to_cart/", add_to_cart, name="add_to_cart"),
    path("product/<pk>/remove_from_cart/", remove_from_cart, name="remove_from_cart"),
]