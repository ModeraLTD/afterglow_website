# Generated by Django 4.0 on 2021-12-27 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0027_alter_service_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('HEALTH', 'Health'), ('SKIN', 'Skin'), ('APP', 'Appearance'), ('NON_INV', 'Non-invasive procedure')], default='SKIN', max_length=7),
        ),
    ]
