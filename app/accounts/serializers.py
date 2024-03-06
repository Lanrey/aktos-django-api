from rest_framework import serializers
from core.models import (Client, Consumers, ProcessedURL)


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumers
        fields = ['id', 'client_reference_no', 'balance', 'consumer_name', 'status', 'consumer_address',
                  'ssn','created_at', 'updated']


class BalanceFilterSerializer(serializers.Serializer):
    min_balance = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)
    max_balance = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, allow_null=True)


