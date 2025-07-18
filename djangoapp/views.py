# djangoapp/views.py
from django.shortcuts import render

def about(request):
    return render(request, 'djangoapp/about.html')

def contact(request):
    return render(request, 'djangoapp/contact.html')

def index(request):
    return render(request, 'djangoapp/index.html') 