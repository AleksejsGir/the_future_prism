# apps/users/migrations/0008_remove_social_networks_cleanup.py
from django.db import migrations


def cleanup_social_network_data(apps, schema_editor):
    """
    Безопасная миграция без обращения к удаленным полям.

    Основная цель - просто синхронизировать состояние базы данных.
    """
    print("Миграция социальных сетей завершена. Дополнительная очистка не требуется.")


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0007_remove_customuser_facebook_and_more'),
    ]

    operations = [
        migrations.RunPython(cleanup_social_network_data),
    ]