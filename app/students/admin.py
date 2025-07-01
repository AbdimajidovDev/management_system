from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.students.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass
