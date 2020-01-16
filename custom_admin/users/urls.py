# User URL Configuration
app_name = 'users'
from django.urls import path, include
from .views import CreateUser, LoginUser, Success_page
urlpatterns = [
    path('register/', CreateUser.as_view(), name='register'),
    path('', LoginUser.as_view(), name='login'),
    path('success/', Success_page.as_view(), name='success')
]
