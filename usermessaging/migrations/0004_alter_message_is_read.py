# Generated by Django 4.0.3 on 2022-04-10 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermessaging', '0003_alter_message_is_read'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
