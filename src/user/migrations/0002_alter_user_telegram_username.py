# Generated by Django 5.0 on 2023-12-28 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telegram_username',
            field=models.TextField(help_text='Юзернейм в телеграмме', max_length=500, unique=True),
        ),
    ]
