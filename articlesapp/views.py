from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from pathlib import Path

from .models import Articles
from utils.mixins import PaginateMixin
from .forms import WriteArticleForm


class ArticlesView(PaginateMixin, ListView):
    model = Articles
    template_name = Path('articlesapp', 'index.html')
    extra_context = {
        'page_title': 'статьи',
    }

    def get_queryset(self):
        return self.model.objects.filter(is_active=True).select_related('topic')


class DetailArticleView(DetailView):
    model = Articles
    template_name = Path('articlesapp', 'detail_article.html')

    def get_object(self, queryset=None):
        return self.model.objects.filter(pk=self.kwargs['pk'], is_active=True).select_related('topic').first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f'Articles «{self.object.title}»'
        return context


class WriteArticleView(LoginRequiredMixin, FormView):
    template_name = Path('articlesapp', 'write_article.html')
    form_class = WriteArticleForm
    extra_context = {
        'page_title': 'написать статью',
    }

    def form_valid(self, form):
        item = form.save()
        self.pk = item.pk
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('articles:detail_article', kwargs={'pk': self.pk})

    def get_initial(self):
        init = super().get_initial()
        init['user'] = self.request.user
        return init
