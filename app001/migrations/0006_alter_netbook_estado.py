# Generated by Django 3.2 on 2022-07-06 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app001', '0005_alter_netbook_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='netbook',
            name='estado',
            field=models.CharField(choices=[('ok', 'ok'), ('no funciona', 'no funciona'), ('bloqueada', 'bloqueada'), ('pendiente de revision', 'pendiente de revision'), ('pendiente migracion', 'pendiente migracion'), ('robada', 'robada')], default='pendiente de revision', max_length=30),
        ),
    ]
