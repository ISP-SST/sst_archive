# Generated by Django 3.2.6 on 2021-10-15 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('previews', '0005_imagepreview_preview'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagepreview',
            old_name='preview',
            new_name='full_size',
        ),
    ]