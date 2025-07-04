from django.urls import path
from .views import PaymentView

urlpatterns = [
    path('billing/', PaymentView.as_view(), name='billing'),
]