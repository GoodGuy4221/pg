from django.urls import path

from .apps import TasksappConfig

from .views import CharacterCountConverterAPIView

app_name = TasksappConfig.name

urlpatterns = [
    path('strings/', CharacterCountConverterAPIView.as_view()),
]
