import django_filters
from .models import Habit


class HabitFilter(django_filters.FilterSet):
    """
    Фильтры для привычек.
    """
    place = django_filters.CharFilter(lookup_expr='icontains')
    action = django_filters.CharFilter(lookup_expr='icontains')
    is_pleasant = django_filters.BooleanFilter()
    is_public = django_filters.BooleanFilter()
    periodicity = django_filters.ChoiceFilter(choices=Habit.PERIOD_CHOICES)

    # Фильтр по времени (например, привычки до 12:00)
    time_before = django_filters.TimeFilter(field_name='time', lookup_expr='lte')
    time_after = django_filters.TimeFilter(field_name='time', lookup_expr='gte')

    # Фильтр по дате создания
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')

    class Meta:
        model = Habit
        fields = [
            'place',
            'action',
            'is_pleasant',
            'is_public',
            'periodicity',
            'time',
        ]

    @property
    def qs(self):
        """
        Переопределяем queryset, чтобы учитывать пользователя.
        """
        parent = super().qs

        if hasattr(self, 'request') and self.request and self.request.user.is_authenticated:
            return parent.filter(user=self.request.user)

        return parent.filter(is_public=True)
