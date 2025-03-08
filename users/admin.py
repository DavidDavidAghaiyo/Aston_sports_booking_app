from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# User Register
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_admin', 'is_staff') #Fields in the user model
    search_fields = ('username', 'email') #Search functionality
    list_filter = ('is_admin', 'is_staff')



