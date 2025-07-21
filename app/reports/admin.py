from django.contrib import admin as django_admin
from unfold import admin as unfold_admin

from app.reports.models import TeacherSalary, Report
from app.users.models import User


class TeacherSalaryAdmin(unfold_admin.ModelAdmin):
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

django_admin.site.register(TeacherSalary, TeacherSalaryAdmin)


class ReportAdmin(unfold_admin.ModelAdmin):
    list_display = ('student_fees', 'teachers_salaries', 'benefit', 'month', 'year')

django_admin.site.register(Report, ReportAdmin)
