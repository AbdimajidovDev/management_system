from calendar import month

from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime

from .models import TeacherSalary, Report
from .utility import student_fees_view, total_teacher_salary

@receiver(post_save, sender=TeacherSalary)
def update_or_create_report(sender, instance, created, **kwargs):
    month = instance.month
    year = instance.year

    student_fees = student_fees_view()
    teachers_salaries = total_teacher_salary()
    benefit = student_fees_view() - total_teacher_salary()

    report, created = Report.objects.update_or_create(
        month = month,
        year = year,
        defaults = {
            'student_fees' : student_fees,
            'teachers_salaries' : teachers_salaries,
            'benefit' : benefit,
        }
    )
