import requests
from django.utils import timezone
from datetime import timedelta

from config import settings
from .models import Habit

import os


TEST_MODE = os.getenv('TEST_MODE', 'False') == 'True'


class HabitService:
    """
    Сервис для бизнес-логики работы с привычками.
    """

    @staticmethod
    def get_todays_habits(user):
        """
        Получить привычки пользователя на сегодня.
        """
        today = timezone.now().date()
        today_weekday = today.strftime('%a').lower()[:3]  # 'mon', 'tue', etc.

        # Ежедневные привычки
        daily_habits = Habit.objects.filter(
            user=user,
            periodicity='daily'
        )

        # Еженедельные привычки на сегодня
        weekly_habits = Habit.objects.filter(
            user=user,
            periodicity='weekly',
            specific_days__contains=[today_weekday]
        )

        # Через день - проверяем последнее выполнение
        every_other_day_habits = Habit.objects.filter(
            user=user,
            periodicity='every_other_day'
        )

        result = list(daily_habits) + list(weekly_habits)

        # Фильтруем привычки "через день"
        for habit in every_other_day_habits:
            if not habit.last_completed:
                result.append(habit)
            else:
                days_passed = (today - habit.last_completed.date()).days
                if days_passed >= 2:
                    result.append(habit)

        # Сортируем по времени
        return sorted(result, key=lambda x: x.time)

    @staticmethod
    def check_and_send_reminders():
        """
        Проверить, какие привычки нужно выполнить сейчас,
        и отправить напоминания.
        """
        now = timezone.now()
        current_time = now.time()

        # Привычки, которые нужно выполнить в ближайшие 10 минут
        reminder_time = (now + timedelta(minutes=10)).time()

        habits_to_remind = Habit.objects.filter(
            time__gte=current_time,
            time__lte=reminder_time
        ).select_related('user')

        reminders = []
        for habit in habits_to_remind:
            if habit.should_be_done_today():
                reminders.append({
                    'habit': habit,
                    'user': habit.user,
                    'time': habit.time,
                    'message': f"Напоминание: {habit.action} в {habit.time} в {habit.place}"
                })

        return reminders

    @staticmethod
    def complete_habit(habit, user):
        """
        Отметить привычку как выполненную.
        """
        if habit.user != user:
            raise PermissionError("Вы не можете отмечать чужие привычки")

        habit.last_completed = timezone.now()
        habit.streak += 1
        habit.save()

        # Возвращаем информацию о выполненной привычке
        return {
            'habit': habit.action,
            'streak': habit.streak,
            'completed_at': habit.last_completed,
            'reward': habit.reward if habit.reward else None,
            'linked_habit': habit.linked_habit.action if habit.linked_habit else None
        }

    @staticmethod
    def send_telegram_message(chat_id, message):
        """
        Отправка сообщения в Telegram.
        Простой способ без webhook.
        """
        if not settings.TELEGRAM_BOT_TOKEN:
            print(f"Telegram: {message} (без отправки, нет токена)")
            return None

        url = f"{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        params = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            return response.json()
        except Exception as e:
            print(f"Ошибка отправки в Telegram: {e}")
            return None

    @staticmethod
    def send_habit_created_notification(habit):
        """
        Отправить уведомление о создании новой привычки.
        """
        if not habit.user.telegram_chat_id:
            print(f"⚠️ У пользователя {habit.user.email} нет telegram_chat_id")
            return None

        message = (
            f"🎯 <b>Новая привычка создана!</b>\n\n"
            f"🏃‍♂️ <b>Действие:</b> {habit.action}\n"
            f"⏰ <b>Время:</b> {habit.time.strftime('%H:%M')}\n"
            f"📍 <b>Место:</b> {habit.place}\n"
            f"📅 <b>Периодичность:</b> {habit.get_periodicity_display()}\n"
            f"⏱️ <b>Время на выполнение:</b> {habit.execution_time} сек\n\n"
            f"<i>Напоминание придет за 10 минут до выполнения</i>"
        )

        return HabitService.send_telegram_message(habit.user.telegram_chat_id, message)
