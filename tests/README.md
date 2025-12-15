# dj-paynow Testing Guide

Complete testing suite for the dj-paynow Django package using pytest and Django's TestCase.

## Setup

### Install Test Dependencies

```bash
pip install -e ".[dev]"
```

Or install manually:

```bash
pip install pytest pytest-django pytest-cov
```

### Project Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest configuration
├── urls.py                  # Test URL configuration
├── test_models.py           # Model tests
├── test_utils.py            # Utility function tests
├── test_client.py           # PayNow client tests
├── test_views.py            # View tests
├── test_api.py              # REST API tests
├── test_signals.py          # Signal tests
└── README.md                # This file
```

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test Files

```bash
# Run model tests only
pytest tests/test_models.py

# Run view tests only
pytest tests/test_views.py

# Run API tests only
pytest tests/test_api.py
```

### Run Specific Test Classes

```bash
# Run specific test class
pytest tests/test_models.py::PayNowPaymentModelTest

# Run specific test method
pytest tests/test_models.py::PayNowPaymentModelTest::test_create_payment
```

### Run with Coverage

```bash
# Run with coverage report
pytest --cov=paynow --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Run with Verbose Output

```bash
pytest -v
```

### Run and Show Print Statements

```bash
pytest -s
```

## Test Categories

### Unit Tests

Test individual components in isolation:

```bash
pytest -m unit
```

### Integration Tests

Test component interactions:

```bash
pytest -m integration
```

### API Tests

Test REST API endpoints:

```bash
pytest -m api
```

## Test Configuration

Tests are configured via `conftest.py` which:
- Configures Django settings programmatically
- Sets up in-memory SQLite database
- Configures test apps and middleware
- Sets PayNow test credentials

## Writing New Tests

### Model Tests

```python
from django.test import TestCase
from paynow.models import PayNowPayment

class MyModelTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.payment = PayNowPayment.objects.create(
            amount='100.00',
            description='Test',
            email='test@example.com',
        )
    
    def test_something(self):
        """Test description"""
        self.assertEqual(self.payment.status, 'pending')
```

### View Tests

```python
from django.test import TestCase, Client
from django.urls import reverse

class MyViewTest(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_view(self):
        response = self.client.get(reverse('paynow:checkout'))
        self.assertEqual(response.status_code, 200)
```

### API Tests

```python
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class MyAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_api_endpoint(self):
        url = '/paynow/payments/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

## Mocking External Services

PayNow API calls are mocked in tests:

```python
from unittest.mock import patch, Mock

@patch('paynow.views.PayNowClient')
def test_with_mock(self, mock_client_class):
    mock_client = Mock()
    mock_client.initiate_transaction.return_value = {
        'success': True,
        'browser_url': 'http://example.com',
    }
    mock_client_class.return_value = mock_client
    
    # Your test code here
```

## Common Test Patterns

### Testing Payment Creation

```python
def test_create_payment(self):
    payment = PayNowPayment.objects.create(
        amount='100.00',
        description='Test Payment',
        email='test@example.com',
    )
    
    self.assertIsNotNone(payment.id)
    self.assertTrue(payment.reference.startswith('PN'))
```

### Testing Status Changes

```python
def test_mark_paid(self):
    payment = PayNowPayment.objects.create(
        amount='100.00',
        description='Test',
        email='test@example.com',
    )
    
    payment.mark_paid()
    
    self.assertEqual(payment.status, 'paid')
    self.assertIsNotNone(payment.paid_at)
```

### Testing Webhooks

```python
def test_webhook(self):
    payment = PayNowPayment.objects.create(
        amount='100.00',
        description='Test',
        email='test@example.com',
    )
    
    data = {
        'reference': payment.reference,
        'status': 'Paid',
        'hash': 'VALID_HASH',
    }
    
    response = self.client.post(
        reverse('paynow:payment_result'),
        data
    )
    
    self.assertEqual(response.status_code, 200)
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
    
    - name: Run tests
      run: |
        pytest --cov=paynow --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Continuous Testing

### Watch for Changes

```bash
# Install pytest-watch
pip install pytest-watch

# Run tests on file changes
ptw
```

## Debugging Tests

### Run Single Test with PDB

```bash
pytest tests/test_models.py::test_create_payment --pdb
```

### Show Print Statements

```bash
pytest -s
```

### Increase Verbosity

```bash
pytest -vv
```

## Coverage Goals

Target coverage: **90%+**

Current coverage:
- Models: 100%
- Views: 95%
- Utils: 100%
- Client: 90%

## Best Practices

1. **Isolation**: Each test should be independent
2. **Setup/Teardown**: Use `setUp()` and `tearDown()` methods
3. **Descriptive Names**: Test names should describe what they test
4. **One Assertion**: Focus each test on one thing
5. **Mock External**: Always mock PayNow API calls
6. **Test Edge Cases**: Test both success and failure paths

## Troubleshooting

### Tests Not Found

Ensure pytest can find tests:
```bash
pytest --collect-only
```

### Import Errors

Make sure package is installed:
```bash
pip install -e .
```

### Database Errors

Tests use in-memory SQLite - no setup needed.

### Django Not Configured

`conftest.py` handles Django configuration automatically.

## Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)

## Questions?

Open an issue on GitHub or contact carrington.muleya@outlook.com