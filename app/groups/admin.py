from django.contrib import admin as django_admin
from unfold import admin
from app.attendance.admin import AttendanceInline
from app.groups.models import Group
from app.students.models import Student, StudentGroup


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
        print('request: ', request)

        if user.is_staff and hasattr(user, 'role') and user.role == user.UserRoles.teacher:
            return qs.filter(teacher=user)
        return qs

django_admin.site.register(Group, GroupAdmin)
