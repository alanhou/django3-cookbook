# Generated by Django 3.0.8 on 2020-08-12 14:40

from django.db import migrations, models
import myproject.apps.locations.models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20200812_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='picture',
            field=models.ImageField(default='', upload_to=myproject.apps.locations.models.upload_to, verbose_name='Picture'),
            preserve_default=False,
        ),
    ]
