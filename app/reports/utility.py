import datetime
from calendar import monthrange
from decimal import Decimal

from django.db.models import Sum

from app.attendance.models import Attendance

def get_lesson_days(group, start_date, end_date):

    if group.type == 'e':
        lesson_weekdays = [1, 3, 5]
    elif group.type == 'o':
        lesson_weekdays = [0, 2, 4, ]
    else:
        lesson_weekdays = [0, 1, 2, 3, 4, 5]

    days = (end_date - start_date).days + 1
    dates = [
        start_date + datetime.timedelta(days=i)
        for i in range(days)
        if (start_date + datetime.timedelta(days=i)).weekday() in lesson_weekdays
    ]
    return dates

def calculate_teacher_salary(group, month, year, percentage=50):

    first_day = datetime.date(year, month, 1)
    last_day = datetime.date(year, month, monthrange(year, month)[1])

    lesson_days = get_lesson_days(group, first_day, last_day)
    print('lesson days: ////// ', len(lesson_days))
    active_dates = [d for d in lesson_days if d >= group.start_date]

    course_price = group.price

    attendances = Attendance.objects.filter(
        group=group,
        date__in=active_dates,
    )

    print('lesson_days: ', lesson_days)

    attendance_count = attendances.exclude(status='e').count()

    if lesson_days == 0:
        return 0

    total_sum = (course_price / len(lesson_days)) * attendance_count
    # total_sum = (course_price / lesson_days) *

    salary = total_sum * Decimal(percentage / 100)
    return round(salary)


def attendance_count_view(group, month, year):
    attendances = Attendance.objects.filter(
        group=group,
        date__year=year,
        date__month=month,
    )
    # print('attendances:', attendances)
    attendance_count = attendances.exclude(status='e').count()
    return attendance_count


def total_teacher_salary():
    from .models import TeacherSalary

    total_salary = TeacherSalary.objects.aggregate(total=Sum('salary'))['total']
    print('total_salary:', total_salary)
    return total_salary

def student_fees_view():
    from app.payments.models import Payment

    student_fees = Payment.objects.aggregate(total=Sum('amount'))['total']
    print('student_fees:', student_fees)
    return student_fees