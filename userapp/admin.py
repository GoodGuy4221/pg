from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea

from .forms import RegisterCustomUserForm, UpdateAdminCustomUserForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = RegisterCustomUserForm
    form = UpdateAdminCustomUserForm
    model = CustomUser

    search_fields = ('email', 'user_name', 'phone_number', 'first_name', 'last_name',)
    list_filter = ('email', 'user_name', 'phone_number', 'first_name', 'is_active', 'is_staff')
    ordering = ('-date_joined',)
    list_display = ('email', 'user_name', 'phone_number', 'first_name',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'phone_number', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('about_me', 'photo',)}),
    )
    formfield_overrides = {
        CustomUser.about_me: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'phone_number', 'first_name', 'last_name', 'photo', 'about_me',
                       'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )
    filter_horizontal = ()
