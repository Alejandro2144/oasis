# Generated by Django 4.0.3 on 2022-03-16 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_alter_informacionpaciente_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informacionpaciente',
            name='etnicidad',
            field=models.CharField(max_length=255),
        ),
    ]