from calendar import month_name
from datetime import datetime, timedelta, date
from django.contrib import admin as django_admin
from django.shortcuts import render
from unfold import admin as unfold_admin
from django import forms

from app.attendance.models import Attendance
from app.groups.models import Group
from app.students.models import StudentGroup
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

from datetime import date, timedelta, datetime
from calendar import month_name
from django.shortcuts import render
from unfold.admin import ModelAdmin as UnfoldModelAdmin


@django_admin.register(Attendance)
class AttendanceAdmin(UnfoldModelAdmin):
    change_list_template = 'admin/attendance_matrix.html'

    def changelist_view(self, request, extra_context=None):
        user = request.user

        groups = self.get_user_groups(user)
        group = self.get_selected_group(request, groups)
        students = self.get_group_students(group)

        current_date = date.today()
        selected_month = request.GET.get('month', current_date.strftime('%Y-%m'))
        selected_date = self.parse_selected_date(selected_month, current_date)

        month_start, month_end = self.get_month_range(selected_date)
        lesson_weekdays = self.get_group_weekdays(group)
        lesson_dates = self.get_lesson_dates(month_start, month_end, lesson_weekdays)

        months = self.get_available_months(group)
        attendance_data = self.get_attendance_data(students, group, lesson_dates)

        extra_context = extra_context or {}
        extra_context.update({
            'students': students,
            'dates': lesson_dates,
            'attendance_data': attendance_data,
            'group': group,
            'groups': groups,
            'months': months,
            'selected_month': selected_month,
            'today': current_date.strftime('%Y-%m-%d'),
            'user': user,
        })
        return render(request, self.change_list_template, extra_context)

    def get_user_groups(self, user):
        if user.role == User.UserRoles.teacher:
            return Group.objects.filter(teacher=user)
        elif user.role == User.UserRoles.parent:
            return Group.objects.filter(
                id__in=StudentGroup.objects.filter(student__parent=user).values('group_id')
            ).distinct()
        return Group.objects.all()

    def get_selected_group(self, request, groups):
        group_id = request.GET.get('group')
        if group_id:
            return groups.filter(id=group_id).first()
        return groups.first()

    def get_group_students(self, group):
        if not group:
            return StudentGroup.objects.none()
        return StudentGroup.objects.filter(group=group)

    def parse_selected_date(self, month_str, fallback_date):
        try:
            return datetime.strptime(month_str, '%Y-%m').date()
        except ValueError:
            return fallback_date

    def get_month_range(self, selected_date):
        month_start = selected_date.replace(day=1)
        if selected_date.month == 12:
            month_end = selected_date.replace(year=selected_date.year + 1, month=1, day=1)
        else:
            month_end = selected_date.replace(month=selected_date.month + 1, day=1)
        return month_start, month_end

    def get_group_weekdays(self, group):
        if not group:
            return list(range(6))  # all days by default
        if group.type == Group.GroupType.even:
            return [1, 3, 5]
        elif group.type == Group.GroupType.odd:
            return [0, 2, 4]
        return list(range(6))  # all days

    def get_lesson_dates(self, start, end, weekdays):
        return [
            start + timedelta(days=i)
            for i in range((end - start).days)
            if (start + timedelta(days=i)).weekday() in weekdays
        ]

    def get_available_months(self, group):
        if not group:
            return []

        months = []
        current = group.start_date.replace(day=1)
        while current <= group.end_date:
            months.append({
                'value': current.strftime('%Y-%m'),
                'label': f"{month_name[current.month]} {current.year}"
            })
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)
        return months

    def get_attendance_data(self, students, group, dates):
        data = {}
        for student_rel in students:
            student_id = student_rel.student.id
            data[student_id] = {}
            for d in dates:
                att = Attendance.objects.filter(
                    student=student_rel.student,
                    group=group,
                    date=d
                ).first()
                data[student_id][d.strftime('%Y-%m-%d')] = att.status if att else 'e'
        return data

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        user = request.user
        if user.role == User.UserRoles.teacher:
            return qs.filter(group__teacher=user)
        elif user.role == User.UserRoles.parent:
            return qs.none()  # Parent should not access this queryset directly
        return qs



# # # -------------------------------------------------------------------------------------------->

# class AttendanceAdmin(unfold_admin.ModelAdmin):
#     change_list_template = 'admin/attendance_matrix.html'
#
#     def changelist_view(self, request, extra_context=None):
#         user = request.user
#         students = StudentGroup.objects.none()
#
#         # Group filter
#         if user.role == User.UserRoles.teacher:
#             groups = Group.objects.filter(teacher=user)
#         elif user.role == User.UserRoles.parent:
#             groups = Group.objects.filter(
#                 id__in=StudentGroup.objects.filter(student__parent=user).values('group_id')
#             ).distinct()
#         else:
#             groups = Group.objects.all()
#
#         group_id = request.GET.get('group')
#         group = groups.filter(id=group_id).first() if group_id else groups.first()
#
#         if group:
#             students = StudentGroup.objects.filter(group=group)
#
#         # Hozirgi sana va tanlangan oy
#         current_date = date.today()
#         selected_month = request.GET.get('month', current_date.strftime('%Y-%m'))
#         # group_id = request.GET.get('group')
#
#         # Tanlangan oy bo‘yicha start va end
#         try:
#             selected_date = datetime.strptime(selected_month, '%Y-%m').date()
#         except ValueError:
#             selected_date = current_date
#
#         month_start = selected_date.replace(day=1)
#         if selected_date.month == 12:
#             month_end = selected_date.replace(year=selected_date.year + 1, month=1, day=1)
#         else:
#             month_end = selected_date.replace(month=selected_date.month + 1, day=1)
#
#         # Guruh dars kunlari
#         if group.type == group.GroupType.even:
#             lesson_weekdays = [1, 3, 5]
#         elif group.type == group.GroupType.odd:
#             lesson_weekdays = [0, 2, 4]
#         else:
#             lesson_weekdays = [0, 1, 2, 3, 4, 5]
#
#         # Tanlangan oy ichidagi dars kunlari
#         days = (month_end - month_start).days
#         dates = [
#             month_start + timedelta(days=i)
#             for i in range(days)
#             if (month_start + timedelta(days=i)).weekday() in lesson_weekdays
#         ]
#
#         # Guruh davriga qarab oylar ro‘yxatini hosil qilish
#         start_date = group.start_date
#         end_date = group.end_date
#         months = []
#         current = start_date.replace(day=1)
#         while current <= end_date:
#             months.append({
#                 'value': current.strftime('%Y-%m'),
#                 'label': f"{month_name[current.month]} {current.year}"
#             })
#
#             # Keyingi oyga o'tish
#             if current.month == 12:
#                 current = current.replace(year=current.year + 1, month=1)
#             else:
#                 current = current.replace(month=current.month + 1)
#
#         attendance_data = {}
#         for student in students:
#             attendance_data[student.student.id] = {}
#             for d in dates:
#                 att = Attendance.objects.filter(student=student.student, group=group, date=d).first()
#                 attendance_data[student.student.id][d.strftime('%Y-%m-%d')] = att.status if att else 'e'
#
#         extra_context = extra_context or {}
#         extra_context.update({
#             'students': students,
#             'dates': dates,
#             'attendance_data': attendance_data,
#             'group': group,
#             'groups': groups,
#             'months': months,
#             'selected_month': selected_month,
#             'today': date.today().strftime('%Y-%m-%d'),
#             'user': request.user,
#         })
#
#         # return super().changelist_view(request, extra_context=extra_context)
#         return render(request, 'admin/attendance_matrix.html', extra_context)
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         user = request.user
#         if user.role == User.UserRoles.teacher:
#             return qs.filter(group__teacher=user)
#         return qs
#
# django_admin.site.register(Attendance, AttendanceAdmin)

# # # -------------------------------------------------------------------------------------------->
