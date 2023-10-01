from rest_framework import generics
from users.serializers import UserSerializer
# Create your views here.


class UserCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт для регистрации пользователя
    """
    serializer_class = UserSerializer
