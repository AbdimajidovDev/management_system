from unfold import admin
from django.contrib import admin as django_admin

from app.attendance.admin import AttendanceInline
from app.students.models import StudentGroup
from app.groups.models import Group
from app.users.models import User


class StudentInline(admin.TabularInline):
    model = StudentGroup
    fields = ('student', 'is_paid')
    extra = 1

class GroupAdmin(admin.ModelAdmin):
    inlines = [StudentInline, AttendanceInline]
    list_display = ('name', 'teacher', 'price', 'start_date', 'end_date', 'type')
    search_fields = ('name', 'teacher')
    list_filter = ('teacher', 'type')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.is_staff and hasattr(user, 'role') and user.role == User.UserRoles.teacher:
            return qs.filter(teacher=user)
        return qs

django_admin.site.register(Group, GroupAdmin)
