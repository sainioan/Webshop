from django.urls import path
from django.conf.urls import url, include
from . import views
from .views import *
import Webshop

app_name = "shop"

urlpatterns = [
    path("", products, name="index"),
    path("product/<pk>/", ProductView.as_view(), name="product"),
    path("add_to_cart/<pk>/", add_to_cart, name="add_to_cart"),
    path("remove_from_cart/<pk>/", remove_from_cart, name="remove_from_cart"),  
]