# ============================================================================
# paynow/models.py
# ============================================================================
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from paynow.utils import generate_payment_id

User = get_user_model()


class PayNowPayment(models.Model):
    """Model to store PayNow payment transactions"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent to PayNow'),
        ('awaiting_delivery', 'Awaiting Delivery'),
        ('delivered', 'Delivered'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
        ('failed', 'Failed'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('ecocash', 'EcoCash'),
        ('onemoney', 'OneMoney'),
        ('telecash', 'TeleCash'),
        ('visa', 'Visa/Mastercard'),
    ]
    
    # User and identification
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='paynow_payments'
    )
    
    # Payment identifiers
    reference = models.CharField(
        max_length=100,
        unique=True,
        default=generate_payment_id,
        help_text='Unique payment reference'
    )
    poll_url = models.URLField(blank=True, help_text='PayNow poll URL')
    paynow_reference = models.CharField(
        max_length=100,
        blank=True,
        help_text='PayNow internal reference'
    )
    
    # Transaction details
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    
    # Customer details
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    # Status and payment method
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        blank=True
    )
    
    # PayNow response data
    hash_value = models.CharField(max_length=512, blank=True)
    browser_url = models.URLField(blank=True, help_text='Redirect URL for payment')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Additional metadata
    authemail = models.EmailField(blank=True, help_text='Customer auth email')
    additional_info = models.TextField(blank=True)
    
    # Custom fields
    custom_str1 = models.CharField(max_length=255, blank=True)
    custom_str2 = models.CharField(max_length=255, blank=True)
    custom_str3 = models.CharField(max_length=255, blank=True)
    custom_int1 = models.IntegerField(null=True, blank=True)
    custom_int2 = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'PayNow Payment'
        verbose_name_plural = 'PayNow Payments'
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f'Payment {self.reference} - {self.status}'
    
    def mark_paid(self):
        """Mark payment as paid"""
        self.status = 'paid'
        self.paid_at = timezone.now()
        self.save()
    
    def mark_failed(self):
        """Mark payment as failed"""
        self.status = 'failed'
        self.save()
    
    def mark_cancelled(self):
        """Mark payment as cancelled"""
        self.status = 'cancelled'
        self.save()
    
    def get_absolute_url(self):
        return reverse('paynow:payment_detail', kwargs={'reference': self.reference})


class PayNowStatusUpdate(models.Model):
    """Model to log PayNow status updates and polling results"""
    
    payment = models.ForeignKey(
        PayNowPayment,
        on_delete=models.CASCADE,
        related_name='status_updates'
    )
    
    # Status data
    status = models.CharField(max_length=50)
    paynow_reference = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Raw response
    raw_response = models.JSONField(default=dict)
    
    # Hash verification
    hash_verified = models.BooleanField(default=False)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'PayNow Status Update'
        verbose_name_plural = 'PayNow Status Updates'
    
    def __str__(self):
        return f'Update for {self.payment.reference} - {self.status}'

