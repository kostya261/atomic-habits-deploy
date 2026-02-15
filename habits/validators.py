from rest_framework import serializers


class HabitValidator:
    """Комплексный валидатор для привычек"""

    @staticmethod
    def validate_execution_time(value):
        if value > 120:
            raise serializers.ValidationError(
                "Время выполнения не должно превышать 120 секунд"
            )
        return value

    @staticmethod
    def validate_linked_habit(value):
        if value and not value.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной"
            )
        return value

    @staticmethod
    def validate_periodicity(value):
        valid_periods = ['daily', 'every_other_day', 'weekly', 'monthly']
        if value not in valid_periods:
            raise serializers.ValidationError(
                f"Периодичность должна быть одним из: {', '.join(valid_periods)}"
            )
        return value

    @staticmethod
    def validate_habit_data(data):
        """Валидация взаимосвязей полей"""
        is_pleasant = data.get('is_pleasant', False)
        linked_habit = data.get('linked_habit')
        reward = data.get('reward', '')

        # Приятная привычка не имеет вознаграждения или связанной привычки
        if is_pleasant and (reward or linked_habit):
            raise serializers.ValidationError({
                'non_field_errors': [
                    "Приятная привычка не может иметь вознаграждения "
                    "или связанной привычки"
                ]
            })

        # Нельзя одновременно указать и связанную привычку, и вознаграждение
        if linked_habit and reward:
            raise serializers.ValidationError({
                'non_field_errors': [
                    "Нельзя указывать одновременно связанную привычку "
                    "и вознаграждение. Выберите что-то одно."
                ]
            })

        # Периодичность не реже 1 раза в 7 дней
        periodicity = data.get('periodicity')
        if periodicity == 'weekly' and not data.get('specific_days'):
            raise serializers.ValidationError({
                'specific_days': "Для еженедельной привычки укажите дни выполнения"
            })

        return data

    @staticmethod
    def validate_not_less_than_once_per_week(data):
        """Нельзя выполнять привычку реже, чем 1 раз в 7 дней"""
        periodicity = data.get('periodicity')

        if periodicity not in ['daily', 'every_other_day', 'weekly']:
            # Если monthly или другая - это реже чем раз в неделю
            raise serializers.ValidationError({
                'periodicity': 'Нельзя выполнять привычку реже, чем 1 раз в 7 дней'
            })

        if periodicity == 'weekly' and not data.get('specific_days'):
            raise serializers.ValidationError({
                'specific_days': 'Для еженедельной привычки укажите дни выполнения'
            })

        return data
