from django.contrib import admin

from app.users.models import User


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "full_name", "role", "is_staff")