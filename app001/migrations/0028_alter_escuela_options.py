# Generated by Django 3.2 on 2024-05-15 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app001', '0027_alter_directivo_escuela'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='escuela',
            options={'ordering': ['-cuise'], 'verbose_name_plural': 'Escuelas'},
        ),
    ]
