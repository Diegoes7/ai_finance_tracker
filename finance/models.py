from django.db import models


#! Create your models here.
class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    category = models.CharField(max_length=50)
    transaction_type = models.CharField(
        max_length=7, choices=TRANSACTION_TYPES)

    def __str__(self):
        return f"{self.transaction_type.title()}: {self.description} - {self.amount}"


class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    category = models.CharField(max_length=50)


class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    date = models.DateField()
    category = models.CharField(max_length=50)
