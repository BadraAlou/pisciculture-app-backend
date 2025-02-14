# Generated by Django 5.1.2 on 2025-01-30 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionferme', '0011_charges'),
    ]

    operations = [
        migrations.AddField(
            model_name='cycleproduction',
            name='cycle',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='cycleproduction',
            name='date_fin',
            field=models.DateField(null=True, verbose_name='Date de fin de cycle'),
        ),
    ]
