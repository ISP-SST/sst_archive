# Generated by Django 3.2.6 on 2021-10-15 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0003_alter_datacube_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datacube',
            name='path',
            field=models.TextField(help_text='Full path to the file'),
        ),
    ]
