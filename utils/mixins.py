from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _


class SuperUserOnlyMixin:
    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SetPageTitleMixin:
    page_title = ''

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['page_title'] = self.page_title
        return context


class MessageAttributesAuthMixin:
    error_send_email_messages = _(f'произошла ошибка, email со ссылкой активации не был отправлен!')
    success_send_email_messages = _(f'email со ссылкой активации успешно отправлен!')
    error_activation = _(f'ключ активации не подошел или такого пользователя нет!')
    success_activation = _(f'активация прошла успешно!')


class AccessOnlyOwnerObjectMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if self.request.user.pk == self.object.user.pk:
            return response
        return self.handle_no_permission()


class IsActiveFalseMixin:
    def delete(self, using=None, keep_parents=False):
        if self.is_active:
            self.is_active = False
            self.save()


class PaginateMixin:
    paginate_by = 12
