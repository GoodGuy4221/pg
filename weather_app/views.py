from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.conf import settings

import requests

from .models import City
from .forms import CityForm


def main(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    form = CityForm()

    cities = City.objects.all()

    cities_list = []

    for item in cities:
        url_request = f'http://api.openweathermap.org/data/2.5/weather?q={item}&units=metric&lang=ru&appid={settings.OPEN_WEATHER_KEY}'
        response = requests.get(url=url_request).json()
        city_info = {
            'city': response['name'],
            'temp': response['main']['temp'],
            'icon': response['weather'][0]['icon'],
        }
        cities_list.append(city_info)

    context = {
        'page_title': _('Погода'),
        'menu_items': (
            _('главная'), _('информация'), _('подписаться на рассылку'),
        ),
        'placeholder_input_city': _('введите город'),
        'label_text': _('город'),
        'title': _('погода в вашем городе'),
        'learn': _('узнать'),
        'weather_in_dimitrovgrad': _('погода в Димитровграде'),
        'cities_list': cities_list,
        'form': form,
    }
    return render(request, 'weather_app/index.html', context=context)
