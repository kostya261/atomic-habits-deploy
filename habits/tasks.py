from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Habit
from .services import HabitService


@shared_task
def send_telegram_reminders():
    """
    Отправка напоминаний в Telegram.
    Простой вариант без сложных настроек.
    """
    now = timezone.now()
    current_time = now.time()

    # Привычки, которые нужно выполнить в ближайшие 10 минут
    reminder_time = (now + timedelta(minutes=10)).time()

    # Получаем привычки
    habits = Habit.objects.filter(
        time__gte=current_time,
        time__lte=reminder_time,
        user__telegram_chat_id__isnull=False
    ).select_related('user')

    sent_count = 0
    for habit in habits:
        if habit.should_be_done_today() and habit.user.telegram_chat_id:
            message = (
                f"🔔 <b>Напоминание о привычке!</b>\n\n"
                f"🏃‍♂️ <b>Привычка:</b> {habit.action}\n"
                f"⏰ <b>Время:</b> {habit.time.strftime('%H:%M')}\n"
                f"📍 <b>Место:</b> {habit.place}\n"
                f"⏱️ <b>На выполнение:</b> {habit.execution_time} сек\n"
                f"📅 <b>Периодичность:</b> {habit.get_periodicity_display()}"
            )

            result = HabitService.send_telegram_message(
                habit.user.telegram_chat_id,
                message
            )

            if result and result.get('ok'):
                sent_count += 1
                print(f"✅ Отправлено напоминание {habit.user.email}")
            else:
                print(f"❌ Ошибка отправки {habit.user.email}: {result}")

    return f"Отправлено напоминаний: {sent_count}"
