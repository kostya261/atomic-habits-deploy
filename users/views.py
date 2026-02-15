from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserProfileSerializer


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "message": "Пользователь успешно зарегистрирован",
            "user": user.email
        }, status=status.HTTP_201_CREATED)


class UpdateTelegramChatIDView(generics.UpdateAPIView):
    """
    Эндпоинт для обновления Telegram Chat ID пользователя.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer  # Нужно создать

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        chat_id = request.data.get('telegram_chat_id')

        if chat_id:
            user.telegram_chat_id = chat_id
            user.save()
            return Response({
                'message': 'Telegram Chat ID обновлен',
                'telegram_chat_id': user.telegram_chat_id
            })

        return Response(
            {'error': 'telegram_chat_id обязателен'},
            status=status.HTTP_400_BAD_REQUEST
        )
