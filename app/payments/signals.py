from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Payment



def update_student_payment_status(student):
    total_paid = student.payments.aggregate(total=Sum('amount'))['total'] or 0
    is_paid = total_paid >= student.group.price
    if student.is_paid != is_paid:
        student.is_paid = is_paid
        student.save()

@receiver(post_save, sender=Payment)
def payment_save(sender, instance, **kwargs):
    update_student_payment_status(instance.student)


@receiver(post_delete, sender=Payment)
def payment_deletes(sender, instance, **kwargs):
    update_student_payment_status(instance.student)

