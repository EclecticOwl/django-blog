# Generated by Django 4.0.3 on 2022-04-17 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_theme_theme_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='theme', to='core.profile'),
        ),
    ]