# Generated by Django 3.2.6 on 2021-10-15 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0004_alter_datacube_path'),
        ('previews', '0006_rename_preview_imagepreview_full_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagepreview',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='thumbnails/', verbose_name='Small preview image stored in managed upload folder'),
        ),
        migrations.AlterField(
            model_name='imagepreview',
            name='data_cube',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='previews', to='observations.datacube'),
        ),
    ]