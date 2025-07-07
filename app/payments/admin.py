from django.contrib import admin

from app.payments.models import Payment
from app.users.models import User


# admin.site.register(Payment)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'student__group', 'amount', 'moth', 'paid_at')
    search_fields = ('student', 'moth')
    list_filter = ('moth',)

    def get_queryset(self, request):
        user = request.user
        qs = super().get_queryset(request)

        if user.is_staff and hasattr(user, 'role') and user.role == User.UserRoles.teacher:
            return qs.filter(student__group__teacher=user)
        return qs
