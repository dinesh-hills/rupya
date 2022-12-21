from django.utils.html import format_html
from django.urls import reverse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import RegistrationForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    
    add_form = RegistrationForm

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "first_name", "last_name"),
            },
        ),
    )