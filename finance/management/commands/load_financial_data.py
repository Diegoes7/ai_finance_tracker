import csv
from django.core.management.base import BaseCommand
from finance.models import Transaction

class Command(BaseCommand):
    help = 'Load financial transactions from CSV'

    def handle(self, *args, **kwargs):
        with open('finance/data/finance_data.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Transaction.objects.create(
                    date=row['date'],
                    amount=row['amount'],
                    category=row['category'],
                    description=row['description']
                )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully.'))
