from django.db import models


class Habit(models.Model):
    """
    Представляет модель полезной привычки.
    Attributes:
        user (User): Пользователь — создатель привычки
        place (str): Место выполнения привычки
        time (time): Время выполнения привычки
        action (str): Действие, которое представляет собой привычку
        is_pleasant (bool): Признак приятной привычки
        related_habit (Habit): Связанная привычка
        periodicity (int): Периодичность выполнения привычки
        reward (str): Вознаграждение
        duration (duration): Время на выполнение
        is_public (bool): Признак публичности привычки
        created_at (datetime): Дата и время создания привычки
    """

    # Пользователь — создатель привычки
    user = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",  # определяет имя обратной связи — то, как обращаться к связанным объектам с
        # другой стороны связи
    )  # type: ignore[var-annotated]

    # Место — место, в котором необходимо выполнять привычку
    place = models.CharField(max_length=255, verbose_name="Место")  # type: ignore[var-annotated]

    # Время — время, когда необходимо выполнять полезную привычку
    time = models.TimeField(verbose_name="Время")  # type: ignore[var-annotated]

    # Действие — действие, которое представляет собой полезная привычка
    action = models.CharField(max_length=255, verbose_name="Действие")  # type: ignore[var-annotated]

    # Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки
    is_pleasant = models.BooleanField(
        default=False, editable=False, verbose_name="Приятная привычка"
    )  # type: ignore[var-annotated]

    # Связанная привычка — привычка, которая связана с другой привычкой, важно указывать для полезных привычек, но не
    # для приятных
    related_habit = models.ForeignKey(
        "habit.PleasantHabit",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Указывается только для полезных привычек",
    )  # type: ignore[var-annotated]

    # Периодичность (по умолчанию ежедневная) — периодичность выполнения полезной привычки для напоминания в днях
    periodicity = models.PositiveSmallIntegerField(
        default=1, verbose_name="Периодичность (в днях)"
    )  # type: ignore[var-annotated]

    # Вознаграждение — чем пользователь должен себя вознаградить после выполнения полезной привычки
    reward = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Вознаграждение"
    )  # type: ignore[var-annotated]

    # Время на выполнение — время, которое предположительно потратит пользователь на выполнение полезной привычки
    duration = models.DurationField(verbose_name="Время на выполнение")  # type: ignore[var-annotated]

    # Признак публичности — привычки можно публиковать в общий доступ, чтобы другие пользователи могли брать в пример
    # чужие привычки
    is_public = models.BooleanField(default=False, verbose_name="Публичная привычка")  # type: ignore[var-annotated]

    # Дата создания полезной привычки
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создана")  # type: ignore[var-annotated]

    id: int  # Для mypy

    # Возвращает строковое представление привычки
    def __str__(self) -> str:
        """
        Возвращает строковое представление привычки
        :return: Строковое представление привычки
        """
        return f"{self.action} - ({self.user})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"


class PleasantHabit(models.Model):
    """
    Представляет приятную привычку.
    Attributes:
        user (User): Пользователь — создатель привычки
        place (str): Место выполнения привычки
        action (str): Действие, которое представляет собой приятную привычку
        created_at (datetime): Дата создания приятной привычки
    """

    # Пользователь — создатель привычки
    user: models.ForeignKey = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="pleasant_habits",
        verbose_name="Пользователь",
    )

    # Признак приятной привычки — привычка, которую можно привязать к выполнению полезной привычки
    is_pleasant: models.BooleanField = models.BooleanField(
        default=True, editable=False, verbose_name="Приятная привычка"
    )

    # Место — место, в котором необходимо выполнять привычку
    place: models.CharField = models.CharField(max_length=255, verbose_name="Место")

    # Действие — действие, которое представляет собой полезная привычка
    action: models.CharField = models.CharField(max_length=255, verbose_name="Действие")

    # Дата создания полезной привычки
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Создана")

    id: int  # Для mypy

    # Возвращает строковое представление приятной привычки
    def __str__(self) -> str:
        """
        Возвращает строковое представление приятной привычки
        :return: Строковое представление приятной привычки
        """
        return f"{self.action} - ({self.user})"

    class Meta:
        verbose_name = "Приятная привычка"
        verbose_name_plural = "Приятные привычки"
