import requests
import json
from .models import CarMake, CarModel # IMPOR INI HARUS DARI MODEL DJANGO ANDA

# Configuration for API endpoints
API_URL = "http://localhost:3030"
# Placeholder for Sentiment Analyzer URL.
# Replace with your actual IBM Cloud Code Engine Sentiment Analyzer URL when deployed.
# Example: SENTIMENT_ANALYZER_URL = "https://your-sentiment-analyzer-app.codeengine.appdomain.cloud"
SENTIMENT_ANALYZER_URL = "http://localhost:5000" # Contoh placeholder

def get_request(url, **kwargs):
    print(f"DEBUG: Making GET request to {url} with params {kwargs}")
    try:
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                params=kwargs)
        response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        print(f"DEBUG: GET request successful, status {response.status_code}")
        return data
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP error during GET request: {e} - Response: {e.response.text}")
        return {"error": str(e), "details": e.response.text}
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Network error during GET request: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON decode error: {e} - Response text: {response.text}")
        return {"error": str(e), "details": response.text}

def post_request(url, json_payload, **kwargs):
    print(f"DEBUG: Making POST request to {url} with payload {json_payload} and params {kwargs}")
    try:
        response = requests.post(url, headers={'Content-Type': 'application/json'},
                                 json=json_payload, params=kwargs)
        response.raise_for_status()
        data = response.json()
        print(f"DEBUG: POST request successful, status {response.status_code}")
        return data
    except requests.exceptions.HTTPError as e:
        print(f"ERROR: HTTP error during POST request: {e} - Response: {e.response.text}")
        return {"error": str(e), "details": e.response.text}
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Network error during POST request: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON decode error: {e} - Response text: {response.text}")
        return {"error": str(e), "details": response.text}

def get_dealers_from_api(state="All"):
    endpoint = f"{API_URL}/fetchDealers"
    if state and state != "All":
        endpoint = f"{API_URL}/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    if dealerships and not dealerships.get("error"):
        return dealerships
    return []

def get_dealer_by_id(dealer_id):
    endpoint = f"{API_URL}/fetchDealer/{dealer_id}"
    dealer = get_request(endpoint)
    if dealer and not dealer.get("error"):
        return dealer
    return None

def get_dealer_reviews_from_api(dealer_id):
    endpoint = f"{API_URL}/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)
    if reviews and not reviews.get("error"):
        for review_detail in reviews:
            review_text = review_detail.get("review")
            if review_text:
                sentiment_result = analyze_review_sentiments(review_text)
                review_detail["sentiment"] = sentiment_result.get("sentiment", "N/A")
            else:
                review_detail["sentiment"] = "N/A" # Handle cases with no review text
        return reviews
    return []

def analyze_review_sentiments(review_text):
    if not SENTIMENT_ANALYZER_URL or SENTIMENT_ANALYZER_URL == "http://localhost:5000":
        print("WARNING: Sentiment Analyzer URL is not configured or is using placeholder. Returning default sentiment.")
        return {"sentiment": "neutral"} # Default sentiment if service is not configured

    endpoint = f"{SENTIMENT_ANALYZER_URL}/analyze/{review_text}"
    sentiment_response = get_request(endpoint)
    return sentiment_response if sentiment_response and not sentiment_response.get("error") else {"sentiment": "N/A"}

def add_review(json_payload):
    endpoint = f"{API_URL}/insertReview"
    response = post_request(endpoint, json_payload)
    return response

# Helper functions to get car makes and models from Django models (local SQLite DB)
def get_car_makes():
    try:
        car_makes = CarMake.objects.all().values('id', 'name')
        return list(car_makes)
    except Exception as e:
        print(f"ERROR: Failed to fetch car makes from Django models: {e}")
        return []

def get_car_models(make_id=None):
    try:
        if make_id:
            car_models = CarModel.objects.filter(car_make_id=make_id).values('id', 'name', 'year', 'type')
        else:
            car_models = CarModel.objects.all().values('id', 'name', 'year', 'type')
        return list(car_models)
    except Exception as e:
        print(f"ERROR: Failed to fetch car models from Django models: {e}")
        return []