# dj-paynow - Django + PayNow Made Easy

[![PyPI version](https://img.shields.io/pypi/v/dj-paynow.svg)](https://pypi.org/project/dj-paynow/)
[![Python versions](https://img.shields.io/pypi/pyversions/dj-paynow.svg)](https://pypi.org/project/dj-paynow/)
[![Django versions](https://img.shields.io/pypi/djversions/dj-paynow.svg)](https://pypi.org/project/dj-paynow/)
[![License](https://img.shields.io/github/license/carrington-dev/dj-paynow.svg)](LICENSE)

Complete PayNow payment gateway integration for Django applications. Accept payments from Zimbabwean customers using EcoCash, OneMoney, Visa/Mastercard, and more.

## Introduction

**dj-paynow** is a comprehensive Django library for integrating PayNow, Zimbabwe's leading payment gateway. It provides a simple, secure, and Pythonic way to accept online payments.

## Features

- **Easy Integration** - Get started in under 10 minutes
- **Multiple Payment Methods** - EcoCash, OneMoney, TeleCash, Visa/Mastercard
- **Secure** - Hash verification and validation
- **Complete** - Models, forms, views, and webhooks included
- **Database Tracking** - Complete payment history
- **Django Admin** - Full admin integration
- **REST API** - Optional DRF support
- **Status Polling** - Real-time payment status updates

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST Framework 3.12+
- requests 2.25.0+
- PayNow Account (sign up at [paynow.co.zw](https://www.paynow.co.zw))

## Installation

### 1. Install via pip

```bash
pip install dj-paynow
```

### 2. Add to `INSTALLED_APPS`

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',  # Optional, for API support
    'paynow',         # Add this
    
    # Your apps
    'myapp',
]
```

### 3. Configure Settings

Add your PayNow credentials to `settings.py`:

```python
# PayNow Configuration
PAYNOW_INTEGRATION_ID = 'your_integration_id'
PAYNOW_INTEGRATION_KEY = 'your_integration_key'
PAYNOW_TEST_MODE = True  # False for production
```

**Environment Variables (Recommended):**

```bash
pip install dotzen
```


```python
from dotzen import config

PAYNOW_INTEGRATION_ID = config('PAYNOW_INTEGRATION_ID')
PAYNOW_INTEGRATION_KEY = config('PAYNOW_INTEGRATION_KEY')
PAYNOW_TEST_MODE = config('PAYNOW_TEST_MODE', 'True') == 'True'
```

### 4. Configure URLs

```python
# urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('paynow/', include('paynow.urls')),
]
```

### 5. Run Migrations

```bash
python manage.py migrate
```

## Quick Start

### Create a Payment

```python
from django.shortcuts import redirect, reverse
from urllib.parse import urlencode

def buy_product(request):
    """Create payment and redirect to PayNow"""
    
    params = urlencode({
        'amount': '50.00',
        'description': 'Premium Subscription',
        'email': request.user.email,
        'phone': '+263771234567',
    })
    
    url = f"{reverse('paynow:checkout')}?{params}"
    return redirect(url)
```

### Using the API

```python
import requests

# Create payment
response = requests.post('http://localhost:8000/paynow/payments/', json={
    'amount': '100.00',
    'description': 'Product Purchase',
    'email': 'customer@example.com',
    'phone': '+263771234567',
})

payment = response.json()
# Redirect user to payment['paynow_url']
```

## Payment Flow

1. **Create Payment** - Create a payment record with amount and description
2. **Initialize with PayNow** - Send request to PayNow to get payment URL
3. **Redirect User** - Redirect customer to PayNow payment page
4. **Customer Pays** - Customer completes payment via EcoCash/OneMoney/Card
5. **Receive Webhook** - PayNow sends status update to your webhook
6. **Poll Status** - Optionally poll for payment status
7. **Update Status** - Payment status updated in database

## Payment Methods

PayNow supports multiple payment methods:

- **EcoCash** - Mobile money (most popular in Zimbabwe)
- **OneMoney** - NetOne mobile money
- **TeleCash** - Telecel mobile money
- **Visa/Mastercard** - Credit and debit cards

Customers choose their preferred method on the PayNow payment page.

## Webhook Handling

PayNow sends notifications to your result URL when payment status changes:

```python
# Webhook endpoint: /paynow/result/
# This is handled automatically by dj-paynow

# You can add custom logic using Django signals:
from django.db.models.signals import post_save
from django.dispatch import receiver
from paynow.models import PayNowPayment

@receiver(post_save, sender=PayNowPayment)
def handle_payment_complete(sender, instance, **kwargs):
    if instance.status == 'paid':
        # Grant access to service
        grant_premium_access(instance.user)
        
        # Send confirmation email
        send_confirmation_email(instance)
```

## Status Polling

Check payment status programmatically:

```python
from paynow.paynow_client import PayNowClient

client = PayNowClient()
payment = PayNowPayment.objects.get(reference='PN123456789')

if payment.poll_url:
    status = client.check_transaction_status(payment.poll_url)
    
    if status['success']:
        print(f"Status: {status['status']}")
        print(f"Reference: {status['paynow_reference']}")
```

## Models

### PayNowPayment

Stores payment transaction data:

```python
payment = PayNowPayment.objects.create(
    user=request.user,
    amount=99.99,
    description='Premium Plan',
    email='user@example.com',
    phone='+263771234567',
)
```

**Fields:**
- `reference` - Unique payment reference
- `amount` - Payment amount (decimal)
- `description` - Payment description
- `email` - Customer email
- `phone` - Customer phone number
- `status` - Payment status (pending, sent, paid, failed, etc.)
- `poll_url` - URL for status polling
- `browser_url` - PayNow payment page URL
- `paynow_reference` - PayNow internal reference

### PayNowStatusUpdate

Logs all status updates and webhook calls:

```python
updates = payment.status_updates.all()
for update in updates:
    print(f"{update.status} at {update.created_at}")
```

## Django Admin

Full admin interface included:

- View all payments
- Filter by status, date
- Search by reference, email
- View status update history
- Manual status updates

Access at: `/admin/paynow/`

## REST API

Optional REST API endpoints:

```
GET    /paynow/payments/              - List payments
POST   /paynow/payments/              - Create payment
GET    /paynow/payments/{reference}/  - Get payment details
```

## Security

dj-paynow implements security best practices:

1. **Hash Verification** - All responses verified with SHA512 hash
2. **Status Logging** - All webhook calls logged for audit
3. **Environment Variables** - Credentials stored securely
4. **HTTPS Required** - Production requires HTTPS

## Testing

PayNow provides a sandbox environment for testing:

1. Sign up at [paynow.co.zw](https://www.paynow.co.zw)
2. Get sandbox credentials
3. Set `PAYNOW_TEST_MODE = True`
4. Test with EcoCash sandbox numbers

## Examples

### Subscription Payment

```python
def subscribe_to_plan(request, plan_id):
    plan = get_object_or_404(Plan, id=plan_id)
    
    params = urlencode({
        'amount': plan.price,
        'description': f'{plan.name} Subscription',
        'email': request.user.email,
    })
    
    return redirect(f"{reverse('paynow:checkout')}?{params}")
```

### Donation Widget

```python
def process_donation(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        
        params = urlencode({
            'amount': amount,
            'description': 'Donation',
            'email': email,
        })
        
        return redirect(f"{reverse('paynow:checkout')}?{params}")
    
    return render(request, 'donate.html')
```

## Getting PayNow Credentials

1. Visit [paynow.co.zw](https://www.paynow.co.zw)
2. Sign up for an account
3. Navigate to Settings → Integrations
4. Copy your Integration ID and Integration Key
5. Add them to your environment variables

## Troubleshooting

**Payment not updating?**
- Check webhook URL is publicly accessible
- Verify hash in status updates
- Check PayNow status update logs in admin

**Hash verification failing?**
- Ensure integration key is correct
- Check for extra spaces in credentials

**Webhook not receiving calls?**
- Use ngrok for local development
- Verify result URL is correct
- Check server logs for errors

## Support

- **GitHub**: [github.com/carrington-dev/dj-paynow](https://github.com/carrington-dev/dj-paynow)
- **Issues**: [GitHub Issues](https://github.com/carrington-dev/dj-paynow/issues)
- **Email**: carrington.muleya@outlook.com
- **PayNow Docs**: [paynow.co.zw/developers](https://www.paynow.co.zw/developers)

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License - See [LICENSE](LICENSE) file

## Acknowledgments

Inspired by:
- [dj-payfast](https://github.com/carrington-dev/dj-payfast)
- [dj-stripe](https://github.com/dj-stripe/dj-stripe)

## Changelog

### 0.1.0 (2025-12-15)
- Initial release
- PayNow integration
- Payment models
- Webhook handling
- Status polling
- REST API
- Django admin

---

Made with ❤️ for the Zimbabwean developer community
