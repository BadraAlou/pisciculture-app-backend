# Generated by Django 5.1.2 on 2025-01-28 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionferme', '0007_alter_alevin_coutachattilapia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aliment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(blank=True, max_length=50, verbose_name='Aliment 1')),
                ('quantite', models.FloatField(default=0)),
                ('prix', models.PositiveIntegerField(default=0, verbose_name='Prix Aliment 1')),
            ],
        ),
        migrations.RemoveField(
            model_name='rationjournaliere',
            name='aliment1',
        ),
        migrations.RemoveField(
            model_name='rationjournaliere',
            name='aliment2',
        ),
        migrations.RemoveField(
            model_name='rationjournaliere',
            name='aliment3',
        ),
        migrations.RemoveField(
            model_name='rationjournaliere',
            name='aliment4',
        ),
        migrations.RemoveField(
            model_name='rationjournaliere',
            name='aliment5',
        ),
        migrations.RemoveField(
            model_name='rationjournaliere',
            name='nom',
        ),
        migrations.RemoveField(
            model_name='rationjournaliere',
            name='produit1',
        ),
        migrations.RemoveField(
            model_name='rationjournaliere',
            name='produit2',
        ),
        migrations.RemoveField(
            model_name='rationjournaliere',
            name='produit3',
        ),
    ]
