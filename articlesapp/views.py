from django.shortcuts import render
from django.views.generic import ListView
from pathlib import Path

from .models import Articles
from utils.mixins import PaginateMixin


class ArticlesView(PaginateMixin, ListView):
    model = Articles

    template_name = Path('articlesapp', 'index.html')

    def get_queryset(self):
        return self.model.objects.filter(is_active=True).select_related('topic')
