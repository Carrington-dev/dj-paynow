from decimal import Decimal
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from paynow.models import PayNowPayment

User = get_user_model()


class PaymentSignalsTest(TestCase):
    """Test payment signals"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    @patch('paynow.signals.print')
    def test_signal_on_payment_creation(self, mock_print):
        """Test signal is triggered on payment creation"""
        payment = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            description='Test Payment',
            email='test@example.com',
        )
        
        # Signal should print creation message
        mock_print.assert_called()
        call_args = str(mock_print.call_args_list)
        self.assertIn('New payment created', call_args)
        self.assertIn(payment.reference, call_args)
    
    @patch('paynow.signals.print')
    def test_signal_on_payment_status_change(self, mock_print):
        """Test signal is triggered on status change to paid"""
        payment = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            description='Test Payment',
            email='test@example.com',
        )
        
        # Clear previous calls
        mock_print.reset_mock()
        
        # Mark as paid
        payment.status = 'paid'
        payment.save()
        
        # Signal should print completion message
        mock_print.assert_called()
        call_args = str(mock_print.call_args_list)
        self.assertIn('completed successfully', call_args)
        self.assertIn(payment.reference, call_args)
    
    @patch('paynow.signals.print')
    def test_signal_not_triggered_on_other_status(self, mock_print):
        """Test signal doesn't print completion for non-paid status"""
        payment = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            description='Test Payment',
            email='test@example.com',
        )
        
        mock_print.reset_mock()
        
        # Change to failed status
        payment.status = 'failed'
        payment.save()
        
        # Should not print completion message
        if mock_print.called:
            call_args = str(mock_print.call_args_list)
            self.assertNotIn('completed successfully', call_args)


class SignalIntegrationTest(TestCase):
    """Integration tests for signals with custom logic"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_signal_workflow(self):
        """Test complete signal workflow"""
        # Create payment
        payment = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            description='Test Payment',
            email='test@example.com',
        )
        
        self.assertEqual(payment.status, 'pending')
        
        # Update to sent
        payment.status = 'sent'
        payment.save()
        
        # Finally mark as paid
        payment.mark_paid()
        
        self.assertEqual(payment.status, 'paid')
        self.assertIsNotNone(payment.paid_at)