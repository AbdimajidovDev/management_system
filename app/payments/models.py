from django.db import models

from app.students.models import Student
from app.users.models import BaseModel


class Payment(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    paid_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    moth = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-paid_at']
        unique_together = ('student', 'moth')

    def __str__(self):
        return f"{self.student.full_name} - {self.student.group} - {self.amount} ming UZS"