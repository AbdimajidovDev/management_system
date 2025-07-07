from django.contrib import admin
from django import forms

from app.attendance.models import Attendance
from app.groups.models import Group
from app.students.models import Student

from datetime import timedelta, date


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('student', 'group', 'status', 'date')

class AttendanceInline(admin.TabularInline):
    model = Attendance
    form = AttendanceForm
    extra = 0

# # # -------------------------------------------------------------------------------------------->

class AttendanceAdmin(admin.ModelAdmin):
    change_list_template = 'admin/attendance_matrix.html'

    def changelist_view(self, request, extra_context=None):
        user = request.user
        students = Student.objects.none()

        # Faqat teacherlar uchun o‘z guruhlarini ko‘rsat
        if user.role == 't':
            groups = Group.objects.filter(teacher=user)
            group_id = request.GET.get('group')
            if group_id:
                group = groups.filter(id=group_id).first()
            else:
                group = groups.first()  # default

            if group:
                students = Student.objects.filter(group=group)
        else:
            # admin yoki superadmin bo‘lsa, barcha
            groups = Group.objects.all()
            group_id = request.GET.get('group')
            group = Group.objects.filter(id=group_id).first() if group_id else groups.first()
            if group:
                students = Student.objects.filter(group=group)

        # Sanalarni generatsiya qilamiz
        if group.type == 'e':
            start_date = group.start_date
            if int(str(group.start_date).split('-')[-1]) % 2 != 0:
                start_date += timedelta(days=1)
            end_date = group.end_date
            days = end_date - start_date
            dates = [start_date + timedelta(days=i) for i in range(0, days.days + 1, 2)]
        elif group.type == 'o':
            start_date = group.start_date
            if int(str(group.start_date).split('-')[-1]) % 2 == 0:
                start_date += timedelta(days=1)
            end_date = group.end_date
            days = end_date - start_date
            dates = [start_date + timedelta(days=i) for i in range(0, days.days + 1, 2)]
        else:
            start_date = group.start_date
            end_date = group.end_date
            days = end_date - start_date
            dates = [start_date + timedelta(days=i) for i in range(days.days + 1)]

        # Davomat ma'lumotlari
        attendance_data = {}
        for student in students:
            attendance_data[student] = {}
            for d in dates:
                a = Attendance.objects.filter(student=student, date=d).first()
                attendance_data[student][d] = a.status if a else None

        extra_context = extra_context or {}
        extra_context.update({
            'students': students,
            'dates': dates,
            'attendance_data': attendance_data,
            'group': group,
            'groups': groups,
            'today': date.today(),
        })
        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.role == 't':
            return qs.filter(group__teacher=user)
        return qs

admin.site.register(Attendance, AttendanceAdmin)


# # # -------------------------------------------------------------------------------------------->