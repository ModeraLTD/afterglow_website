# Generated by Django 4.0 on 2021-12-23 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0009_service_length_alter_service_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
