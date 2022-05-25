from django.urls import path

from .apps import MainappConfig
from .views import MainPage, AboutView

app_name = MainappConfig.name

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('', MainPage.as_view(), name='mainpage'),
]
