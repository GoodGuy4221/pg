from django.urls import path

from .apps import WeatherAppConfig

from . import views

app_name = WeatherAppConfig.name

urlpatterns = [
    path('', views.main, name='main'),
]
