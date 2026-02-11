from django.urls import path
from .views import UserRegistrationView, UpdateTelegramChatIDView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('telegram/', UpdateTelegramChatIDView.as_view(), name='update_telegram'),
]
