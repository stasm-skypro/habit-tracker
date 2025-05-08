from rest_framework import serializers

from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Представляет сериализатор для регистрации пользователя.
    Attributes:
        email (str): Электронная почта пользователя
        password (str): Пароль
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data.get("email"), password=validated_data["password"])
        return user


class UserListSerializer(serializers.ModelSerializer):
    """
    Представляет сериализатор для просмотра списка пользователей или просмотра одного пользователя.
    Определяет какие поля из модели будут сериализоваться (попадут в JSON-ответ или обработаются при запросе).
    Attributes:
        id (int): Идентификатор пользователя
        email (str): Электронная почта пользователя
        first_name (str): Имя пользователя
        last_name (str): Фамилия пользователя
    """

    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")
