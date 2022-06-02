from django.forms import ModelForm, TextInput
from django.utils.translation import gettext_lazy as _

from .models import City


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = (
            'name',
        )
        widgets = {'name': TextInput(attrs={
            'class': 'form-control',
            'name': 'city',
            'id': 'city',
            'placeholder': _('Введите город'),
        })}
