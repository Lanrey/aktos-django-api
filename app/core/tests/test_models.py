"""
Django test to test models
"""

from django.test import TestCase
from core import models
from django.core.exceptions import ValidationError


class ClientModelTest(TestCase):
    def test_client_creation(self):
        client = models.Client.objects.create(name="Test Client")
        self.assertEqual(client.name, "Test Client")
        self.assertTrue(client.created_at)
        self.assertTrue(client.updated)


class ConsumerModelTest(TestCase):
    def setUp(self):
        self.client = models.Client.objects.create(name="Test Client")

    def test_consumer_creation(self):
        consumer = models.Consumers.objects.create(
            client=self.client,
            client_reference_no='ffeb5d88-e5af-45f0-9637-16ea469c58c0',
            balance=100.50,
            status=models.Status.IN_COLLECTION,
            consumer_name="John Doe",
            consumer_address="123 Main St",
            ssn="123-45-6789"
        )
        self.assertEqual(consumer.client, self.client)
        self.assertEqual(consumer.balance, 100.50)
        self.assertEqual(consumer.status, models.Status.IN_COLLECTION)
        self.assertEqual(consumer.consumer_name, "John Doe")
        self.assertEqual(consumer.consumer_address, "123 Main St")
        self.assertEqual(consumer.ssn, "123-45-6789")
        self.assertTrue(consumer.client_reference_no)
        self.assertTrue(consumer.created_at)
        self.assertTrue(consumer.updated)

    def test_ssn_validation_error(self):
        with self.assertRaises(ValidationError):
            models.Consumers.objects.create(
                client=self.client,
                balance=100.50,
                status=models.Status.IN_COLLECTION,
                consumer_name="Jane Doe",
                consumer_address="123 Main St",
                ssn="invalid-ssn"
            ).full_clean()



