from django.urls import path
from accounts import views

"""
urlpatterns = [
    path('ingest_csv_from_url/', views.ingest_csv_from_url, name='ingest_data')
]
"""

urlpatterns = [
    path('ingest_csv/', views.IngestCSVFromURL.as_view(), name='ingest-csv-from-url')
]
