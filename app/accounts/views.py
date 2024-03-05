"""
Views for creating data
"""
import os
from django.http import JsonResponse
from django.core.management import call_command
from django.views.decorators.http import require_http_methods

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
