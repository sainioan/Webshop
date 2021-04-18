from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse, HttpResponse
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

current_user = []

# Create your views here.

# def index(request):
#     return render(request, "index.html", {})


def products(request):
    product_list = Product.objects.all()
    return render(request, "index.html", {"product_list": product_list})


class ProductView(DetailView):
    model = Product
    template_name = "product.html"


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
        print(data["cartItem"])
        cartItem = data["cartItem"]
        ci = CartItem()
        p_qs = Product.objects.filter(id=cartItem)
        if p_qs.exists():
            p = p_qs[0]
        else:
            p = Product.objects.get(id=cartItem)
        date_added = timezone.now()
        ci.date_added = date_added
        ci.product = p
        ci.user = request.user
        ci.save()
        cart_qs = Cart.objects.filter(user=request.user)

        if cart_qs.exists():
            cart = cart_qs[0]
            
            cart.count = cart.products.count()
            print(cart.count)
            cart.save()

            if cart.products.filter(product__pk=pk).exists():
                ci.augment_quantity(ci.quantity)
                ci.save()
                return redirect("shop:shopping_cart")
            else:
                cart.products.add(ci)
                return redirect("shop:shopping_cart")

        else:
            cart.products.add(ci) 
            cart.count = 1
            cart.save()
            print(cart.count)
            return redirect("shop:shopping_cart")   
        
    else:
        date_added = timezone.now()
        ci.date_added = date_added
        ci.save()
        cart.products.add(ci)
        return redirect("shop:shopping_cart")


def remove_from_cart(request, pk):
    print("ajax_remove: ")

    if request.method == "GET":
        response_json = request.GET
        response_json = json.dumps(response_json)
        data = json.loads(response_json)
        print(data["cartItem"])

    return JsonResponse(data)


class ShoppingCartView(View):
    def get(self, *args, **kwargs):

        try:
            user = User.objects.get(id=self.request.user.id)
            print(user)
            cart = Cart.objects.get(user=user)
            print(cart)
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
    # def get_cart(request):
    return render(request, "shopping_cart.html", context)
    # def get(self, *args, **kwargs):

    #     try:
    #         cart = Cart.objects.get(user=request.user)

    #     except ObjectDoesNotExist:
    #         messages.error(self.request, "You have nothing in your shopping cart ")
    #         return redirect("/")


def search(request):
    if request.method == "POST":
        search = request.POST.get("search")
        product_count = Product.objects.filter(
            Q(product_name__contains=search) | Q(price__contains=search)
        ).count()
        per_page = 9
        count_page = int(product_count / per_page) + 1
        product = Product.objects.filter(
            Q(product_name__contains=search) | Q(price__contains=search)
        )[:per_page]
        a = []
        for i in product:
            b = []
            b.append(i.product_name)
            b.append(i.image)
            b.append(i.description)
            b.append(i.price)
            a.append(b)
        # cat = Product.objects.filter(submenu_id=0)
        context = {
            "search": search,
            "product": a,
        }
        return render(request, "search.html", context)
    else:
        return redirect("/")
    return redirect("/")
