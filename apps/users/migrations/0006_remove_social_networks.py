# apps/users/migrations/0006_remove_social_networks.py
from django.db import migrations


def remove_social_network_columns(apps, schema_editor):
    """
    Безопасное удаление столбцов социальных сетей из таблицы пользователей.

    Этот метод использует прямые SQL-запросы для удаления столбцов,
    что позволяет избежать возможных проблем с ORM Django.
    """
    db_table = 'users_customuser'
    columns_to_remove = ['facebook', 'twitter', 'instagram', 'telegram']

    for column in columns_to_remove:
        try:
            # Используем IF EXISTS для предотвращения ошибок, если столбец уже удален
            schema_editor.execute(f'ALTER TABLE {db_table} DROP COLUMN IF EXISTS {column}')
            print(f'Столбец {column} успешно удален')
        except Exception as e:
            print(f"Предупреждение: Ошибка при удалении столбца {column}: {e}")


def restore_social_network_columns(apps, schema_editor):
    """
    Метод отката миграции на случай непредвиденных обстоятельств.
    В данном случае мы не восстанавливаем поля, так как удаление необратимо.
    """
    print("Откат миграции не требуется. Социальные сети были намеренно удалены.")


class Migration(migrations.Migration):
    """
    Миграция для удаления полей социальных сетей из модели CustomUser.
    """
    dependencies = [
        ('users', '0005_auto_20250218_2153'),  # Указываем предыдущую миграцию
    ]

    operations = [
        # Используем RunPython для выполнения кастомной логики удаления
        migrations.RunPython(
            remove_social_network_columns,
            restore_social_network_columns
        )
    ]

# <!-- AI-TODO:
# 1. Протестировать миграцию на staging-окружении
# 2. Убедиться в отсутствии зависимостей от удаленных полей
# 3. Обновить документацию проекта
# -->