from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """
    Админка для модели Habit.
    """
    # Поля в списке
    list_display = ('user', 'action', 'place', 'time', 'is_pleasant', 'is_public', 'periodicity', 'streak')

    # Поля для поиска
    search_fields = ('action', 'place', 'user__email')

    # Фильтры
    list_filter = ('is_pleasant', 'is_public', 'periodicity', 'created_at')

    # Поля только для чтения
    readonly_fields = ('created_at', 'updated_at', 'last_completed', 'streak')

    # Группировка полей в форме
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'action', 'place', 'time')
        }),
        ('Детали привычки', {
            'fields': ('is_pleasant', 'linked_habit', 'periodicity', 'specific_days')
        }),
        ('Вознаграждение и выполнение', {
            'fields': ('reward', 'execution_time', 'is_public')
        }),
        ('Статистика', {
            'fields': ('last_completed', 'streak', 'created_at', 'updated_at'),
            'classes': ('collapse',)  # Сворачиваемая секция
        }),
    )

    # Автозаполнение поля "user" при создании привычки
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['user'].initial = request.user
        return form
