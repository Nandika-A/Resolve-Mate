# Generated by Django 4.0.4 on 2022-10-29 13:19

import django.contrib.postgres.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TaskHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('complaint', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('profession', models.CharField(max_length=100)),
                ('status', models.CharField(default='PENDING', max_length=50)),
                ('Comments', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, default=None), size=None)),
            ],
        ),
    ]
