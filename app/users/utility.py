from rest_framework import permissions
from app.users.models import User


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        print('-----------------------------')
        print("Super User:", request.user)
        print("Role:", getattr(request.user, "role", None))
        print("is_superuser:", request.user.is_superuser)
        print("is_authenticated:", request.user.is_authenticated)
        print('-----------------------------')

        return bool(user and user.is_authenticated and  user.role == User.UserRoles.superadmin)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        print('-----------------------------')
        print("User:", request.user)
        print("Role:", getattr(request.user, "role", None))
        print("is_superuser:", request.user.is_superuser)
        print("is_authenticated:", request.user.is_authenticated)
        print('-----------------------------')

        return bool(user and user.is_authenticated and user.role == User.UserRoles.admin)


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.role == User.UserRoles.teacher)
