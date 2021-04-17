from django.shortcuts import render
from .forms import ContactForm
from django.http import JsonResponse, HttpResponse


def index(request):
    return render(request, "home.html", {})