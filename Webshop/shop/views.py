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
from django.http import HttpResponse
from django.template import loader

item_count = []
items_by_name = []
items_by_price = []


def products(request):
    product_list = Product.objects.all()
    products = Product.objects.all().order_by('product_name').order_by('price')

    if request.method == "GET":
        print("NAME")
        response_json = request.GET
        response_json = json.dumps(response_json)
        data = json.loads(response_json)
        print("data: ", data)
        my_products_by_name = []
        for key, value in data.items():
            print("key: ", key)
            print("value, ", value)
            keyword = value
            my_products_by_name = Product.objects.filter(Q(product_name__icontains=keyword) |
            Q(code__icontains=keyword) 
            ).order_by('product_name').order_by('price')
            product_list = Product.objects.filter(Q(product_name__icontains=keyword) |
            Q(code__icontains=keyword)).order_by('product_name').order_by('price')
    if item_count:
        count = item_count[0]
    else:
        count = 0
    return render(request, "index.html", {"product_list": product_list, "items": count, "my_products":my_products_by_name})


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
    return redirect(request, "shopping_cart.html", context)

#change to search by code
#implement sorting by name and price

def search_by_code(request):
    if request.method == "GET":
        print("PRICE")
        response_json = request.GET
        response_json = json.dumps(response_json)
        data = json.loads(response_json)
        print("data", data)
        for value in data:
            arr = value.split(",")
        min_arr = arr[0].split(":")
        max_arr = arr[1].split(":")
        min_arr[1] = min_arr[1].replace("{", "")
        min_arr[1] = min_arr[1].replace("}", "")
        min_arr[1] = min_arr[1].strip('"')
        min_val = Decimal(min_arr[1])
        max_arr[1] = max_arr[1].replace("{", "")
        max_arr[1] = max_arr[1].replace("}", "")
        max_arr[1] = max_arr[1].strip('"')
        max_val = Decimal(max_arr[1])

        my_products_by_price = Product.objects.all().filter(
            price__range=[min_val, max_val]
        )
        #implement sorting by name and price
        print("my_products_by_price", my_products_by_price)
        items_by_price.clear()
        for obj in my_products_by_price:
            items_by_price.append(obj)
        context = {"my_products": my_products_by_price}
        t = loader.get_template('search.html')
    return redirect(request, "search_by_code.html", {"my_products": my_products_by_price})
    # else:
    #     return redirect("/")
    # return redirect("/")


def search_by_name(request):
    if request.method == "GET":
        print("NAME")
        response_json = request.GET
        response_json = json.dumps(response_json)
        data = json.loads(response_json)
        for value in data:
            arr = value.split(":")
        arr[1] = arr[1].replace("{", "")
        arr[1] = arr[1].replace("}", "")
        arr[1] = arr[1].strip('"')
        product_name = arr[1]

        my_products_by_name = Product.objects.all().filter(product_name=product_name).order_by('product_name').order_by('price')
        print(my_products_by_name)
        items_by_name.clear()
        for obj in my_products_by_name:
            items_by_name.append(obj)
        context = {"my_products": my_products_by_name}
    return render(request, "search_by_name.html", {"my_products": my_products_by_name})
    # else:
    #     return redirect("/")
    # return redirect("/")


class SearchView(View):
    model = Product
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        if items_by_name:
            context["my_products"] = items_by_name
        elif items_by_price:
            context["my_products"] = items_by_price
        else:
            context["my_products"] = {}
        return context
