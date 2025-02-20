#!/usr/bin/env python
import os
import sys


def main():
    """Запускает административные команды проекта."""
    # Загружаем переменные окружения из .env файла
    try:
        from dotenv import load_dotenv
        load_dotenv()  # Загружает переменные из .env в os.environ
        print("Переменные окружения успешно загружены из .env файла")
    except ImportError:
        print("ВНИМАНИЕ: python-dotenv не установлен. Переменные окружения из .env не будут загружены.")
        print("Установите его командой: pip install python-dotenv")

    # Устанавливаем переменную окружения для использования настроек (сейчас мы используем настройки для разработки)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Убедитесь, что он установлен и "
            "доступен в PYTHONPATH. Активируйте виртуальное окружение."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()