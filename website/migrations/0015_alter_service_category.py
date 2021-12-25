# Generated by Django 4.0 on 2021-12-25 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_remove_service_length_service_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('SKIN', 'Skin'), ('APP', 'Appearance'), ('HEALTH', 'Health'), ('NON_INV', 'Non-invasive procedure')], default='SKIN', max_length=7),
        ),
    ]
