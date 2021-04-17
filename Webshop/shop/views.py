from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse, HttpResponse
import json

# Create your views here.

# def index(request):
#     return render(request, "index.html", {})


def products(request):
    product_list = Product.objects.all()
    return render(request, "index.html", {"product_list": product_list})


class ProductView(DetailView):
    model = Product
    template_name = "product.html"


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)

    cart_item = request.GET.get('cart_item', None)
    
    print(product)
    
    return HttpResponse(product)

def add_product(request):
    # cart = Cart(request)
 
    # cart.add(product=product)
    data = request.POST
    received_json_data = json.loads(request.body)
    product_id = request.GET.get('product_id')
    product = Product.objects.get(id=product_id)
    return JsonResponse({'product': 'product'})

def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    print("removed product: ", product)
    return HttpResponse(product)

def search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        product_count = Product.objects.filter(Q(product_name__contains=search) | Q(price__contains=search)).count()
        per_page = 9
        count_page = int(product_count / per_page) + 1
        product = Product.objects.filter(Q(product_name__contains=search) | Q(price__contains=search))[:per_page]
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
            'search': search,
            'product': a,

        }
        return render(request, 'search.html', context)
    else:
        return redirect('/')
    return redirect('/')