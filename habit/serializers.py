"""
Модуль сериализатора модели Habit.
RewardOrRelatedValidator и PleasantRestrictionsValidator — используются в Meta.validators так как они работают
с несколькими полями одновременно.
MaxDurationValidator, FrequencyValidator, RelatedHabitValidator — подключены к конкретным полям через validators=[...].
Типы полей:
DurationField валидируется через value.total_seconds().
'related_habit' задан как PrimaryKeyRelatedField, при этом валидатор принимает саму модель.
"""

from rest_framework import serializers

from .models import Habit, PleasantHabit
from .validators import (
    FrequencyValidator,
    MaxDurationValidator,
    PleasantRestrictionsValidator,
    RelatedHabitValidator,
    RewardOrRelatedValidator,
)


class HabitSerializer(serializers.ModelSerializer):
    """
    Проверяет валидность привычки согласно бизнес-правилам.
    Attributes:
        duration (DurationField): Время выполнения привычки
        related_habit (PrimaryKeyRelatedField): Связанная привычка
        periodicity (IntegerField): Периодичность выполнения привычки
    """

    # Исключает выполнение привычки более 120 секунд
    duration = serializers.DurationField(validators=[MaxDurationValidator()], required=True)

    # Проверяет, что в связанные привычки могут попадать только привычки с признаком приятной привычки
    related_habit = serializers.PrimaryKeyRelatedField(
        queryset=PleasantHabit.objects.all(),
        required=False,
        allow_null=True,
        validators=[RelatedHabitValidator()],
    )

    # Проверяет периодичность выполнения привычки. Нельзя выполнять привычку реже, чем 1 раз в 7 дней
    periodicity = serializers.IntegerField(validators=[FrequencyValidator()])

    class Meta:
        model = Habit
        fields = "__all__"
        validators = (
            RewardOrRelatedValidator(),  # Исключает одновременное указание вознаграждения и связанной привычки
            PleasantRestrictionsValidator(),  # Исключает появление у приятной привычки вознаграждения
            # или связанной привычки
        )
        read_only_fields = ("user",)
