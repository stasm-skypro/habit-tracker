from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from user.serializer import RegisterSerializer


class RegisterAPIView(CreateAPIView):
    """
    Регистрация нового пользователя.

    Параметры запроса:
    - email (str): Email пользователя
    - password (str): Пароль не менее 8 символов
    """

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает запрос на регистрацию нового пользователя.
        :param request: Объект запроса, содержащий данные пользователя.
                    Тип: rest_framework.request.Request
        :return: Response с результатом регистрации.
        """
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": f"Регистрация пользователя {user.email} прошла успешно."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
