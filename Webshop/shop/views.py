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


def remove_from_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    print("removed product: ", product)
    return HttpResponse(product)