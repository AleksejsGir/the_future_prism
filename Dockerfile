# Dockerfile
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

# Создаем необходимые директории
RUN mkdir -p /app/media /app/staticfiles /app/sent_emails



# Открываем порт 8000 для доступа к приложению
EXPOSE 8000

# Команда для запуска приложения (переопределяется в docker-compose)
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]