from django.urls import path
from . import views

urlpatterns = [
    path('', views.log, name='log'),
    path('api/login', views.LoginView.as_view(), name='api_login'),
    path('api/signup', views.SignupView.as_view(), name='api_register'),
]