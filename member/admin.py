from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import SignUpForm

from .models import User

# Register your models here.

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('추가정보', {'fields': ('img_profile', 'gender')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('추가정보', {
            'fields': ('img_profile', 'gender',),
        }),
    )
    add_form = SignUpForm

admin.site.register(User, UserAdmin)