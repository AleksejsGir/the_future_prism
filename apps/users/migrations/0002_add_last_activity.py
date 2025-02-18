from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='last_activity',
            field=models.DateTimeField(
                auto_now=True,
                help_text='Время последней активности пользователя',
                verbose_name='Последняя активность',
            ),
        ),
    ]