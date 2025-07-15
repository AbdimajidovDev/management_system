from django.contrib import admin as django_admin
from app.students.models import Student, StudentGroup
from app.users.models import User

from unfold import admin as unfold_admin
from unfold.admin import ModelAdmin, TabularInline


class StudentGroupInline(TabularInline):
    model = StudentGroup
    extra = 1
    show_change_link = True

class StudentAdmin(ModelAdmin):
    inlines = [StudentGroupInline]

    list_display = ('full_name', 'phone_number', 'parents_phone_number', 'get_groups')
    list_display_links = ('full_name',)
    search_fields = ('full_name',)

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = 'Groups'


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user

        if user.is_staff and hasattr(user, 'role') and user.role == User.UserRoles.teacher:
            return qs.filter(group__teacher=user)
        return qs

django_admin.site.register(Student, StudentAdmin)


class StudentGroupAdmin(unfold_admin.ModelAdmin):
    list_display = ('student', 'group', 'is_paid', 'created_at')
    list_display_links = ('student', 'group')
    search_fields = ('student', 'group')
    list_filter = ('group', 'is_paid')

django_admin.site.register(StudentGroup, StudentGroupAdmin)