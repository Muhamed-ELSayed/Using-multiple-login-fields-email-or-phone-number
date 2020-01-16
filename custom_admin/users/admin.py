from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import User
# Register your models here.
User = get_user_model()

class UserAdmin(admin.ModelAdmin):
  class Meta:
    model = User

  list_display = ('email', 'fullname','phone', 'admin', 'last_login')
  search_fields = ('email', 'phone', 'fullname')
  list_filter = ['email', 'phone', 'fullname']
  readonly_fields = ['password']
  ordering = ['last_login']
  fieldsets = (
      ('Basic Info', {"fields": ('fullname', 'email', 'password'),}),
      ("Personal Info",{"fields":('phone',)}),
      ("Active",{"fields":('active',)}),
      ("Staff",{"fields":('staff',)}),
      ("Admin",{"fields":('admin',)}),
  )

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)