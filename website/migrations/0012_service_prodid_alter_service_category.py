# Generated by Django 4.0 on 2021-12-24 16:11

from django.db import migrations, models
import website.models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_service_imgurl_alter_service_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='prodID',
            field=models.CharField(default=website.models.randomProdID, editable=False, max_length=8),
        ),
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('HEALTH', 'Health'), ('APP', 'Appearance'), ('NON_INV', 'Non-invasive procedure'), ('SKIN', 'Skin')], default='SKIN', max_length=7),
        ),
    ]
