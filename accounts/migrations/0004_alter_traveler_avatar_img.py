# Generated by Django 4.0.6 on 2022-10-04 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_traveler_avatar_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traveler',
            name='avatar_img',
            field=models.ImageField(default='default.png', upload_to='profile_pics'),
        ),
    ]
