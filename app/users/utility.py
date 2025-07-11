import phonenumbers
from django.core.exceptions import ValidationError
from rest_framework import permissions
from app.users.models import User


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and  user.role == User.UserRoles.superadmin)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == User.UserRoles.admin)


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == User.UserRoles.teacher)


class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user.is_authenticated and user.role in [user.UserRoles.superadmin, user.UserRoles.admin])


def validate_phone_number(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        if not phonenumbers.is_valid_number(parsed_number):
            raise ValidationError(message="Phone number is invalid")
    except phonenumbers.NumberParseException:
        raise ValidationError(message="Your phone number is in the wrong format.. (Correct format: +998xxxxxxxxx)")
