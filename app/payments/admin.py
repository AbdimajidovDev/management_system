from django.contrib import admin

from app.payments.models import Payment

# admin.site.register(Payment)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'moth', 'paid_at')
    search_fields = ('student', 'moth')
    list_filter = ('moth',)
