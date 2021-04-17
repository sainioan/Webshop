from django.shortcuts import render
from .models import *
# Create your views here.

# def index(request):
#     return render(request, "index.html", {})

def products(request):
    product_list = Product.objects.all()
    return render(request, 'index.html', {'product_list':product_list})