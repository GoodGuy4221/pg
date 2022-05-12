from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings


class MainPage(TemplateView):
    template_name = 'mainapp/index.html'
    extra_context = {
        'page_title': 'главная',
    }


class PageNotFound(TemplateView):
    template_name = 'mainapp/page-not-found.html'
    extra_context = {
        'page_title': 'страница не найдена',
    }
