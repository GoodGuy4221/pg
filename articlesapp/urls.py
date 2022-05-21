from django.urls import path
from .apps import ArticlesappConfig

from .views import ArticlesView

app_name = ArticlesappConfig.name

urlpatterns = [
    path('', ArticlesView.as_view(), name='index'),
]
