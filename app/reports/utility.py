from decimal import Decimal
from app.attendance.models import Attendance


def calculate_teacher_salary(group, month, year):
    course_price = group.price

    attendances = Attendance.objects.filter(
        group=group,
        date__year=year,
        date__month=month,
    )

    lesson_days = attendances.values('date').distinct().count()
    attendance_count = attendances.exclude(status='e').count()

    if lesson_days == 0:
        return 0
    total_sum = (course_price / lesson_days) * attendance_count
    salary = total_sum * Decimal(0.5)
    return round(salary)


def attendance_count_view(group, month, year):
    attendances = Attendance.objects.filter(
        group=group,
        date__year=year,
        date__month=month,
    )
    attendance_count = attendances.exclude(status='e').count()
    return attendance_count