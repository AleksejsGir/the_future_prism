#!/usr/bin/env python
import os
import sys

def main():
    """Запускает административные команды проекта."""
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
