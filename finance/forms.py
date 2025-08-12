# finance/forms.py

from django import forms
from .utils.csv_manager import FORMAT


CATEGORY_CHOICES = [("Income", "Income"), ("Expense", "Expense")]


class TransactionForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=[FORMAT],
        required=False
    )
    amount = forms.FloatField(min_value=0.01)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter a description',
            'rows': 7,
            'cols': 27,
            'style': 'width: 100%; max-width: 300px;'
        })
    )
