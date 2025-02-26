from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError
import time
import sys


class Command(BaseCommand):
    """
    Django management команда для ожидания готовности базы данных.
    """
    help = 'Ожидает доступности базы данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--max-tries',
            type=int,
            default=60,
            help='Максимальное количество попыток подключения'
        )
        parser.add_argument(
            '--wait-seconds',
            type=int,
            default=1,
            help='Время ожидания между попытками (в секундах)'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Проверка соединения с базой данных...'))
        db_conn = None
        max_tries = options['max_tries']
        wait_seconds = options['wait_seconds']

        for attempt in range(max_tries):
            try:
                db_conn = connections['default']
                db_conn.ensure_connection()
                self.stdout.write(self.style.SUCCESS('✅ База данных готова к работе!'))
                return
            except OperationalError:
                self.stdout.write(
                    self.style.WARNING(f'База данных недоступна, ожидание ({attempt + 1}/{max_tries})...')
                )
                time.sleep(wait_seconds)

        self.stdout.write(
            self.style.ERROR(f'❌ Не удалось подключиться к базе данных после {max_tries} попыток!')
        )
        sys.exit(1)