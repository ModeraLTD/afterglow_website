# Generated by Django 4.0 on 2021-12-26 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0026_alter_service_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('HEALTH', 'Health'), ('NON_INV', 'Non-invasive procedure'), ('APP', 'Appearance'), ('SKIN', 'Skin')], default='SKIN', max_length=7),
        ),
    ]
