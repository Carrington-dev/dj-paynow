
# ============================================================================
# paynow/signals.py
# ============================================================================
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PayNowPayment


@receiver(post_save, sender=PayNowPayment)
def handle_payment_update(sender, instance, created, **kwargs):
    """Handle payment status changes"""
    
    if created:
        print(f"New payment created: {instance.reference}")
    
    elif instance.status == 'paid':
        # Handle successful payment
        print(f"Payment {instance.reference} completed successfully")
        # Add your custom logic here:
        # - Send confirmation email
        # - Grant access to service
        # - Update user subscription
        # etc.

