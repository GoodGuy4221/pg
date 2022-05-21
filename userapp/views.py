from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import FormView
from django.views.generic import UpdateView, DeleteView, RedirectView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from pathlib import Path
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin

from .forms import (AuthenticationCustomUserForm, RegisterCustomUserForm, UpdateCustomUserForm,
                    PasswordChangeCustomUserForm,
                    UpdateProfileCustomUserForm)
from utils.mixins import SetPageTitleMixin, MessageAttributesAuthMixin


class Login(SetPageTitleMixin, LoginView):
    authentication_form = AuthenticationCustomUserForm
    success_url = reverse_lazy('mainapp:mainpage')
    template_name = Path('registration', 'login.html')
    page_title = 'авторизация'

    def get(self, *args, **kwargs):
        response = super(Login, self).get(*args, **kwargs)
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('mainapp:mainpage'))
        return response


class Logout(LoginRequiredMixin, LogoutView):
    pass


class Register(SetPageTitleMixin, MessageAttributesAuthMixin, SuccessMessageMixin, FormView):
    form_class = RegisterCustomUserForm
    template_name = Path('registration', 'signup.html')
    page_title = 'регистрация'
    success_url = reverse_lazy('mainapp:mainpage')

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.set_activation_key()
            user.save()
            if not user.send_confirm_email():
                messages.error(self.request, self.error_send_email_messages)
                return HttpResponseRedirect(reverse('mainapp:mainpage'))
            messages.success(self.request, self.success_send_email_messages)
            return HttpResponseRedirect(reverse('mainapp:mainpage'))
        messages.error(request, form.errors)
        return render(request, self.template_name, {'form': form})


class Verify(SetPageTitleMixin, MessageAttributesAuthMixin, SuccessMessageMixin, RedirectView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        email = request.resolver_match.kwargs.get('email')
        activation_key = request.resolver_match.kwargs.get('activation_key')
        try:
            user = get_user_model().objects.get(email=email)
            if user and user.activation_key == activation_key and not user.is_activation_key_expired:
                user.activation_key = ''
                user.is_active = True
                user.save()
                auth.login(self.request, user, backend='userapp.auth_backends.SettingsBackend')
            messages.success(self.request, self.success_activation)
            return HttpResponseRedirect(reverse('mainapp:mainpage'))
        except Exception as e:
            messages.error(self.request, self.error_activation)
            return HttpResponseRedirect(reverse('mainapp:mainpage'))


# class EditProfile(SetPageTitleMixin, SuccessMessageMixin, LoginRequiredMixin, UpdateView):
#     page_title = 'редактирование профиля'
#     model = get_user_model()
#     form_class = UpdateCustomUserForm
#     second_form_class = UpdateProfileCustomUserForm
#     template_name = Path('registration', 'edit.html')
#     success_message = _('данные успешно обновлены!')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form2'] = self.second_form_class(instance=self.request.user.profile)
#         return context
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(instance=request.user, data=request.POST, files=request.FILES)
#         form2 = self.second_form_class(instance=request.user.profile, data=request.POST)
#
#         if self.forms_valid(form, form2):
#             form.save()
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             return self.render_to_response(
#                 self.get_context_data(form=form, form2=form2))
#
#     def forms_valid(self, form, form2):
#         response = super().form_valid(form)
#         if form2.is_valid():
#             return response
#         return False
#
#     def get_success_url(self):
#         return self.request.META.get('HTTP_REFERER')
#
#     def get_success_message(self, cleaned_data):
#         return self.success_message
#
#     def get_form(self, form_class=None):
#         return self.form_class(instance=self.request.user)


class EditProfile(SetPageTitleMixin, SuccessMessageMixin, LoginRequiredMixin, FormView):
    page_title = 'редактирование профиля'
    form_class = UpdateCustomUserForm
    second_form_class = UpdateProfileCustomUserForm
    template_name = Path('registration', 'edit.html')
    success_message = _('данные успешно обновлены!')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form2'] = self.second_form_class(instance=self.request.user.profile)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(instance=request.user, data=request.POST, files=request.FILES)
        form2 = self.second_form_class(instance=request.user.profile, data=request.POST)

        if self.forms_valid(form, form2):
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2))

    def forms_valid(self, form, form2):
        response = super().form_valid(form)
        if form2.is_valid():
            return response
        return False

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def get_success_message(self, cleaned_data):
        return self.success_message

    def get_form(self, form_class=None):
        return self.form_class(instance=self.request.user)


class EditPassword(LoginRequiredMixin, PasswordChangeView):
    form_class = PasswordChangeCustomUserForm
    extra_context = {
        'page_title': 'изменить пароль',
    }
    template_name = Path('registration', 'change-password.html')
    success_url = reverse_lazy('mainapp:mainpage')


class DeleteAccount(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = Path('registration', 'delete-account.html')
    success_url = reverse_lazy('mainapp:mainpage')
    extra_context = {
        'page_title': 'удалить аккаунт',
        'warning_message': 'Удаление приведет к невозможности использовать данный аккаунт и немедленному '
                           'разлогированию!',
    }

    def post(self, request, *args, **kwargs):
        response = super(DeleteAccount, self).post(request, *args, **kwargs)
        self.object.delete()
        return HttpResponseRedirect(reverse('passport:logout'))
