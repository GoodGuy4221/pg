from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='_')
def m(string):
    pass
