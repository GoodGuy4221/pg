from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
import hashlib
import random
from uuid import uuid4

from utils.utils import user_photo_directory_path


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError(_('Адрес электронной почты должен быть установлен!'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self._create_user(email, password, **extra_fields)

    def make_random_password(
            self,
            length=12,
            allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789!@#~`$%^&*()_-+=?/\><.',
    ):
        """
        Generate a random password with the given length and given
        allowed_chars. The default value of allowed_chars does not have "I" or
        "O" or letters and digits that look similar -- just to avoid confusion.
        """
        return get_random_string(length, allowed_chars)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    uid = models.UUIDField(primary_key=True, default=uuid4)
    email = models.EmailField(_('email address'), unique=True, max_length=64, db_index=True,
                              help_text=_('Required. 64 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                              validators=[],
                              error_messages={
                                  'unique': _('A user with that email already exists.'),
                              }, )

    phone_number = models.CharField(_('phone number'), unique=True, null=True, blank=True, max_length=12, db_index=True,
                                    help_text=_('Required. Starts with + country code and 10 numbers.'),
                                    validators=[],
                                    error_messages={
                                        'unique': _('A user with that phone number already exists.'),
                                    }, )

    user_name = models.CharField(_('user name'), unique=True, null=True, blank=True, max_length=64, db_index=True,
                                 help_text=_('Required. 64 characters or fewer. Letters, digits and @/./+/-/_ only.'),
                                 validators=[username_validator],
                                 error_messages={
                                     'unique': _('A user with that name already exists.'),
                                 }, )

    first_name = models.CharField(_('first name'), max_length=64, blank=True)
    last_name = models.CharField(_('last name'), max_length=64, blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_('date update'), auto_now=True)

    # photo = models.ImageField(_('photo'), upload_to='photos-user/%Y/%m/%d/', blank=True)
    photo = models.ImageField(_('photo'), upload_to=user_photo_directory_path, blank=True)
    about_me = models.CharField(_('about me'), max_length=1024, blank=True)

    activation_key = models.CharField(max_length=128, blank=True)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS — список имен полей, которые будут запрашиваться при создании пользователя через команду
    # управления createsuperuser;
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('-date_joined',)
        verbose_name = _('custom user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def get_full_name(self):
        '''
        Возвращает first_name и last_name с пробелом между ними.
        '''
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        '''
        Возвращает сокращенное имя пользователя.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, recipient_list=None, **kwargs):
        '''
        Отправляет электронное письмо этому пользователю.
        '''
        send_mail(subject, message, from_email, recipient_list=[self.email], **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.is_active:
            self.is_active = False
            self.save()

    @property
    def is_activation_key_expired(self):
        print('dfgsgds', now() - self.date_joined)
        return now() - self.date_joined > timedelta(hours=settings.ACTIVATION_KEY_TTL)

    def set_activation_key(self):
        salt = hashlib.sha256(str(random.random()).encode('utf8')).hexdigest()[:12]
        self.activation_key = hashlib.sha1((self.email + salt).encode('utf8')).hexdigest()

    def send_confirm_email(self):
        """
        Формирование и отправка письма активации
        """
        verify_link = reverse('passport:verify',
                              kwargs={'email': self.email,
                                      'activation_key': self.activation_key})

        subject = f'Подтверждение учетной записи с email {self.email}'
        message = f'Для подтверждения учетной записи с email {self.email} на портале ' \
                  f'{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

        return send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list=[self.email],
                         fail_silently=False)


class Profile(models.Model):
    """
    Дополнительная информация о пользователе
    """
    MALE = 'M'
    FEMALE = 'W'
    OTHER = 'O'
    GENDER = (
        (MALE, 'мужской'),
        (FEMALE, 'женский'),
        (OTHER, 'предпочитаю не указывать'),
    )
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.PROTECT, related_name='profile')
    gender = models.CharField(_('пол'), max_length=1, choices=GENDER, default=OTHER)
    date_birth = models.DateField(_('дата рождения'), null=True, blank=True)
    deposit = models.PositiveIntegerField(_('Стоимость портфеля'), null=True, blank=True)
    annual_tax_amount = models.PositiveIntegerField(_('Общая сумма налога'), null=True, blank=True)
    total_amount_commissions = models.PositiveIntegerField(_('Общая сумма комиссий'), null=True, blank=True)
    number_transactions = models.PositiveSmallIntegerField(_('Общее количество сделок'), null=True, blank=True)
    transactions_closed_in_profit = models.PositiveSmallIntegerField(_('Прибыльных сделок'), null=True, blank=True)
    transactions_closed_in_loss = models.PositiveSmallIntegerField(_('Убыточных сделок'), null=True, blank=True)
    transactions_active = models.PositiveSmallIntegerField(_('Не закрытых сделок'), null=True, blank=True)
    tagline = models.CharField(_('теги'), max_length=128, blank=True)
