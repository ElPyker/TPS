# Generated by Django 5.1.4 on 2025-01-08 03:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Combo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('is_available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dino',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('stack', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Tribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ComboDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('combo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.combo')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.item')),
            ],
        ),
        migrations.CreateModel(
            name='Genetic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('health_base', models.IntegerField()),
                ('health_mutates', models.IntegerField(default=0)),
                ('stamina_base', models.IntegerField()),
                ('stamina_mutates', models.IntegerField(default=0)),
                ('oxygen_base', models.IntegerField()),
                ('oxygen_mutates', models.IntegerField(default=0)),
                ('food_base', models.IntegerField()),
                ('food_mutates', models.IntegerField(default=0)),
                ('weight_base', models.IntegerField()),
                ('weight_mutates', models.IntegerField(default=0)),
                ('damage_base', models.IntegerField()),
                ('damage_mutates', models.IntegerField(default=0)),
                ('sale_format', models.CharField(choices=[('egg', 'Egg'), ('baby', 'Baby'), ('grown', 'Grown'), ('embryo', 'Embryo')], max_length=50)),
                ('is_for_sale', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('dino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.dino')),
                ('tribe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.tribe')),
            ],
        ),
        migrations.AddField(
            model_name='combo',
            name='tribe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.tribe'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('tribe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.tribe')),
            ],
        ),
    ]
