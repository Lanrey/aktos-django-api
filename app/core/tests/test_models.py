"""
Django test to test models
"""

from django.test import TestCase
from core import models
from django.core.exceptions import ValidationError


class ClientModelTest(TestCase):
    def test_client_creation(self):
        client = Client.objects.create(name="Test Client")
        self.assertEqual(client.name, "Test Client")
        self.assertTrue(client.created_at)
        self.assertTrue(client.updated)
