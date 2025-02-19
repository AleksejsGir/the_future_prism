# apps/users/migrations/0005_fix_social_fields.py
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0004_merge_20250218_2143'),
    ]

    operations = [
        migrations.RunSQL(
            """
            DO $$
            BEGIN
                BEGIN
                    ALTER TABLE users_customuser ADD COLUMN IF NOT EXISTS facebook VARCHAR(200) NULL;
                EXCEPTION WHEN duplicate_column THEN
                    -- Колонка уже существует, ничего не делаем
                END;

                BEGIN
                    ALTER TABLE users_customuser ADD COLUMN IF NOT EXISTS twitter VARCHAR(200) NULL;
                EXCEPTION WHEN duplicate_column THEN
                    -- Колонка уже существует, ничего не делаем
                END;

                BEGIN
                    ALTER TABLE users_customuser ADD COLUMN IF NOT EXISTS instagram VARCHAR(200) NULL;
                EXCEPTION WHEN duplicate_column THEN
                    -- Колонка уже существует, ничего не делаем
                END;

                BEGIN
                    ALTER TABLE users_customuser ADD COLUMN IF NOT EXISTS telegram VARCHAR(200) NULL;
                EXCEPTION WHEN duplicate_column THEN
                    -- Колонка уже существует, ничего не делаем
                END;
            END $$;
            """,
            # Пустой откат, так как мы не хотим удалять поля при откате
            "SELECT 1;"
        ),
    ]