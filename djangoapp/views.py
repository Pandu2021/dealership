from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import logging
import json 

from .restapis import (
    get_dealers_from_api,
    get_dealer_by_id,
    get_dealer_reviews_from_api,
    add_review,
    get_car_makes,
    get_car_models
)

# Get an instance of a logger
logger = logging.getLogger(__name__)

# --- Existing views (from Part 1 & 2) ---
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
            messages.success(request, f"Hallo, {username}. You have successfully logged in.")
            return redirect('djangoapp:index') 
        else:
            messages.error(request, "Username or Password is incorrect.")
            return render(request, 'djangoapp/login.html') 
    return render(request, 'djangoapp/login.html')

# Logout
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('djangoapp:index') 

# Registration
def registration_request(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'djangoapp/register.html') 

        user = User.objects.create_user(username=username, email=email, password=password,
                                         first_name=first_name, last_name=last_name)
        user.save()
        login(request, user)
        messages.success(request, f"Akun {username} successfully created and you have logged in.")
        return redirect('djangoapp:index') 
    return render(request, 'djangoapp/register.html')

# --- New views for Part 3 (Proxy Services) ---

def get_dealerships(request, state="All"):
    """
    Fetches dealerships from the Express-Mongo API, optionally filtered by state.
    """
    dealerships = get_dealers_from_api(state)
    if dealerships:
        return JsonResponse({"status": 200, "dealers": dealerships})
    return JsonResponse({"status": 404, "message": "No dealerships found"}, status=404)

def get_dealer_details(request, dealer_id):
    """
    Fetches details for a specific dealer and their reviews.
    """
    dealer_details = get_dealer_by_id(dealer_id)
    if dealer_details:
        reviews = get_dealer_reviews_from_api(dealer_id)
        return JsonResponse({"status": 200, "dealerDetails": dealer_details, "reviews": reviews})
    return JsonResponse({"status": 404, "message": "Dealer not found"}, status=404)

def add_review_view(request):
    """
    Handles POST request to add a new review.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            
            required_fields = ['dealership', 'name', 'purchase', 'review']
            if not all(field in data for field in required_fields):
                return JsonResponse({"status": 400, "message": "Missing required fields"}, status=400)

            response = add_review(data) # Call the add_review function from restapis.py
            if response and not response.get("error"):
                return JsonResponse({"status": 201, "message": "Review added successfully", "review": response}, status=201)
            else:
                return JsonResponse({"status": 400, "message": response.get("error", "Failed to add review")}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"status": 400, "message": "Invalid JSON in request body"}, status=400)
        except Exception as e:
            logger.error(f"Error in add_review_view: {e}")
            return JsonResponse({"status": 500, "message": "Internal server error"}, status=500)
    return JsonResponse({"status": 405, "message": "Method Not Allowed"}, status=405)


def get_car_makes_view(request):
    """
    Fetches car makes from local Django models and returns as JSON.
    """
    car_makes = get_car_makes()
    if car_makes:
        return JsonResponse({"status": 200, "car_makes": car_makes})
    return JsonResponse({"status": 404, "message": "No car makes found"}, status=404)

def get_car_models_view(request, make_id=None):
    """
    Fetches car models from local Django models, optionally filtered by car make.
    """
    car_models = get_car_models(make_id)
    if car_models:
        return JsonResponse({"status": 200, "car_models": car_models})
    return JsonResponse({"status": 404, "message": "No car models found"}, status=404)