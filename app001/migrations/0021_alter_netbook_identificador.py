# Generated by Django 3.2 on 2024-05-14 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app001', '0020_alter_netbook_identificador'),
    ]

    operations = [
        migrations.AlterField(
            model_name='netbook',
            name='identificador',
            field=models.IntegerField(null=True),
        ),
    ]