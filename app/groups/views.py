from rest_framework import viewsets

from app.groups.models import Group
from app.groups.serializers import GroupSerializer
from app.users.utility import *


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrSuperAdmin, )
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

# ////////////////////////////////////////////////////////////////////////////


from app.attendance.models import Attendance
from app.groups.models import Group




def calculate_teacher_salary(group: Group, month: int, year: int):
    lesson_dates = Attendance.objects.filter(
        group=group,
        date__year=year,
        date__month=month,
    ).values('date').distinct()


    lesson_count = lesson_dates.count()

    if lesson_count == 0:
        return 0

    attendance_count = Attendance.objects.filter(
        group=group,
        date__year=year,
        date__month=month,
        status=['p', 'a']).count()

    per_lesson_price = group.price / lesson_count
    total_income = per_lesson_price * attendance_count
    salary = total_income // 2

    # return salary
    return round(salary, 2)