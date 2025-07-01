from django.contrib import admin

from app.groups.models import Group
from app.students.models import Student


class StudentInline(admin.TabularInline):
    model = Student
    extra = 1

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'start_date', 'end_date')
    search_fields = ('name', 'teacher')
    list_filter = ('teacher',)

    inlines = (StudentInline,)
