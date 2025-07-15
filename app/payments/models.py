from django.db import models

from app.groups.models import Group
from app.students.models import Student, StudentGroup
from app.users.models import BaseModel


class Payment(BaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    paid_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    moth = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-paid_at']
        unique_together = ('student', 'moth')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        student_group, created = StudentGroup.objects.get_or_create(
            student=self.student,
            group=self.group
        )
        student_group.is_paid = True
        student_group.save()

    def __str__(self):
        return f"{self.student.full_name} - {self.group} - {self.amount} ming UZS"