# Generated by Django 4.2.7 on 2024-05-09 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='id_device',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]
