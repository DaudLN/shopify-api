from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    search_fields = ['first_name', 'last_name', 'email', 'username']
    list_display = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['username', 'first_name', 'last_name', 'email']
    
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "first_name" ,"last_name", "email", "password1", "password2"),
            },
        ),
    )