# Generated by Django 4.0.6 on 2022-10-14 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_trips_city_code_alter_preference_budget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trips',
            name='city_code',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
