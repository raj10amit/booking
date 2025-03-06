import csv
from django.core.management.base import BaseCommand
from inventory.models import Member, Inventory
from django.utils.dateparse import parse_datetime

class Command(BaseCommand):
    help = 'Import CSV data into the database'

    def handle(self, *args, **kwargs):
        # Load members.csv
        with open('inventory/data/members.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Member.objects.create(
                    name=row['name'].strip(),
                    surname=row['surname'].strip(),
                    booking_count=int(row['booking_count']),
                    date_joined=parse_datetime(row['date_joined'])
                )

        # Load inventory.csv
        with open('inventory/data/inventory.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                Inventory.objects.create(
                    title=row['title'].strip(),
                    description=row['description'].strip(),
                    remaining_count=int(row['remaining_count']),
                    expiration_date=row['expiration_date']
                )

        self.stdout.write(self.style.SUCCESS('CSV data imported successfully!'))
