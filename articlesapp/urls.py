from django.urls import path
from .apps import ArticlesappConfig

from .views import ArticlesView, DetailArticleView, WriteArticleView

app_name = ArticlesappConfig.name

urlpatterns = [
    path('article/<slug:pk>/', DetailArticleView.as_view(), name='detail_article'),
    path('writearticle/', WriteArticleView.as_view(), name='writearticle'),
    path('', ArticlesView.as_view(), name='index'),
]
