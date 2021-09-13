# Generated by Django 3.2.6 on 2021-09-10 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0002_alter_datalocation_unique_together'),
        ('extra_data', '0005_alter_animatedgifpreview_data_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagePreview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=255, verbose_name='Relative URL to image preview')),
                ('image_path', models.CharField(max_length=255, verbose_name='Absolute path to image on disk')),
                ('data_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='thumbnail', to='dataset.datalocation')),
            ],
        ),
        migrations.DeleteModel(
            name='ThumbnailPreview',
        ),
    ]
