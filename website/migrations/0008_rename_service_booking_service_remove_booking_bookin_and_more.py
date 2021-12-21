# Generated by Django 4.0 on 2021-12-21 20:20

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_alter_service_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='Service',
            new_name='service',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='bookin',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='id',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='user',
        ),
        migrations.RemoveField(
            model_name='service',
            name='number',
        ),
        migrations.AddField(
            model_name='booking',
            name='address',
            field=models.CharField(default=None, max_length=256, verbose_name='Address of booker'),
        ),
        migrations.AddField(
            model_name='booking',
            name='booking_id',
            field=models.CharField(default=None, max_length=8, verbose_name='Booking ID for user'),
        ),
        migrations.AddField(
            model_name='booking',
            name='firstName',
            field=models.CharField(default=None, max_length=16, verbose_name='First name of booker'),
        ),
        migrations.AddField(
            model_name='booking',
            name='lastName',
            field=models.CharField(default=None, max_length=32, verbose_name='Last name of booker'),
        ),
        migrations.AddField(
            model_name='booking',
            name='time_from',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 1, 0, 0), verbose_name='Starting date/time of booking'),
        ),
        migrations.AddField(
            model_name='booking',
            name='time_to',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 1, 0, 0), verbose_name='Ending date/time of booking'),
        ),
        migrations.AddField(
            model_name='booking',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('APP', 'Appearance'), ('SKIN', 'Skin'), ('NON_INV', 'Non-invasive procedure'), ('HEALTH', 'Health')], default='SKIN', max_length=7),
        ),
        migrations.AlterField(
            model_name='service',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
