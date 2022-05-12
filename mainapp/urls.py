from django.urls import path

from .apps import MainappConfig
from .views import MainPage

app_name = MainappConfig.name

urlpatterns = [
    path('', MainPage.as_view(), name='mainpage'),
]
