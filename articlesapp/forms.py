from django import forms
from django.forms.widgets import HiddenInput
from django.utils.translation import gettext_lazy as _

from .models import Articles


class WriteArticleForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = (
            'user', 'topic', 'title', 'body',
        )
        labels = {
            'class': 'form-label',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''
            if field_name == 'user':
                field.widget = HiddenInput()
            field.widget.attrs['class'] = 'form-control'
