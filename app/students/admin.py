from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.students.models import Student
from app.users.models import User


# @admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone_number', 'parents_phone_number', 'group', 'is_paid')
    list_display_links = ('full_name',)
    search_fields = ('full_name',)
    list_filter = ('group', 'is_paid')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.is_staff and hasattr(user, 'role') and user.role == User.UserRoles.teacher:
            return qs.filter(group__teacher=user)
        return qs

admin.site.register(Student, StudentAdmin)
