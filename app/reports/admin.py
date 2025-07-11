from django.contrib import admin

from app.reports.models import TeacherSalary, Report
from app.users.models import User


@admin.register(TeacherSalary)
class TeacherSalaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'group', 'salary', 'month', 'year')
    list_filter = ('group', 'month', 'year')
    search_fields = ('group', 'teacher')
    list_display_links = ('id', 'teacher')

    def get_queryset(self, request):
        qs = super(TeacherSalaryAdmin, self).get_queryset(request)
        user = request.user
        if user.role == User.UserRoles.teacher:
            return qs.filter(teacher=user)
        return qs


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    # pass
    list_display = ('student_fees', 'teachers_salaries', 'benefit', 'month', 'year')