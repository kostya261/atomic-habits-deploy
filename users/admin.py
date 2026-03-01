from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Кастомная админка для модели User.
    Наследуемся от стандартного UserAdmin.
    """
    # Поля которые отображаются в списке
    list_display = ('email', 'username', 'telegram_chat_id', 'is_staff', 'is_active', 'date_joined')

    # Поля для поиска
    search_fields = ('email', 'username', 'telegram_chat_id')

    # Фильтры
    list_filter = ('is_staff', 'is_active', 'date_joined')

    # Порядок полей в форме редактирования
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Telegram', {'fields': ('telegram_chat_id', 'timezone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Поля при создании пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'telegram_chat_id'),
        }),
    )

    # Сортировка
    ordering = ('email',)
