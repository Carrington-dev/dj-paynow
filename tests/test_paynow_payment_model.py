from django.test import TestCase
from paynow.models import PayNowPayment

class TestPayNowPaymentModel(TestCase):
    def setUp(self):
        self.payment = PayNowPayment.objects.create(
            paynow_reference="REF123",
            amount="100.00",
            description="TestPayNowPaymentModel",
            email="test.model@outlook.com",
            phone="0123456723",
        )

    def test_paynow_payment_model_creatiom(self):
        self.assertIsNotNone(self.payment.id)
        self.assertEqual(self.payment.reference, "REF123")
        self.assertEqual(str(self.payment), "REF123")

