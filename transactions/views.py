from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from pathlib import Path
from django.utils.translation import gettext_lazy as _

from .forms import TransactionForm
from .models import Transaction
from .name_columns import name_columns
from utils.mixins import AccessOnlyOwnerObjectMixin


class TransactionListView(LoginRequiredMixin, ListView):
    model = Transaction
    template_name = Path('transactions', 'index.html')
    extra_context = {
        'page_title': _('ваши сделки'),
    }

    def get_queryset(self):
        result = self.model.objects.filter(user=self.request.user).only('name_asset', 'ticker')
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name_columns'] = name_columns
        return context


class TransactionNewView(LoginRequiredMixin, CreateView):
    form_class = TransactionForm
    template_name = Path('transactions', 'new_transaction.html')
    success_url = reverse_lazy('transactions:index')
    extra_context = {
        'page_title': _('новая сделка'),
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        match self.request.method:
            case 'GET':
                context['form'].initial['user'] = self.request.user
            case 'POST':
                pass
        return context


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = Path('transactions', 'detail_transaction.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _(f'детальная информация по сделке «{self.object.name_asset}»')
        return context


class TransactionEditView(LoginRequiredMixin, AccessOnlyOwnerObjectMixin, UpdateView):
    model = Transaction
    template_name = Path('transactions', 'edit_transaction.html')
    form_class = TransactionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _(f'редактирование Вашей сделки «{self.object.name_asset}»')
        return context

    def get_success_url(self):
        return reverse('transactions:detail', args=(self.object.pk,))
