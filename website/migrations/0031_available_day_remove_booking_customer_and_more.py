# Generated by Django 4.0 on 2021-12-29 02:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0030_remove_booking_booking_id_alter_service_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Available_Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.DateField(default=False, verbose_name='Create Available Dates')),
            ],
        ),
        migrations.RemoveField(
            model_name='booking',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='service',
        ),
        migrations.AlterField(
            model_name='booking',
            name='Time_From',
            field=models.IntegerField(choices=[(0, '09:00 - 09:30'), (1, '10:00 - 10:30'), (2, '11:00 - 11:30'), (3, '12:00 - 12:30'), (4, '13:00 - 13:30'), (5, '14:00 - 14:30'), (6, '15:00 - 15:30'), (7, '16:00 - 16:30'), (8, '17:00 - 17:30')]),
        ),
        migrations.AlterField(
            model_name='customer',
            name='fullname',
            field=models.CharField(default=None, max_length=20, verbose_name='Full Name'),
        ),
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('APP', 'Appearance'), ('SKIN', 'Skin'), ('HEALTH', 'Health'), ('NON_INV', 'Non-invasive procedure')], default='SKIN', max_length=7),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('complete', models.BooleanField(default=False, null=True)),
                ('date_ordered', models.DateTimeField(auto_now_add=True)),
                ('booking', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking', to='website.booking')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='customer', to='website.customer')),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Service', to='website.service')),
            ],
        ),
        migrations.AlterField(
            model_name='booking',
            name='date',
            field=models.ForeignKey(default=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='availability', to='website.available_day'),
        ),
    ]
