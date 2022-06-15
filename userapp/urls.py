from django.urls import path
from .apps import UserappConfig
from django.views.generic import TemplateView

from .views import Login, Logout, Register, EditProfile, EditPassword, DeleteAccount, Verify

app_name = UserappConfig.name

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('signup/', Register.as_view(), name='signup'),
    path('edit/', EditProfile.as_view(), name='edit'),
    path('edit/pass/<uuid:pk>/', EditPassword.as_view(), name='editpass'),
    path('edit/delete/<uuid:pk>/', DeleteAccount.as_view(), name='delete'),

    path('error/', TemplateView.as_view(template_name='registration/error.html'), name='error'),

    path('verify/<str:email>/<str:activation_key>/', Verify.as_view(), name='verify'),
]
