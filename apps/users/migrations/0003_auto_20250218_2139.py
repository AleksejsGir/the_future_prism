# apps/users/migrations/0003_empty.py
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),  # Указываем зависимость от начальной миграции
    ]

    operations = [
        # Пустые операции, так как поля уже существуют
    ]