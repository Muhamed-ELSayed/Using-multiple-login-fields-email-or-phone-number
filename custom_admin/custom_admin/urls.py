from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('custom_user/admin/', admin.site.urls),
    path('', include('users.urls', namespace='users')),
]
