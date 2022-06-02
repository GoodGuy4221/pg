from django.urls import path

from .apps import TelegramBotAppConfig
from .views import NotesAPIView

app_name = TelegramBotAppConfig.name

urlpatterns = [
    # path('notes/', NotesAPIView.as_view()),
]
