# Generated by Django 5.1.4 on 2025-02-10 09:24

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], default='user', max_length=10)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('short_code', models.CharField(max_length=10, unique=True)),
            ],
        ),
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
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('playing', 'Playing'), ('gachatower', 'GachaTower'), ('afk', 'AFK')], default='playing', max_length=20)),
                ('afk_text', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.account')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SessionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.account')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.player')),
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
        migrations.AddField(
            model_name='account',
            name='tribe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='store.tribe'),
        ),
        migrations.AddField(
            model_name='user',
            name='tribe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.tribe'),
        ),
    ]
