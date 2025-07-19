from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # Static pages from Part 1
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # Mengubah halaman root untuk menampilkan daftar dealer secara default
    # Anda dapat mengganti ini kembali ke views.index jika ingin halaman statis 'index.html' tetap menjadi halaman utama
    path('', views.get_dealerships, name='index'), 

    # User Management paths from Part 2
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.registration_request, name='register'),

    # API Endpoints for Dealers and Reviews (New from Part 3)
    path('dealers/', views.get_dealerships, name='get_dealers'),
    path('dealers/<str:state>/', views.get_dealerships, name='get_dealers_by_state'),
    path('dealer/<int:dealer_id>/', views.get_dealer_details, name='get_dealer_details'),
    path('add_review/', views.add_review_view, name='add_review'),
    
    # API Endpoints for Car Makes and Models (New from Part 3)
    path('carmakes/', views.get_car_makes_view, name='get_car_makes'),
    path('carmodels/', views.get_car_models_view, name='get_car_models'),
    path('carmodels/<int:make_id>/', views.get_car_models_view, name='get_car_models_by_make'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)