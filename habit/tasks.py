# поддержка отложенных аннотаций, все типы в аннотациях становятся строками до runtime, нужно для mypy
from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, cast

from django.conf import settings

import requests
from celery import shared_task

from habit.models import Habit

if TYPE_CHECKING:  # безопасный импорт User только для mypy, чтобы mypy понял откуда user, не влияет на runtime
    from user.models import User


def send_telegram_message(chat_id: int, text: str) -> None:
    """
    Отправляет сообщение в телеграм пользователя.
    :param chat_id: id пользователя в телеграм-чате
    :param text: Отправляемое сообщение
    :return:
    """
    token = settings.TELEGRAM_BOT_TOKEN
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})


@shared_task
def send_habit_reminders() -> None:
    """
    Напоминает пользователям о полезной привычке за 15 минут до начала.
    :return:
    """
    now = datetime.now()
    notify_time = now + timedelta(minutes=15)

    habits = cast(
        list[Habit], list(Habit.objects.filter(time__hour=notify_time.hour, time__minute=notify_time.minute))
    )

    for habit in habits:
        user: User = habit.user  # Явная аннотация помогает mypy - чтобы telegram_chat_id не вызывал ошибок
        if user.telegram_chat_id:
            message = f"Напоминание: через 15 минут необходимо выполнить привычку: {habit.action}"
            try:
                send_telegram_message(user.telegram_chat_id, message)
            except Exception as e:
                print(f"Ошибка при отправке сообщения в Telegram: {e}")


@shared_task
def test_task():
    print("Задача работает!")
