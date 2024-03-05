from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from django.db.utils import IntegrityError, DataError


class IngestCSVFromURLTest(APITestCase):

    @patch('accounts.views.call_command')
    def test_ingest_success(self, mock_call_command):
        # Mock environment variable
        with patch.dict('os.environ', {'CSV_URL': 'http://example.com/test.csv'}):
            response = self.client.get(reverse('ingest-csv-from-url'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json(), {'success': 'Data ingestion initiated successfully.'})
            mock_call_command.assert_called_once_with('data_ingestion')
    """
    @patch('accounts.views.call_command')
    def test_csv_url_not_set(self, mock_call_command):
        response = self.client.get(reverse('ingest-csv-from-url'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'CSV_URL environment variable is not set'})
        mock_call_command.assert_not_called()
    """


    @patch('accounts.views.call_command')
    def test_data_error(self, mock_call_command):
        mock_call_command.side_effect = DataError("Mocked data error")
        with patch.dict('os.environ', {'CSV_URL': 'http://example.com/test.csv'}):
            response = self.client.get(reverse('ingest-csv-from-url'))
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response.json(), {'error': 'Mocked data error'})
