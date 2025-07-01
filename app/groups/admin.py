from django.contrib import admin

from app.groups.models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'start_date', 'end_date')
    search_fields = ('name', 'teacher')
    # list_filter = ('start_date', 'end_date')
