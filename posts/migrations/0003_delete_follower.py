# Generated by Django 4.0.3 on 2022-04-03 03:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_follower'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Follower',
        ),
    ]