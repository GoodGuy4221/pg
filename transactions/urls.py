from django.urls import path
from django.views.generic import TemplateView

from .apps import TransactionsConfig
from .views import TransactionListView, TransactionNewView, TransactionDetailView, TransactionEditView

app_name = TransactionsConfig.name

urlpatterns = [
    path('', TransactionListView.as_view(), name='index'),
    path('new/', TransactionNewView.as_view(), name='new'),
    path('detail/<int:pk>/', TransactionDetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', TransactionEditView.as_view(), name='edit'),
]
