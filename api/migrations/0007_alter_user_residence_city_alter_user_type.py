# Generated by Django 4.2.7 on 2024-02-14 20:24

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_city_name_alter_usertype_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='residence_city',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.city'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='api.usertype'),
            preserve_default=False,
        ),
    ]