from django.contrib import admin

from app.reports.models import TeacherSalary


@admin.register(TeacherSalary)
class TeacherSalaryAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'group', 'salary', 'month', 'year')
    list_filter = ('group', 'month', 'year')
    search_fields = ('group', 'teacher')