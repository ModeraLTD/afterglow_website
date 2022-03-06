# Generated by Django 4.0 on 2022-03-05 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0124_alter_service_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('APP', 'Appearance'), ('HEALTH', 'Health'), ('SKIN', 'Skin'), ('NON_INV', 'Non-invasive procedure')], default='SKIN', max_length=7),
        ),
    ]
