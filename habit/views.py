from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Habit
from .paginators import HabitPagination
from .serializers import HabitSerializer

# Так как нужно реализовать полный набор CRUD-действий (создание, список, редактирование, удаление, просмотр) —
# лучше использовать ModelViewSet.
# Он:
# уже реализует все основные методы (list, create, retrieve, update, partial_update, destroy);
# легко настраивается через queryset, serializer_class и permission_classes;
# поддерживает пагинацию, фильтрацию и сортировку «из коробки»;
# позволяет использовать router для удобной маршрутизации.


class HabitViewSet(ModelViewSet):
    """
    CRUD для привычек текущего пользователя.

    Эндпоинты:
    GET /habits/ — список привычек текущего пользователя (с пагинацией),
    POST /habits/ — создание,
    GET /habits/{id}/ — просмотр,
    PUT /habits/{id}/ — полное обновление,
    PATCH /habits/{id}/ — частичное обновление,
    DELETE /habits/{id}/ — удаление.
    """

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitPagination

    def get_queryset(self):
        """
        Возвращает queryset привычек, принадлежащих текущему пользователю.
        """
        return Habit.objects.filter(user=self.request.user).order_by("created_at")

    def perform_create(self, serializer):
        """
        Автоматически устанавливает пользователя при создании привычки.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def public(self, request):
        """
        Возвращает список публичных привычек.

        @action позволяет добавлять дополнительные эндпоинты к ViewSet'у, которые не входят в стандартные CRUD, он
        автоматически даст новый маршрут используя DefaultRouter.

        Эндпоинт:
        GET /habits/public/
        """
        habits = Habit.objects.filter(is_public=True).order_by("created_at")
        page = self.paginate_queryset(habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)
