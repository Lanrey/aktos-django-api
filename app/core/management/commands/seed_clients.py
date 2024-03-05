from django.core.management.base import BaseCommand
from core.models import Client

class Command(BaseCommand):
    help = 'Seeds the database with a single client role'

    def handle(self, *args, **kwargs):
        client_name = "Sample Client"  # Change this to the desired client name
        # Check if the client already exists to avoid duplicates
        if not Client.objects.filter(name=client_name).exists():
            Client.objects.create(name=client_name)
            self.stdout.write(self.style.SUCCESS(f'Successfully added "{client_name}" to Client table.'))
        else:
            self.stdout.write(self.style.WARNING(f'Client "{client_name}" already exists in the database.'))
