# Generated by Django 4.0 on 2022-03-05 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0118_rename_complete_order_billing_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('NON_INV', 'Non-invasive procedure'), ('SKIN', 'Skin'), ('APP', 'Appearance'), ('HEALTH', 'Health')], default='SKIN', max_length=7),
        ),
    ]
