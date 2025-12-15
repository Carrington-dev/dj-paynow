from decimal import Decimal
from unittest.mock import patch, Mock
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from paynow.models import PayNowPayment, PayNowStatusUpdate

User = get_user_model()


class CheckoutViewTest(TestCase):
    """Test checkout view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
    
    @patch('paynow.views.PayNowClient')
    def test_checkout_success(self, mock_client_class):
        """Test successful checkout"""
        # Mock PayNow client
        mock_client = Mock()
        mock_client.initiate_transaction.return_value = {
            'success': True,
            'poll_url': 'http://paynow.co.zw/poll/123',
            'browser_url': 'http://paynow.co.zw/pay/123',
            'hash': 'HASH123',
        }
        mock_client_class.return_value = mock_client
        
        # Make request
        response = self.client.get(reverse('paynow:checkout'), {
            'amount': '100.00',
            'description': 'Test Payment',
            'email': 'customer@example.com',
            'phone': '+263771234567',
        })
        
        # Should redirect to PayNow
        self.assertEqual(response.status_code, 302)
        self.assertIn('paynow.co.zw', response.url)
        
        # Payment should be created
        payment = PayNowPayment.objects.first()
        self.assertIsNotNone(payment)
        self.assertEqual(payment.amount, Decimal('100.00'))
        self.assertEqual(payment.status, 'sent')
    
    @patch('paynow.views.PayNowClient')
    def test_checkout_failure(self, mock_client_class):
        """Test checkout with PayNow error"""
        mock_client = Mock()
        mock_client.initiate_transaction.return_value = {
            'success': False,
            'error': 'Invalid credentials',
        }
        mock_client_class.return_value = mock_client
        
        response = self.client.get(reverse('paynow:checkout'), {
            'amount': '100.00',
            'description': 'Test',
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid credentials')
        
        # Payment should be marked as failed
        payment = PayNowPayment.objects.first()
        self.assertEqual(payment.status, 'failed')
    
    def test_checkout_requires_login(self):
        """Test checkout requires authentication"""
        self.client.logout()
        
        response = self.client.get(reverse('paynow:checkout'))
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response.url)


class PaymentDetailViewTest(TestCase):
    """Test payment detail view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.payment = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            description='Test Payment',
            email='test@example.com',
        )
    
    def test_payment_detail_view(self):
        """Test viewing payment details"""
        url = reverse('paynow:payment_detail', kwargs={
            'reference': self.payment.reference
        })
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.payment.reference)
        self.assertContains(response, '100.00')
    
    def test_payment_detail_not_found(self):
        """Test viewing non-existent payment"""
        url = reverse('paynow:payment_detail', kwargs={
            'reference': 'INVALID123'
        })
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class PaymentReturnViewTest(TestCase):
    """Test payment return view"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.payment = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            description='Test Payment',
            email='test@example.com',
            poll_url='http://paynow.co.zw/poll/123',
        )
    
    @patch('paynow.views.PayNowClient')
    def test_return_view_paid(self, mock_client_class):
        """Test return view with paid status"""
        mock_client = Mock()
        mock_client.check_transaction_status.return_value = {
            'success': True,
            'status': 'Paid',
            'paynow_reference': 'PN123456',
        }
        mock_client_class.return_value = mock_client
        
        url = reverse('paynow:payment_return', kwargs={
            'reference': self.payment.reference
        })
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'success')
        
        # Payment should be marked as paid
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, 'paid')
    
    @patch('paynow.views.PayNowClient')
    def test_return_view_pending(self, mock_client_class):
        """Test return view with pending status"""
        mock_client = Mock()
        mock_client.check_transaction_status.return_value = {
            'success': True,
            'status': 'Sent',
        }
        mock_client_class.return_value = mock_client
        
        url = reverse('paynow:payment_return', kwargs={
            'reference': self.payment.reference
        })
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'pending')


class PaymentResultWebhookTest(TestCase):
    """Test payment result webhook"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.payment = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            description='Test Payment',
            email='test@example.com',
        )
    
    @patch('paynow.views.verify_hash')
    def test_webhook_paid(self, mock_verify):
        """Test webhook with paid status"""
        mock_verify.return_value = True
        
        data = {
            'reference': self.payment.reference,
            'paynowreference': 'PN123456',
            'status': 'Paid',
            'amount': '100.00',
            'hash': 'HASH123',
        }
        
        response = self.client.post(reverse('paynow:payment_result'), data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), 'OK')
        
        # Payment should be marked as paid
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, 'paid')
        self.assertIsNotNone(self.payment.paid_at)
        
        # Status update should be created
        update = PayNowStatusUpdate.objects.first()
        self.assertIsNotNone(update)
        self.assertEqual(update.status, 'Paid')
        self.assertTrue(update.hash_verified)
    
    @patch('paynow.views.verify_hash')
    def test_webhook_cancelled(self, mock_verify):
        """Test webhook with cancelled status"""
        mock_verify.return_value = True
        
        data = {
            'reference': self.payment.reference,
            'status': 'Cancelled',
            'hash': 'HASH123',
        }
        
        response = self.client.post(reverse('paynow:payment_result'), data)
        
        self.assertEqual(response.status_code, 200)
        
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, 'cancelled')
    
    @patch('paynow.views.verify_hash')
    def test_webhook_invalid_hash(self, mock_verify):
        """Test webhook with invalid hash"""
        mock_verify.return_value = False
        
        data = {
            'reference': self.payment.reference,
            'status': 'Paid',
            'hash': 'INVALID',
        }
        
        response = self.client.post(reverse('paynow:payment_result'), data)
        
        # Should still return 200 (to prevent retries)
        self.assertEqual(response.status_code, 200)
        
        # Status update logged but not verified
        update = PayNowStatusUpdate.objects.first()
        self.assertFalse(update.hash_verified)
        
        # Payment status should not change
        self.payment.refresh_from_db()
        self.assertEqual(self.payment.status, 'pending')
    
    def test_webhook_missing_reference(self):
        """Test webhook without reference"""
        data = {
            'status': 'Paid',
            'hash': 'HASH123',
        }
        
        response = self.client.post(reverse('paynow:payment_result'), data)
        
        self.assertEqual(response.status_code, 400)
    
    def test_webhook_invalid_reference(self):
        """Test webhook with invalid reference"""
        data = {
            'reference': 'INVALID123',
            'status': 'Paid',
            'hash': 'HASH123',
        }
        
        response = self.client.post(reverse('paynow:payment_result'), data)
        
        self.assertEqual(response.status_code, 404)
    
    @patch('paynow.views.get_client_ip')
    @patch('paynow.views.verify_hash')
    def test_webhook_logs_ip(self, mock_verify, mock_get_ip):
        """Test webhook logs IP address"""
        mock_verify.return_value = True
        mock_get_ip.return_value = '192.168.1.1'
        
        data = {
            'reference': self.payment.reference,
            'status': 'Paid',
            'hash': 'HASH123',
        }
        
        self.client.post(reverse('paynow:payment_result'), data)
        
        update = PayNowStatusUpdate.objects.first()
        self.assertEqual(update.ip_address, '192.168.1.1')