from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from paynow.models import PayNowPayment, PayNowStatusUpdate

User = get_user_model()


class PayNowPaymentModelTest(TestCase):
    """Test PayNowPayment model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_payment(self):
        """Test creating a payment"""
        payment = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            description='Test Payment',
            email='customer@example.com',
            phone='+263771234567',
        )
        
        self.assertIsNotNone(payment.id)
        self.assertIsNotNone(payment.reference)
        self.assertEqual(payment.amount, Decimal('100.00'))
        self.assertEqual(payment.status, 'pending')
        self.assertTrue(payment.reference.startswith('PN'))
    
    def test_payment_str_representation(self):
        """Test payment string representation"""
        payment = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('50.00'),
            description='Test',
            email='test@example.com',
        )
        
        expected = f'Payment {payment.reference} - pending'
        self.assertEqual(str(payment), expected)
    
    def test_mark_paid(self):
        """Test marking payment as paid"""
        payment = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            description='Test',
            email='test@example.com',
        )
        
        self.assertIsNone(payment.paid_at)
        payment.mark_paid()
        
        self.assertEqual(payment.status, 'paid')
        self.assertIsNotNone(payment.paid_at)
        self.assertLessEqual(payment.paid_at, timezone.now())
    
    def test_mark_failed(self):
        """Test marking payment as failed"""
        payment = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            description='Test',
            email='test@example.com',
        )
        
        payment.mark_failed()
        self.assertEqual(payment.status, 'failed')
    
    def test_mark_cancelled(self):
        """Test marking payment as cancelled"""
        payment = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            description='Test',
            email='test@example.com',
        )
        
        payment.mark_cancelled()
        self.assertEqual(payment.status, 'cancelled')
    
    def test_payment_without_user(self):
        """Test creating payment without user"""
        payment = PayNowPayment.objects.create(
            amount=Decimal('100.00'),
            description='Guest Payment',
            email='guest@example.com',
        )
        
        self.assertIsNone(payment.user)
        self.assertIsNotNone(payment.reference)
    
    def test_custom_fields(self):
        """Test custom fields"""
        payment = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            description='Test',
            email='test@example.com',
            custom_str1='custom_value_1',
            custom_str2='custom_value_2',
            custom_int1=123,
            custom_int2=456,
        )
        
        self.assertEqual(payment.custom_str1, 'custom_value_1')
        self.assertEqual(payment.custom_str2, 'custom_value_2')
        self.assertEqual(payment.custom_int1, 123)
        self.assertEqual(payment.custom_int2, 456)
    
    def test_get_absolute_url(self):
        """Test get_absolute_url method"""
        payment = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            description='Test',
            email='test@example.com',
        )
        
        url = payment.get_absolute_url()
        expected = f'/paynow/payment/{payment.reference}/'
        self.assertEqual(url, expected)
    
    def test_payment_ordering(self):
        """Test payments are ordered by created_at desc"""
        payment1 = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('100.00'),
            description='First',
            email='test@example.com',
        )
        
        payment2 = PayNowPayment.objects.create(
            user=self.user,
            amount=Decimal('200.00'),
            description='Second',
            email='test@example.com',
        )
        
        payments = PayNowPayment.objects.all()
        self.assertEqual(payments[0], payment2)
        self.assertEqual(payments[1], payment1)


class PayNowStatusUpdateModelTest(TestCase):
    """Test PayNowStatusUpdate model"""
    
    def setUp(self):
        """Set up test data"""
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