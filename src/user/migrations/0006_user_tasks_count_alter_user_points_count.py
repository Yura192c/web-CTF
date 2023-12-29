# Generated by Django 5.0 on 2023-12-28 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_user_name_alter_user_telegram_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tasks_count',
            field=models.PositiveIntegerField(default=0, help_text='Количество задач'),
        ),
        migrations.AlterField(
            model_name='user',
            name='points_count',
            field=models.PositiveIntegerField(default=0, help_text='Количество очков'),
        ),
    ]