from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('', views.log, name='log'),
    path('api/login', views.LoginView.as_view(), name='api_login'),
    path('api/register', views.SignupView.as_view(), name='api_register'),
    path('signup/', views.signup_page, name='signup_page'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/google-login/', views.GoogleLoginView.as_view(), name='google-login'),

]