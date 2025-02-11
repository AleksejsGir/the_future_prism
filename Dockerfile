# Dockerfile для проекта "The Future Prism"

# Используем официальный образ Python (3.11-slim)
FROM python:3.11-slim

# Отключаем запись байткода и буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл requirements.txt и устанавливаем зависимости Python
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Копируем весь проект в контейнер
COPY . /app

# (Опционально) Собираем статические файлы
# RUN python manage.py collectstatic --noinput

# Открываем порт 8000 для доступа к приложению
EXPOSE 8000

# Команда для запуска приложения с помощью Gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
