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

