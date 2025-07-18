from django.shortcuts import render, redirect 
from django.contrib.auth.models import User 
from django.contrib.auth import logout, login, authenticate 
from django.contrib import messages 
from datetime import datetime 
import logging 

# Get logger instance
logger = logging.getLogger(__name__)

# The existing view function
def about(request):
    return render(request, 'djangoapp/about.html')

def contact(request):
    return render(request, 'djangoapp/contact.html')

def index(request):
    return render(request, 'djangoapp/index.html')

# Login
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Hallo, {username}! You have logged in successfully..")
            return redirect("djangoapp:index") 
        else:
            messages.error(request, "Username or password is incorrect.")
    return render(request, 'djangoapp/registration/login.html')

# Logout
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("djangoapp:index") 

# Registration
def registration_request(request):
    if request.method == "POST":
        # Taking data from the form
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm'] 

        # Ensure the password matches
        if password != password_confirm:
            messages.error(request, "Password and confirmation password do not match..")
            return render(request, 'djangoapp/registration/register.html')

        # Ensure that the username or email is not already in use.
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' has been used.")
            return render(request, 'djangoapp/registration/register.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, f"Email '{email}' has been used.")
            return render(request, 'djangoapp/registration/register.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            messages.success(request, f"Akun '{username}' created successfully! You are now logged in.")
            return redirect("djangoapp:index") 
        except Exception as e:
            messages.error(request, f"An error occurred during registration.: {e}")
            logger.error(f"Error during registration: {e}") 
            return render(request, 'djangoapp/registration/register.html')

    return render(request, 'djangoapp/registration/register.html')