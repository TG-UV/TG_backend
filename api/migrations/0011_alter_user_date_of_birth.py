# Generated by Django 4.2.7 on 2024-03-18 21:59

import api.custom_validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_vehicle_license_plate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(validators=[api.custom_validators.validate_date_of_birth]),
        ),
    ]
