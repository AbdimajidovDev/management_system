from django.db import models
from app.users.models import BaseModel, User


class Group(BaseModel):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to = {'role': User.UserRoles.teacher}, related_name='teaching_groups')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

