from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer, LoginSerializer, GoogleAuthSerializer
from django.shortcuts import render
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
import json

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
        return Response(
            {'error': 'Invalid Credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)

class GoogleLoginView(generics.GenericAPIView):
    serializer_class = GoogleAuthSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        
        try:
            # Verify the Google OAuth2 token
            idinfo = id_token.verify_oauth2_token(
                token, 
                requests.Request(), 
                settings.GOOGLE_OAUTH2_CLIENT_ID
            )
            
            # Check if the token is for the intended audience
            if idinfo['aud'] != settings.GOOGLE_OAUTH2_CLIENT_ID:
                raise ValueError('Could not verify audience.')
                
            # Extract user information
            email = idinfo['email']
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')
            
            # Check if user exists, if not create one
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Create a new user
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=None  # No password for social login
                )
                user.save()
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            })
            
        except ValueError:
            return Response(
                {'error': 'Invalid Google token'},
                status=status.HTTP_400_BAD_REQUEST
            )

# Template views
def log(request):
    return render(request, 'log/log.html')

def signup_page(request):
    return render(request, 'log/signup.html')