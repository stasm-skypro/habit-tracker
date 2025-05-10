# Используем Python-образ
FROM python:3.12-slim

# Создаем группу и пользователя, чтобы комнды не выполнялись от имени root.
Используем высоскоуровненые команды из Ubuntu (Dedian)
RUN addgroup -S groupdjango && adduser -S -G groupdjango userdj

# Устанавливаем переменные окружения
"""
Отключает создание .pyc файлов (байткода) при запуске Python-приложения.
Обычно Python создаёт .pyc файлы в __pycache__, чтобы ускорить последующие загрузки модулей.
В Docker это не нужно:
Контейнеры часто одноразовые — кэш бесполезен.
.pyc файлы могут 'засорять' тома и слои образа.
Плюс: меньший размер образа, чище дерево файлов.
"""
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Установим netcat для ожидания сервисов
"""
nc нужен в entypont_*.sh, ждать база когда будет доступна, чтобы применить миграции.
"""
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Копируем все файлы проекта в контейнер
COPY . .

# Копируем скрипты и даём права на исполнение
COPY entrypoint_web.sh /entrypoint_web.sh
COPY entrypoint_celery.sh /entrypoint_celery.sh
COPY entrypoint_celery_beat.sh /entrypoint_celery_beat.sh
RUN chmod +x /entrypoint_*.sh

# Создаем директорию для статики от имени root и назначаем права
RUN mkdir -p /app/staticfiles && chown -R userdj:groupdjango /app/staticfiles

# Возвращаем пользователя на userdj
USER userdj

# Указываем команду для запуска проекта в контейнере при старте
"""
Запуск web-сервера через gunicorn.
"""
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]