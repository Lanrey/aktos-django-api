from rest_framework import serializers
from core.models import (Client, Consumers, ProcessedURL)


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumers
        fields = ['id', 'client_reference_no', 'balance', 'consumer_name', 'status', 'consumer_address',
                  'ssn','created_at', 'updated']
