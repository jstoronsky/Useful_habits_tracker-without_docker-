from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователя. Переопределён метод create, чтобы была возможность регистрироваться через API
    """

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create(
            email=validated_data['email'],
            tg_username=validated_data['tg_username'],
            chat_id=validated_data['chat_id'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'tg_username', 'chat_id')
