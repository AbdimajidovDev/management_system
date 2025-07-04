from django.db import models

from app.groups.models import Group
from app.students.models import Student
from app.users.models import BaseModel


class Attendance(BaseModel):

    class Status(models.TextChoices):
        PRESENT = 'p', 'present'
        ABSENT = 'a', 'absent'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='attendances')
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PRESENT)
    date = models.DateField()

    class Meta:
        unique_together = ('student', 'group', 'date')
        db_table = 'attendance'

    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {self.status}"
