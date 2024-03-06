"""
Views for creating data
"""

from django.core.management import call_command

from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.utils import DataError
from core.models import (Client, Consumers, ProcessedURL)
from rest_framework.pagination import PageNumberPagination
from .serializers import ConsumerSerializer, BalanceFilterSerializer

import os

class IngestCSVFromURL(APIView):
    def get(self, request):
        csv_url = os.getenv('CSV_URL')
        if not csv_url:
            return Response({'error': 'CSV_URL environment variable is not set'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            call_command('data_ingestion')
            return Response({'success': 'Data ingestion initiated successfully.'})
        except DataError as e:
            return Response({'error': str(e)}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                'consumer_name',
                OpenApiTypes.STR,
                description='Client consumer name'
            ),
            OpenApiParameter(
                'min_balance',
                OpenApiTypes.FLOAT,
                description='minimum balance'
            ),
            OpenApiParameter(
                'max_balance',
                OpenApiTypes.FLOAT,
                description='maximum balance'
            ),
            OpenApiParameter(
                'status',
                OpenApiTypes.STR, enum=['IN_COLLECTION', 'INACTIVE', 'PAID_IN_FULL'],
                description='different status to filter by'
            )
        ]
    )
)
class ConsumerList(APIView):
    class CustomPagination(PageNumberPagination):
        page_size = 10

    def get(self, request, *args, **kwargs):
        serializer = BalanceFilterSerializer(data=request.query_params)
        if serializer.is_valid():

            validated_data = serializer.validated_data

            print(validated_data)

            consumers = Consumers.objects.all()

            min_balance = validated_data.get('min_balance')
            max_balance = validated_data.get('max_balance')
            consumer_name = request.query_params.get('consumer_name')
            status = request.query_params.get('status')

            if min_balance is not None:
                consumers = consumers.filter(balance__gte=min_balance)
            if max_balance is not None:
                consumers = consumers.filter(balance__lte=max_balance)
            if consumer_name:
                consumers = consumers.filter(consumer_name__icontains=consumer_name)
            if status:
                consumers = consumers.filter(status__iexact=status)

            paginator = self.CustomPagination()
            result_page = paginator.paginate_queryset(consumers, request)

            response_serializer = ConsumerSerializer(result_page, many=True, context={'request': request})

            return paginator.get_paginated_response(response_serializer.data)
        else:
            return Response({'error': serializer.errors}, status=400)

