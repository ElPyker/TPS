# Generated by Django 5.1.4 on 2025-02-14 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_price_amount_alter_price_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='combo',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
