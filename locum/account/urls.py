# account/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.log, name='log'),
    path('api/login', views.LoginView.as_view(), name='api_login'),
    path('api/register', views.RegisterView.as_view(), name='api_register'),
]