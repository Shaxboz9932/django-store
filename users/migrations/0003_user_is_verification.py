# Generated by Django 5.0.3 on 2024-04-21 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_emailverification'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verification',
            field=models.BooleanField(default=False),
        ),
    ]
