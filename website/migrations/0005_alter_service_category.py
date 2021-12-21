# Generated by Django 4.0 on 2021-12-21 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_service_category_booking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('Body', 'Full body'), ('Face', 'Full Face'), ('Pack', 'Full packages')], max_length=4),
        ),
    ]