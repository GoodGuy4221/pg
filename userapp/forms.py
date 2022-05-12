from django.contrib.auth import get_user_model
from django import forms
from django.forms.widgets import HiddenInput
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, Profile

User = get_user_model()


class AuthenticationCustomUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_field = forms.CharField(max_length=64)
        label_ui = _('Уникальный идентификатор (эл.почта, номер телефона, логин)')
        self.fields['username'].label = label_ui
        self.username_field.verbose_name = label_ui
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class RegisterCustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class UpdateCustomUserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'email', 'phone_number', 'user_name', 'first_name', 'last_name',
            'photo', 'about_me',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = HiddenInput()


class UpdateProfileCustomUserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'gender', 'date_birth',
        )

    def __init__(self, *args, **kwargs):
        super(UpdateProfileCustomUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class PasswordChangeCustomUserForm(PasswordChangeForm):
    class Meta:
        model = CustomUser

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class UpdateAdminCustomUserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            'email', 'phone_number', 'user_name', 'first_name', 'last_name',
            'photo', 'about_me',
        )
