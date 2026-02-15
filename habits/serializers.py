from rest_framework import serializers
from .models import Habit
from .validators import HabitValidator
from .services import HabitService


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'place', 'time', 'action', 'is_pleasant',
            'linked_habit', 'periodicity', 'specific_days', 'reward',
            'execution_time', 'is_public', 'created_at', 'updated_at',
            'last_completed', 'streak'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_completed', 'streak']

    def validate(self, data):
        # Применяем валидацию
        data = HabitValidator.validate_habit_data(data)

        # Дополнительные проверки
        if data.get('execution_time', 0) > 120:
            raise serializers.ValidationError({
                'execution_time': 'Время выполнения не должно превышать 120 секунд'
            })

        return data

    def create(self, validated_data):
        # Создаем привычку
        habit = super().create(validated_data)

        # Отправляем уведомление в Telegram
        try:
            if habit.user.telegram_chat_id:
                HabitService.send_habit_created_notification(habit)
        except Exception as e:
            print(f"Ошибка отправки уведомления: {e}")

        return habit

    def to_representation(self, instance):
        """Кастомизация вывода"""
        representation = super().to_representation(instance)

        # Добавляем связанные данные
        if instance.linked_habit:
            representation['linked_habit'] = {
                'id': instance.linked_habit.id,
                'action': instance.linked_habit.action
            }

        # Форматируем время
        representation['time'] = instance.time.strftime('%H:%M')

        return representation


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор только для чтения публичных привычек"""
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id', 'user_email', 'place', 'time', 'action',
            'periodicity', 'execution_time', 'created_at'
        ]
        read_only_fields = fields
