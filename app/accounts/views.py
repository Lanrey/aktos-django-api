"""
Views for creating data
"""

from django.core.management import call_command

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.utils import DataError
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




"""
@require_http_methods(["GET"])
def ingest_csv_from_url(request):
    csv_url = os.getenv('CSV_URL')
    if not csv_url:
        return JsonResponse({'error': 'CSV_URL environment variable is not set'}, status=400)
    try:
        call_command('data_ingestion', csv_url=csv_url)
        return JsonResponse({'success': 'Data ingestion initiated successfully.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
"""

