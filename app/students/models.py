from django.db import models

from app.groups.models import Group
from app.users.models import BaseModel, User


class Student(BaseModel):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13, unique=True)
    parents_phone_number = models.CharField(max_length=13, blank=True, null=True)
    groups = models.ManyToManyField(Group, through="StudentGroup")
    parent = models.ForeignKey(User, on_delete=models.SET_NULL,
                               limit_choices_to={'role': User.UserRoles.parent},
                               blank=True, null=True,
                               related_name='children')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.full_name} student"


class StudentGroup(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'group')

    def __str__(self):
        return f"{self.group} - {self.student.full_name}"