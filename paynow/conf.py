# ============================================================================
# paynow/conf.py
# ============================================================================
from django.conf import settings

# PayNow Configuration
PAYNOW_INTEGRATION_ID = getattr(settings, 'PAYNOW_INTEGRATION_ID', '')
PAYNOW_INTEGRATION_KEY = getattr(settings, 'PAYNOW_INTEGRATION_KEY', '')
PAYNOW_TEST_MODE = getattr(settings, 'PAYNOW_TEST_MODE', True)

# PayNow URLs
if PAYNOW_TEST_MODE:
    PAYNOW_INIT_URL = 'https://www.paynow.co.zw/interface/initiatetransaction'
    PAYNOW_STATUS_URL = 'https://www.paynow.co.zw/interface/pollurl'
else:
    PAYNOW_INIT_URL = 'https://www.paynow.co.zw/interface/initiatetransaction'
    PAYNOW_STATUS_URL = 'https://www.paynow.co.zw/interface/pollurl'


