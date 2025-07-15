from calendar import month_name
from datetime import datetime
from django.contrib import admin as django_admin
from django.shortcuts import render
from django.utils.timezone import now
from unfold import admin as unfold_admin
from django import forms

from app.attendance.models import Attendance
from app.groups.models import Group
from app.students.models import Student, StudentGroup

from datetime import timedelta, date

from app.users.models import User


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ('student', 'group', 'status', 'date')

    def get_groups(self, obj):
        return obj.groups.all()
    get_groups.short_description = "Groups"


class AttendanceInline(unfold_admin.TabularInline):
    model = Attendance
    form = AttendanceForm
    extra = 0
    ordering = ['date']

# # # -------------------------------------------------------------------------------------------->

class AttendanceAdmin(unfold_admin.ModelAdmin):
    change_list_template = 'admin/attendance_matrix.html'

    def changelist_view(self, request, extra_context=None):
        user = request.user
        students = StudentGroup.objects.none()

        # Guruhlarni filtrlaymiz
        if user.role == 't':
            groups = Group.objects.filter(teacher=user)
        else:
            groups = Group.objects.all()

        group_id = request.GET.get('group')
        group = groups.filter(id=group_id).first() if group_id else groups.first()

        if group:
            students = StudentGroup.objects.filter(group=group)

        # Hozirgi sana va tanlangan oy
        current_date = date.today()
        selected_month = request.GET.get('month', current_date.strftime('%Y-%m'))
        group_id = request.GET.get('group')
        print('group_id:', group_id)


        # Tanlangan oy bo‘yicha start va end
        try:
            selected_date = datetime.strptime(selected_month, '%Y-%m').date()
        except ValueError:
            selected_date = current_date

        month_start = selected_date.replace(day=1)
        if selected_date.month == 12:
            month_end = selected_date.replace(year=selected_date.year + 1, month=1, day=1)
        else:
            month_end = selected_date.replace(month=selected_date.month + 1, day=1)

        # Guruh dars kunlari
        if group.type == 'e':
            lesson_weekdays = [1, 3, 5]
        elif group.type == 'o':
            lesson_weekdays = [0, 2, 4]
        else:
            lesson_weekdays = [0, 1, 2, 3, 4, 5]

        # Tanlangan oy ichidagi dars kunlari
        days = (month_end - month_start).days
        dates = [
            month_start + timedelta(days=i)
            for i in range(days)
            if (month_start + timedelta(days=i)).weekday() in lesson_weekdays
        ]

        # Guruh davriga qarab oylar ro‘yxatini hosil qilish
        start_date = group.start_date
        end_date = group.end_date
        months = []
        current = start_date.replace(day=1)
        while current <= end_date:
            months.append({
                'value': current.strftime('%Y-%m'),
                'label': f"{month_name[current.month]} {current.year}"
            })

            # Keyingi oyga o'tish
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)

        attendance_data = {}
        for student in students:
            attendance_data[student.student.id] = {}
            for d in dates:
                att = Attendance.objects.filter(student=student.student, group=group, date=d).first()
                attendance_data[student.student.id][d.strftime('%Y-%m-%d')] = att.status if att else 'e'

        print('request:', request)

        extra_context = extra_context or {}
        extra_context.update({
            'students': students,
            'dates': dates,
            'attendance_data': attendance_data,
            'group': group,
            'groups': groups,
            'months': months,
            'selected_month': selected_month,
            'today': date.today().strftime('%Y-%m-%d'),
            'user': request.user,
        })

        # return super().changelist_view(request, extra_context=extra_context)
        return render(request, 'admin/attendance_matrix.html', extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.role == User.UserRoles.teacher:
            return qs.filter(group__teacher=user)
        return qs

django_admin.site.register(Attendance, AttendanceAdmin)


# # # -------------------------------------------------------------------------------------------->