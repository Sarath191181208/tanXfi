# Generated by Django 5.0.7 on 2024-07-28 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='coin',
            field=models.CharField(default='btcusdt', max_length=10),
        ),
    ]
