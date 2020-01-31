# User URL Configuration
app_name = 'users'
from django.urls import path, include
from .views import CreateUser, LoginUser, WelcomePage
urlpatterns = [
    path('', WelcomePage.as_view(), name='home-page'),
    path('register/', CreateUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
]
