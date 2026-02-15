from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Habit(models.Model):
    PERIOD_CHOICES = [
        ('daily', 'Ежедневно'),
        ('every_other_day', 'Через день'),
        ('weekly', 'Еженедельно'),
        ('monthly', 'Ежемесячно'),
    ]

    DAYS_OF_WEEK = [
        ('mon', 'Понедельник'),
        ('tue', 'Вторник'),
        ('wed', 'Среда'),
        ('thu', 'Четверг'),
        ('fri', 'Пятница'),
        ('sat', 'Суббота'),
        ('sun', 'Воскресенье'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Пользователь'
    )

    place = models.CharField(
        max_length=255,
        verbose_name='Место выполнения',
        help_text='Где будет выполняться привычка'
    )

    time = models.TimeField(
        verbose_name='Время выполнения',
        help_text='Во сколько выполнять привычку'
    )

    action = models.CharField(
        max_length=500,
        verbose_name='Действие',
        help_text='Конкретное действие, которое нужно выполнить'
    )

    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Приятная привычка',
        help_text='Является ли привычка приятной (вознаграждением)'
    )

    linked_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='linked_to',
        verbose_name='Связанная привычка',
        help_text='Приятная привычка, связанная с полезной'
    )

    periodicity = models.CharField(
        max_length=20,
        choices=PERIOD_CHOICES,
        default='daily',
        verbose_name='Периодичность'
    )

    specific_days = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Конкретные дни недели',
        help_text='Для еженедельных привычек - дни выполнения'
    )

    reward = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Вознаграждение',
        help_text='Чем себя вознаградить после выполнения'
    )

    execution_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(120)],
        verbose_name='Время на выполнение (секунды)',
        help_text='Не более 120 секунд'
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичная привычка',
        help_text='Видна ли привычка другим пользователям'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Для отслеживания выполнения
    last_completed = models.DateTimeField(null=True, blank=True)
    streak = models.PositiveIntegerField(default=0, verbose_name='Серия выполнения')

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['time']
        indexes = [
            models.Index(fields=['user', 'time']),
            models.Index(fields=['is_public']),
            models.Index(fields=['last_completed']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(execution_time__lte=120),
                name='execution_time_max_120'
            ),
        ]

    def __str__(self):
        return f"{self.user.email}: {self.action} в {self.time}"

    def clean(self):
        """Дополнительная валидация на уровне модели"""
        from django.core.exceptions import ValidationError

        if self.is_pleasant and (self.reward or self.linked_habit):
            raise ValidationError(
                "Приятная привычка не может иметь вознаграждения или связанной привычки"
            )

        if self.linked_habit and self.reward:
            raise ValidationError(
                "Нельзя указывать одновременно связанную привычку и вознаграждение"
            )

        if self.linked_habit and not self.linked_habit.is_pleasant:
            raise ValidationError(
                "Связанная привычка должна быть приятной"
            )

        # Проверка периодичности
        if self.periodicity == 'weekly' and not self.specific_days:
            raise ValidationError(
                "Для еженедельной привычки укажите дни выполнения"
            )

    def should_be_done_today(self):
        """Нужно ли выполнять привычку сегодня"""

        if not self.last_completed:
            return True

        today = timezone.now().date()
        last_date = self.last_completed.date()

        if self.periodicity == 'daily':
            return today > last_date
        elif self.periodicity == 'every_other_day':
            days_passed = (today - last_date).days
            return days_passed >= 2
        elif self.periodicity == 'weekly':
            # Проверяем, сегодня ли нужный день недели
            today_weekday = today.strftime('%a').lower()[:3]
            return today_weekday in self.specific_days and today > last_date

        return False
