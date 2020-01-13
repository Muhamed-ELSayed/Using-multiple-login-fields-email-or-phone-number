from django.contrib import admin
from .models import Users
# Register your models here.

class UserAdmin(admin.ModelAdmin):
  fields= ['fullname', 'phone_number', 'email', 'password', 'verfiy_pass']
  list_display = ['fullname', 'phone_number', 'email',]
  search_fields = ['fullname', 'phone_number', 'email',]
  list_filter = ['fullname', 'phone_number', 'email',]
  # list_editable = ['fullname', 'phone_number', 'email',]
  # list_display_links= None
admin.site.register(Users, UserAdmin)