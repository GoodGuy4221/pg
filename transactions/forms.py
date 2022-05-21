from django.contrib.auth import get_user_model
from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import HiddenInput

from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = (
            'user', 'name_asset', 'ticker', 'purchase_price',
            'sale_price', 'quantity', 'type_transaction',
            'tool_type', 'tax', 'broker_exchange_commission_percentage',
            'description'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''
            if field_name == 'user':
                field.widget = HiddenInput()
                continue
            field.widget.attrs['class'] = 'form-control'
