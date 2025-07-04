from django.db import models

from app.groups.models import Group
from app.users.models import BaseModel


class Student(BaseModel):
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13, unique=True)
    parents_phone_number = models.CharField(max_length=13, blank=True, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, related_name="students")
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} student"
