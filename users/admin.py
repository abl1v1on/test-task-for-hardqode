from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Регистрируем новую модель User в админке
admin.site.register(User, UserAdmin)
