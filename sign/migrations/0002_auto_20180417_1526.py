# Generated by Django 2.0.4 on 2018-04-17 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='start_time',
            field=models.DateTimeField(verbose_name='events_time'),
        ),
    ]