from django.conf import settings
import pandas as pd
import requests
import os

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from core.models import (Client, Consumers, ProcessedURL)


class Command(BaseCommand):
    help = 'Ingests data from a streamed CSV URL into the database'

    def handle(self, *args, **options):
        csv_url = os.environ.get('CSV_URL')
        if not csv_url:
            self.stdout.write(self.style.ERROR('CSV URL environment variable is not set'))
            return

        # Check if the URL has already been processed
        if ProcessedURL.objects.filter(url=csv_url).exists():
            self.stdout.write(self.style.WARNING('This CSV URL has already been processed.'))
            return

        # Attempt to retrieve a specific Client Instance
        try:
            client = Client.objects.get(name="Sample Client")
        except Client.DoesNotExist:
            self.stdout.write(self.style.ERROR('Specified client does not exist.'))
            return

        with requests.get(csv_url, stream=True) as r:
            r.raise_for_status()
            for chunk in pd.read_csv(r.raw, chunksize=1000, delimiter=','):

                for index, row in chunk.iterrows():

                    try:
                        Consumers.objects.create(
                            client=client,
                            client_reference_no=row['client reference no'],
                            balance=row['balance'],
                            status=row['status'],
                            consumer_name=row['consumer name'],
                            consumer_address=row['consumer address'].replace(',', ''),
                            ssn=row['ssn']
                        )
                        self.stdout.write(self.style.SUCCESS(f'Successfully ingested rows'))
                    except IntegrityError as e:
                        self.stdout.write(
                            self.style.ERROR(f'Error ingesting data for {row}: {str(e)}'))

        ProcessedURL.objects.create(url=csv_url)
        self.stdout.write(self.style.SUCCESS('CSV URL has been marked as processed'))



