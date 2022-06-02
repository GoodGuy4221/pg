"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from mainapp.views import PageNotFound
from telegram_bot_app.views import NotesAPIView

router = DefaultRouter()
router.register('telegram-bot/notes', NotesAPIView, basename='notes')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),

    path('api/tasks/', include('tasksapp.urls')),
    # path('api/telegram-bot/', include('telegram_bot_app.urls')),

    path('api-token-auth/', views.obtain_auth_token),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('admin/', admin.site.urls),

    path('passport/', include('userapp.urls', namespace='passport')),

    path('', include('mainapp.urls', namespace='mainapp')),

    path('articles/', include('articlesapp.urls', namespace='articles')),

    path('social/', include('social_django.urls', namespace='social')),

    # SSR APP
    path('transactions/', include('transactions.urls', namespace='transactions')),
    path('weather/', include('weather_app.urls', namespace='weather')),
]

handler404 = PageNotFound.as_view()
# handler403 = ''

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
