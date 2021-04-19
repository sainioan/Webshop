from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse, HttpResponse
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from decimal import Decimal

item_count = []

# Create your views here.

# def index(request):
#     return render(request, "index.html", {})


def products(request):
    product_list = Product.objects.all()
    if item_count:
        count = item_count[0]
    else:
        count = 0
    return render(request, "index.html", {"product_list": product_list, "items": count})


class ProductView(DetailView):
    model = Product
    template_name = "product.html"

    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        if item_count:
            count = item_count[0]
        else:
            count = 0
        context["items"] = count
        return context


def update_cart(sender, instance, **kwargs):
    line_cost = instance.quantity * instance.product.cost
    instance.cart.count += instance.quantity
    instance.cart.updated = datetime.now()


def add_to_cart(request, pk):
    current_user.clear()
    current_user.append(request.user)
    cart = Cart.objects.get_or_create(user=request.user)

    if request.method == "GET":
        response_json = request.GET
        response_json = json.dumps(response_json)
        data = json.loads(response_json)
        user = request.user
        print(data["cartItem"])
        cartItem = data["cartItem"]

        product_qs = Product.objects.filter(pk=pk)
        if product_qs.exists():
            product = product_qs[0]
        else:
            product = Product.objects.get(pk=pk)
        ci = CartItem.objects.get_or_create(product=product, user=user)
        cart_qs = Cart.objects.filter(user=request.user)
        if cart_qs.exists():
            cart = cart_qs[0]
            if cart.products.filter(
                product__product_name=product.product_name
            ).exists():
                ci[0].quantity = ci[0].quantity + 1
                ci[0].save()
                messages.info(request, "The product was added to your cart.")
                return redirect("shop:shopping_cart")
            else:
                cart_item = CartItem.objects.filter(product=product)[0]
                cart.products.add(cart_item)
                messages.info(request, "The product was added to your cart.")
                return redirect("shop:shopping_cart")
        else:
            date_added = timezone.now()
            ci.date_added = date_added
            ci.product = product
            ci.user = request.user
            cart = Cart.objects.create(user=user, date_added=date_added)
            cart_item = CartItem.objects.filter(product=product)[0]
            cart.products.add(cart_item)
            cart.count = cart.products.count()
            print("cart.count: ", cart.count)
            cart.save()
            messages.info(request, "The product was added to your cart")
            return redirect("shop:shopping_cart")


def remove_from_cart(request, pk):

    if request.method == "GET":
        response_json = request.GET
        response_json = json.dumps(response_json)
        data = json.loads(response_json)
        print(data["cartItem"])
        ci = data["cartItem"]
        ci = CartItem.objects.filter(product_id=pk)[0]
        if ci is None:
            messages.info(request, "The item is not in your shopping cart.")
            return redirect("shop:product", pk=pk)
        ci.reduce_quantity(ci.quantity)
        ci.save()
        return redirect("shop:shopping_cart")


class ShoppingCartView(View):
    def get(self, *args, **kwargs):

        try:
            user = User.objects.get(id=self.request.user.id)
            cart = Cart.objects.get(user=user)
            if cart:
                items = cart.get_items_total()
                item_count.clear()
                item_count.append(items)
            context = {"object": cart}
            return render(self.request, "shopping_cart.html", context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an order")
            return redirect("/")


def shopping_cart(request):
    model = Cart
    template_name = "shopping_cart.html"
    cart = Cart.objects.filter(user=request.user)
    context = {"object": cart}
    return render(request, "shopping_cart.html", context)


def search_by_price(request):
    if request.method == "GET":
        print("PRICE")
        response_json = request.GET
        response_json = json.dumps(response_json)
        data = json.loads(response_json)
        print("data", data)
        print(str(data))
        for key, value in data.items():
            print(key)
            print("value: ", str(value))
        # filter_min = Decimal(data['min'])
        # filter_max = Decimal(data['max'])
        # print("min: ", filter_min)
        # print("max:", filter_max)
        # my_products=Product.objects.filter(price__range(filter_min,filter_max))
        # print(my_products)
        context = {"my_products": ""}
        return render(request, "search.html", context)
    else:
        return redirect("/")
    return redirect("/")


def search_by_name(request):
    if request.method == "GET":
        print("NAME")
        response_json = request.GET
        response_json = json.dumps(response_json)
        data = json.loads(response_json)
        print("response_json", response_json)
        print("data", data)
        # product_name = data['product_name']
        # print("product_name", product_name)
        # my_products=Product.objects.filter(product_name=product_name)
        # print(my_products)
        context = {"my_products": ""}
        return render(request, "search.html", context)
    else:
        return redirect("/")
    return redirect("/")
