# djangoapp/urls.py
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.registration_request, name='register'), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)