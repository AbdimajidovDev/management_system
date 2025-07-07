from rest_framework import serializers

from app.payments.models import Payment
from app.students.models import Student


class PaymentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('date', 'paid_at')

    def get_queryset(self):
        print('self.instance: ', self.instance)
        return Payment.objects.all()

