from rest_framework import generics

from .models import Payment
from app.payments.serializers import PaymentSerializer
from app.users.permissions import IsAdminOrSuperAdmin


class PaymentView(generics.ListCreateAPIView):
    permission_classes = (IsAdminOrSuperAdmin,)
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
