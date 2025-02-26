from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """
    Django management команда для запуска приложения в Docker-окружении.
    """
    help = 'Инициализирует и запускает приложение в Docker-окружении'

    def handle(self, *args, **options):
        # 1. Проверка доступности базы данных
        call_command('wait_for_db')

        # 2. Применение миграций
        self.stdout.write(self.style.WARNING('Применение миграций...'))
        call_command('migrate')

        # 3. Сбор статических файлов
        self.stdout.write(self.style.WARNING('Сбор статических файлов...'))
        call_command('collectstatic', '--noinput')

        # 4. Запуск сервера разработки
        self.stdout.write(self.style.SUCCESS('Запуск веб-сервера...'))
        call_command('runserver', '0.0.0.0:8000')