from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from app.users.models import User



@admin.register(User)
class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("phone_number", "full_name", "role", "is_staff")
    list_filter = ("role", "is_staff")

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Shaxsiy ma'lumotlar", {"fields": ("first_name", "last_name", "email")}),
        ("Ruxsatlar", {"fields": ("role", "is_staff", "is_superuser", "user_permissions", "groups")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone_number", "first_name", "last_name", "role", "password1", "password2"),
        }),
    )

    search_fields = ("phone_number", "first_name", "last_name")
    ordering = ("phone_number",)
