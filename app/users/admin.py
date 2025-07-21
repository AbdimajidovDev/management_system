from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin

from app.students.models import Student
from app.users.models import User


class ChildrenInline(admin.TabularInline):
    model = Student
    extra = 1


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    inlines = [ChildrenInline]

    def get_inlines(self, request, obj):
        if obj and obj.role == User.UserRoles.parent:
            return [ChildrenInline]
        return []

    def get_queryset(self, request):
        user = request.user
        qs = super().get_queryset(request)

        if hasattr(user, "role") and user.role == User.UserRoles.admin:
            return qs.filter(id=user.id)
        elif hasattr(user, "role") and user.role == User.UserRoles.teacher:
            return qs.filter(id=user.id)
        elif hasattr(user, "role") and user.role == User.UserRoles.parent:
            return qs.filter(id=user.id)

        return qs

    def get_readonly_fields(self, request, obj=None):
        if request.user.role == User.UserRoles.admin:
            return [
                f.name for f in self.model._meta.fields
                if f.name not in ["phone_number", "first_name", "last_name", "email", "password"]
            ]
        elif request.user.role == User.UserRoles.teacher:
            return [
                f.name for f in self.model._meta.fields
                if f.name not in ["phone_number", "first_name", "last_name", "email", "password"]
            ]
        elif request.user.role == User.UserRoles.parent:
            return [
                f.name for f in self.model._meta.fields
                if f.name not in ["phone_number", "first_name", "last_name", "email", "password"]
            ]
        return super().get_readonly_fields(request, obj)

    def has_add_permission(self, request):
        if request.user.role == User.UserRoles.admin:
            return False
        elif request.user.role == User.UserRoles.teacher:
            return False
        elif request.user.role == User.UserRoles.parent:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.role == User.UserRoles.admin:
            return False
        elif request.user.role == User.UserRoles.teacher:
            return False
        elif request.user.role == User.UserRoles.parent:
            return False
        return super().has_delete_permission(request, obj)

    def has_change_permission(self, request, obj = None):
        if request.user.role == User.UserRoles.admin:
            return False
        elif request.user.role == User.UserRoles.teacher:
            return False
        elif request.user.role == User.UserRoles.parent:
            return False
        return super().has_change_permission(request, obj)


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
