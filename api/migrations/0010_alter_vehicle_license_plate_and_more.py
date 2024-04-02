# Generated by Django 4.2.7 on 2024-03-11 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_vehicle_license_plate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='license_plate',
            field=models.CharField(max_length=10),
        ),
        migrations.AddConstraint(
            model_name='vehicle',
            constraint=models.UniqueConstraint(fields=('license_plate', 'owner'), name='License_plate_Owner_Unique'),
        ),
    ]