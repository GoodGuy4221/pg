from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Command(BaseCommand):
    help = _('Create Superuser and some test users')

    def handle(self, *args, **options):
        ADMIN_EXISTS = User.objects.filter(email='a@a.ru').exists()
        if not ADMIN_EXISTS:
            User.objects.create_superuser(email='a@a.ru',
                                          password='a')
            print(_('created user admin'))
        else:
            print(_('user admin already exists'))

        varick = User.objects.filter(email='varick@mail.ru').exists()
        if not varick:
            User.objects.create_user(email='varick@mail.ru',
                                     password='varick')
            print(_('created user varick'))
        else:
            print(_('user varick already exists'))

        bond = User.objects.filter(email='bond@bond.ru').exists()
        if not bond:
            User.objects.create_user(email='bond@bond.ru',
                                     password='bond')
            print(_('created user bond'))
        else:
            print(_('user bond already exists'))
