# Generated by Django 3.2.6 on 2021-10-18 09:27
import os

from django.core.files import File
from django.db import migrations, models


def migrate_animations(apps, schema_editor):
    AnimatedGifPreview = apps.get_model('previews', 'AnimatedGifPreview')

    for preview in AnimatedGifPreview.objects.all():
        preview.full_size.save(os.path.basename(preview.image_path),
                           File(open(preview.image_path, 'rb'))
                           )
        preview.save()


class Migration(migrations.Migration):

    dependencies = [
        ('previews', '0007_auto_20211015_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagepreview',
            name='image_path',
        ),
        migrations.RemoveField(
            model_name='imagepreview',
            name='image_url',
        ),
        migrations.AddField(
            model_name='animatedgifpreview',
            name='full_size',
            field=models.ImageField(null=True, upload_to='gifs/full-size/', verbose_name='Preview animation stored in the managed upload folder'),
        ),
    ]
