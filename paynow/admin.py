# ============================================================================
# paynow/admin.py
# ============================================================================
from django.contrib import admin
from .models import PayNowPayment, PayNowStatusUpdate

admin.site.site_header = "PayNow Payment Portal"
admin.site.site_title = "PayNow Portal"
admin.site.index_title = "Welcome to PayNow Payment Portal"


@admin.register(PayNowPayment)
class PayNowPaymentAdmin(admin.ModelAdmin):
    """Admin configuration for PayNowPayment"""
    
    list_display = [
        'reference',
        'user',
        'amount',
        'status',
        'email',
        'created_at',
        'paid_at',
    ]
    
    list_filter = [
        'status',
        'payment_method',
        'created_at',
        'paid_at',
    ]
    
    search_fields = [
        'reference',
        'paynow_reference',
        'email',
        'description',
    ]
    
    readonly_fields = [
        'reference',
        'poll_url',
        'browser_url',
        'hash_value',
        'created_at',
        'updated_at',
        'paid_at',
    ]
    
    fieldsets = (
        ('Payment Information', {
            'fields': (
                'reference',
                'paynow_reference',
                'user',
                'status',
                'payment_method',
            )
        }),
        ('Transaction Details', {
            'fields': (
                'amount',
                'description',
            )
        }),
        ('Customer Details', {
            'fields': (
                'email',
                'phone',
                'authemail',
            )
        }),
        ('PayNow Data', {
            'fields': (
                'poll_url',
                'browser_url',
                'hash_value',
            )
        }),
        ('Custom Fields', {
            'classes': ('collapse',),
            'fields': (
                'custom_str1',
                'custom_str2',
                'custom_str3',
                'custom_int1',
                'custom_int2',
                'additional_info',
            )
        }),
        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
                'paid_at',
            )
        }),
    )


@admin.register(PayNowStatusUpdate)
class PayNowStatusUpdateAdmin(admin.ModelAdmin):
    """Admin configuration for PayNowStatusUpdate"""
    
    list_display = [
        'id',
        'payment',
        'status',
        'hash_verified',
        'created_at',
    ]
    
    list_filter = [
        'status',
        'hash_verified',
        'created_at',
    ]
    
    search_fields = [
        'payment__reference',
        'paynow_reference',
    ]
    
    readonly_fields = '__all__'

