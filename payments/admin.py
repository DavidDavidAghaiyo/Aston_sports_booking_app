from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
  list_display = ('user', 'amount', 'date') #Fields in the payment model
  search_fields = ('user_username', 'amount') 
  list_filter = ('date',)


