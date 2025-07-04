from django.db import models
from app.users.models import BaseModel, User


class Group(BaseModel):

    class GroupType(models.TextChoices):
        even = 'e', 'Even day'
        odd = 'o', 'Odd day'
        all = 'a', 'All day'

    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to = {'role': User.UserRoles.teacher}, related_name='teaching_groups')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    type = models.CharField(max_length=100, choices=GroupType.choices)

    def __str__(self):
        return f"{self.name} - teacher: {self.teacher.full_name}"
