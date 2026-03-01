from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Habit
from .serializers import HabitSerializer, PublicHabitSerializer
from .permissions import IsOwner
from .pagination import HabitPagination
from .filters import HabitFilter


class HabitViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с привычками.
    """
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = HabitFilter
    ordering_fields = ['time', 'created_at', 'last_completed']
    search_fields = ['action', 'place']

    @action(detail=True, methods=['post'])
    def test_telegram(self, request, pk=None):
        """Тестовая отправка сообщения в Telegram"""
        habit = self.get_object()

        if habit.user != request.user:
            return Response(
                {'error': 'Нет доступа'},
                status=status.HTTP_403_FORBIDDEN
            )

        from .services import HabitService

        message = f"🔔 Тестовое сообщение для привычки: {habit.action}"
        result = HabitService.send_telegram_message(
            habit.user.telegram_chat_id,
            message
        )

        return Response({
            'status': 'Сообщение отправлено' if result else 'Ошибка отправки',
            'result': result
        })

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        elif self.action == 'public':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'today':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Возвращает queryset в зависимости от пользователя и действия.
        """
        user = self.request.user

        if self.action == 'public':
            # Публичные привычки всех пользователей
            return Habit.objects.filter(is_public=True).select_related('user')

        if user.is_authenticated:
            # Привычки текущего пользователя
            return Habit.objects.filter(user=user).select_related('linked_habit')

        return Habit.objects.none()

    def perform_create(self, serializer):
        """Автоматически назначаем пользователя при создании"""
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Отметить привычку как выполненную"""
        habit = self.get_object()

        if habit.user != request.user:
            return Response(
                {'error': 'Вы не можете отмечать чужие привычки'},
                status=status.HTTP_403_FORBIDDEN
            )

        habit.last_completed = timezone.now()
        habit.streak += 1
        habit.save()

        return Response({
            'status': 'Привычка выполнена',
            'streak': habit.streak,
            'last_completed': habit.last_completed
        })

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Получить привычки на сегодня"""
        habits = self.get_queryset().filter(
            periodicity='daily'
        ) | self.get_queryset().filter(
            periodicity='weekly',
            specific_days__contains=[timezone.now().strftime('%a').lower()[:3]]
        )

        page = self.paginate_queryset(habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def public(self, request):
        """Список публичных привычек (доступен всем)"""
        habits = Habit.objects.filter(is_public=True).select_related('user')

        page = self.paginate_queryset(habits)
        if page is not None:
            serializer = PublicHabitSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PublicHabitSerializer(habits, many=True)
        return Response(serializer.data)


class PublicHabitViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Только для чтения публичных привычек.
    """
    queryset = Habit.objects.filter(is_public=True).select_related('user')
    serializer_class = PublicHabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.AllowAny]
