from rest_framework import permissions
from app.users.models import User


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and  User.UserRoles.superadmin)# and request.user.is_authenticated)
