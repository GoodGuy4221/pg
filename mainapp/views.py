from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from pathlib import Path


class MainPage(TemplateView):
    template_name = Path('mainapp', 'index.html')
    extra_context = {
        'page_title': 'главная',
    }


class AboutView(TemplateView):
    template_name = Path('mainapp', 'about.html')
    extra_context = {
        'page_title': 'об этом',
    }


class PageNotFound(TemplateView):
    template_name = Path('mainapp', 'page-not-found.html')
    extra_context = {
        'page_title': 'страница не найдена',
    }
