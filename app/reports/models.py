from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models

from app.groups.models import Group
from app.reports.utility import attendance_count_view, calculate_teacher_salary
from app.users.models import User


class TeacherSalary(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    percentage = models.IntegerField(default=50)
    month = models.PositiveSmallIntegerField(blank=True, default=datetime.now().month)
    year = models.PositiveSmallIntegerField(blank=True, default=datetime.now().year)
    attendance_count = models.IntegerField(blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    calculate_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if TeacherSalary.objects.filter(
                teacher=self.teacher,
                group=self.group,
                month=self.month,
                year=self.year
        ).exclude(id=self.id).exists():
            raise ValidationError("Bu o'qituvchi uchun bu oyda oylik allaqachon mavjud.")

    def save(self, *args, **kwargs):
        self.month = datetime.now().month
        self.year = datetime.now().year
        self.attendance_count = attendance_count_view(self.group, self.month, self.year)
        self.salary = calculate_teacher_salary(self.group, self.month, self.year, self.percentage)
        self.full_clean()
        super(TeacherSalary, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('teacher', 'group', 'month', 'year')

    def __str__(self):
        return f"{self.teacher}-{self.month}/{self.year}-{self.salary} UZS"
