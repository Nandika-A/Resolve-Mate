# Generated by Django 4.1.3 on 2022-11-11 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '__first__'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskhistory',
            name='assigned',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.workerprofile'),
        ),
    ]