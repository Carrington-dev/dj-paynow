# ============================================================================
# paynow/apps.py
# ============================================================================
from django.apps import AppConfig


class PayNowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'paynow'
    verbose_name = 'PayNow Payments'

    def ready(self):
        import paynow.signals  # Register signals


