from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
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

def products(request):
    product_list = Product.objects.all()
    products = Product.objects.all().order_by("product_name").order_by("price")

    if request.method == "GET":
        response_json = request.GET
        response_json = json.dumps(response_json)
        data = json.loads(response_json)
        my_products_by_name = []
        for key, value in data.items():
            print("key: ", key)
            print("value, ", value)
            keyword = value
            my_products_by_name = (
                Product.objects.filter(
                    Q(product_name__icontains=keyword) | Q(code__icontains=keyword)
                )
                .order_by("product_name")
                .order_by("price")
            )
            product_list = (
                Product.objects.filter(
                    Q(product_name__icontains=keyword) | Q(code__icontains=keyword)
                )
                .order_by("product_name")
                .order_by("price")
            )
    if item_count:
        count = item_count[0]
    else:
        count = 0
    return render(
        request,
        "index.html",
        {
            "product_list": product_list,
            "items": count,
            "my_products": my_products_by_name,
        },
    )


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
        if ci.quantity == 0:
            ci.delete()
        return redirect("shop:shopping_cart")

def get_items_in_cart(user):
    user = request.user
    cart = Cart.objects.filter(user=user)
    return cart.objects.get_items_total()

def update_quantity(request, pk):
    
    user = request.user

    if request.method == "GET":
        response_json = request.GET
        response_json = json.dumps(response_json)
        data = json.loads(response_json)
        for key, val in data.items():
            print(key)
            data = key
        print(type(data))
        arr = data.split(',')
        product_name = arr[0].split(":")
        product_name = product_name[1]
        product_name = product_name.strip('"')
        product_name = product_name.strip("\t")
        print(product_name)
        quantity = arr[1].split(":")
        quantity = quantity[1]
        quantity = quantity.strip('"')
        quantity = quantity.strip('"}')
        print(quantity)
        # product_qs = Product.objects.filter(product_name=product_name)
        product_qs = Product.objects.filter(
                    Q(product_name__icontains=product_name) | Q(code__icontains=product_name)
                )
        if product_qs.exists():
           product = product_qs[0]
           cart_qs = Cart.objects.filter(user = user)
           if cart_qs.exists():
                cart = cart_qs[0]
                if cart.products.filter(product=product).exists() :
                    cart_item = CartItem.objects.filter(
                    product = product, user = request.user)[0]
                    if cart_item:
                       cart_item.quantity = int(quantity)     
                       cart_item.save()
                       cart_item.refresh_from_db()
                    if int(quantity) == 0:
                        cart_item.delete()
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


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        cart = Cart.objects.get(user=self.request.user)
        if item_count:
            count = item_count[0]
        else:
            count = 0
        context = {"form": form, "order": cart, "items" : count }
        return render(self.request, "checkout-page.html", context)
