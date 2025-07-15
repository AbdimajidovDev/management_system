
# """oy ning oxirgi davomati qilinganda salary yaratiladi"""


# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# import app.reports.models
# from app.attendance.models import Attendance
# from app.reports.models import TeacherSalary
# from app.reports.utility import attendance_count_view, calculate_teacher_salary
# from datetime import datetime, timedelta
#
#
# @receiver(post_save, sender=Attendance)
# def create_teacher_salary(sender, instance, created, **kwargs):
#     if not created:
#         return
#
#     group = instance.group
#     teacher = instance.group.teacher
#     date = instance.date
#
#     current_month = date.month
#     current_year = date.year
#
#     start_date = group.start_date
#     end_date = group.end_date
#
#     days = (end_date - start_date).days + 1
#     all_dates = []
#
#     for i in range(days):
#         d = start_date + timedelta(days=i)
#         if d.month == current_month and d <= date and d.weekday() != 6:
#             if group.type == 'e' and d.day % 2 == 0:
#                 all_dates.append(d)
#             elif group.type == 'o' and d.day % 2 != 0:
#                 all_dates.append(d)
#             elif group.type == 'a':
#                 all_dates.append(d)
#
#         if not all_dates:
#             return
#
#         last_lesson_day = max(all_dates)
#         if date != last_lesson_day:
#             return
#
#         already_exists = TeacherSalary.objects.filter(
#             teacher = teacher,
#             group = group,
#             month=current_year,
#             year=current_year,
#         ).exists()
#StudentGroup
#         if not already_exists:
#             attendance_count = attendance_count_view(group, current_month, current_year)
#             salary = calculate_teacher_salary(group, current_month, current_year)
#
#             TeacherSalary.objects.create(
#                 teacher = teacher,
#                 group = group,
#                 month = current_year,
#                 year = current_year,
#                 attendance_count = attendance_count,
#                 salary = salary,
#             )