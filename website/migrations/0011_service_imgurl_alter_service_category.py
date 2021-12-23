# Generated by Django 4.0 on 2021-12-23 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_service_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='imgUrl',
            field=models.CharField(default='https://via.placeholder.com/100', help_text='If the static file `css/images/<name>.png` does not exist, use this url', max_length=128, verbose_name='URL to image'),
        ),
        migrations.AlterField(
            model_name='service',
            name='category',
            field=models.CharField(choices=[('NON_INV', 'Non-invasive procedure'), ('SKIN', 'Skin'), ('APP', 'Appearance'), ('HEALTH', 'Health')], default='SKIN', max_length=7),
        ),
    ]