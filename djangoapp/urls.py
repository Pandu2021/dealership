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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)