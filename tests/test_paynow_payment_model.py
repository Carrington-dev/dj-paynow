from decimal import Decimal
from django.test import TestCase
from paynow.models import PayNowPayment


class TestPayNowPaymentModel(TestCase):
    """Test PayNowPayment model creation"""
    
    def setUp(self):
        """Set up test data"""
        self.payment = PayNowPayment.objects.create(
            paynow_reference="REF123",
            amount=Decimal("100.00"),
            description="TestPayNowPaymentModel",
            email="test.model@outlook.com",
            phone="0123456723",
        )

    def test_paynow_payment_model_creation(self):
        """Test that payment model is created successfully"""
        self.assertIsNotNone(self.payment.id)
        # Note: 'reference' is auto-generated, not 'paynow_reference'
        self.assertIsNotNone(self.payment.reference)
        self.assertTrue(self.payment.reference.startswith('PN'))
        self.assertEqual(self.payment.paynow_reference, "REF123")
        self.assertEqual(self.payment.amount, Decimal("100.00"))
        # String representation uses the auto-generated reference
        self.assertIn(self.payment.reference, str(self.payment))