"""
Test custom Djangp management commands;
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Errpr
from django.db.utils import DataError

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import (SimpleTestCase, TestCase)
from core.models import (Client, Consumers, ProcessedURL)

import os
from django.utils.timezone import now
from io import (StringIO, BytesIO)



@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """
    Test commands
    """

    def test_wait_for_db_ready(self, patched_check):
        """ Test waiting for database if database ready"""
        patched_check.return_value = True

        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError"""
        patched_check.side_effect = [Psycopg2Errpr] * 2 + \
                                    [OperationalError] * 3 + [True]

        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])


class SeedClientsCommandTest(TestCase):
    def test_command_output(self):
        self.assertFalse(Client.objects.exists())

        call_command('seed_clients')

        self.assertTrue(Client.objects.exists())
        self.assertEqual(Client.objects.count(), 1)
        client = Client.objects.first()
        self.assertEqual(client.name, "Sample Client")

        call_command('seed_clients')

        self.assertEqual(Client.objects.count(), 1)


class DataIngestionCommandTestCase(TestCase):
    def setUo(self):
        self.client = Client.objects.create(name="example client")

    @patch('core.management.commands.data_ingestion.requests.get')
    def test_ingestion_new_url(self, mock_get):
        mock_get.return_value.__enter__.return_value = MockResponse()

        Client.objects.create(name="Sample Client")

        test_url = "http://example.com/test.csv"
        os.environ['CSV_URL'] = test_url

        out = StringIO()

        call_command('data_ingestion', stdout=out)

        #self.assertTrue(ProcessedURL.objects.filter(url=test_url).exists())

        self.assertIn('Successfully ingested', out.getvalue())

        del os.environ['CSV_URL']


    def test_client_does_not_exist(self):
        # Use a client name that does not exist
        Client.objects.all().delete()  # Ensure no client exists
        test_url = "http://example.com/test.csv"
        os.environ['CSV_URL'] = test_url

        out = StringIO()
        call_command('data_ingestion', stdout=out)

        # Check for error message in command output
        self.assertIn('Specified client does not exist.', out.getvalue())

        del os.environ['CSV_URL']


class MockResponse:
    def __init__(self, *args, **kwargs):
        # Mock CSV content
        csv_content = (b'client reference no,balance,status,consumer name,consumer address,ssn\n'
                       b'ffeb5d88-e5af-45f0-9637-16ea469c58c0,59640.99,INACTIVE,Jessica Williams, 0233 Edwards Glens lisonhaven HI 91491,018-79-4253')
        self._content = BytesIO(csv_content)

    def raise_for_status(self):
        pass

    @property
    def raw(self):
        self._content.seek(0)  # Reset pointer to the start
        return self._content


"""
class MockResponse:
    # Mock the response from requests.get
    def __init__(self, *args, **kwargs):
        self.status_code = 200

    def raise_for_status(self):
        pass

    def iter_content(self, chunk_size=1, decode_unicode=False):
        # Return content for the CSV. You'll need to adjust this based on your actual CSV content.
        content = (b'client reference no, balance, status, consumer name,consumer address, ssn\nffeb5d88-e5af-45f0-9637-16ea469c58c0,'
                   b'59638.99,INACTIVE,Jessica Williams, 0233 Edwards Glens lisonhaven, HI 91491,018-79-4253'
                   b'\nffeb5d88-e5af-45f0-9637-16ea469c58c1,'
                   b'59648.99,INACTIVE,Sola Williams,  Edwards Glens lisonhaven, HI 91491,019-79-4253')
        yield content


    @property
    def raw(self):
        return self
"""

