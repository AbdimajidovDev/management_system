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
    ordering = ['date']

# # # -------------------------------------------------------------------------------------------->

class AttendanceAdmin(admin.ModelAdmin):
    change_list_template = 'admin/attendance_matrix.html'

    def changelist_view(self, request, extra_context=None):
        user = request.user
        students = Student.objects.none()

        if user.role == 't':
            groups = Group.objects.filter(teacher=user)
        else:
            groups = Group.objects.all()

        group_id = request.GET.get('group')
        group = groups.filter(id=group_id).first() if group_id else groups.first()

        if group:
            students = Student.objects.filter(group=group)

        start_date = group.start_date
        end_date = group.end_date

        # Tizimga asoslangan kunlar
        if group.type == 'e':  # juft
            if start_date.day % 2 != 0:
                start_date += timedelta(days=1)
            days = (end_date - start_date).days + 1
            dates = [start_date + timedelta(days=i) for i in range(0, days, 2) if
                     (start_date + timedelta(days=i)).weekday() != 6]
        elif group.type == 'o':  # toq
            if start_date.day % 2 == 0:
                start_date += timedelta(days=1)
            days = (end_date - start_date).days + 1
            dates = [start_date + timedelta(days=i) for i in range(0, days, 2) if
                     (start_date + timedelta(days=i)).weekday() != 6]
        else:  # har kuni
            days = (end_date - start_date).days + 1
            dates = [start_date + timedelta(days=i) for i in range(days) if
                     (start_date + timedelta(days=i)).weekday() != 6]

        # Attendance statuslarini yig'amiz
        attendance_data = {}
        for student in students:
            attendance_data[student.id] = {}
            for d in dates:
                att = Attendance.objects.filter(student=student, group=group, date=d).first()
                attendance_data[student.id][d.strftime('%Y-%m-%d')] = att.status if att else 'e'

        extra_context = extra_context or {}
        extra_context.update({
            'students': students,
            'dates': dates,
            'attendance_data': attendance_data,
            'group': group,
            'groups': groups,
            'today': date.today().strftime('%Y-%m-%d'),
            'user': request.user,
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