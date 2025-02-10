# Generated by Django 5.1.4 on 2025-02-10 10:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_user_groups_user_is_staff_user_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionlog',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
