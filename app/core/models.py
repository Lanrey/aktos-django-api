"""
Models for the Consumer and the Accounts
"""

from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator

import uuid

ssn_validator = RegexValidator(
    regex=r'^\d{3}-\d{2}-\d{4}$',
    message="SSN must be entered in the format: 'XXX-XX-XXXX'. Up to 9 digits allowed."
)


class Status(models.TextChoices):
    IN_COLLECTION = 'IN_COLLECTION'
    INACTIVE = 'INACTIVE'
    PAID_IN_FULL = 'PAID_IN_FULL'


class Client(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Consumers(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_reference_no = models.UUIDField(default=uuid.uuid4, editable=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices)
    consumer_name = models.CharField(max_length=255)
    consumer_address = models.TextField()
    ssn = models.CharField(max_length=11, validators=[ssn_validator],
                           help_text="Enter ssn in the format XXX-XX-XXXX")
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
