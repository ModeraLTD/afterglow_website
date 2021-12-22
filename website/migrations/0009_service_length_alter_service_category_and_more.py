# Generated by Django 4.0 on 2021-12-22 15:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_rename_service_booking_service_remove_booking_bookin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='length',
            field=models.TimeField(default=datetime.time(1, 0), verbose_name='Length of service (minutes)'),
        ),
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('SKIN', 'Skin'), ('HEALTH', 'Health'), ('NON_INV', 'Non-invasive procedure'), ('APP', 'Appearance')], default='SKIN', max_length=7),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(max_length=40),
        ),
    ]
