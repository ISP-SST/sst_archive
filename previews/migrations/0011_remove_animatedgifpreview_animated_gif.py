# Generated by Django 3.2.6 on 2021-10-21 10:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('previews', '0010_spectrallinedata_data_preview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animatedgifpreview',
            name='animated_gif',
        ),
    ]