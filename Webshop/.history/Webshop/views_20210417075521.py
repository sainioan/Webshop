from django.shortcuts import render
from .forms import ContactForm
from django.http import JsonResponse, HttpResponse


def home_page(request):
    return render(request, "home.html", {})