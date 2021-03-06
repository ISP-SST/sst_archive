# Generated by Django 3.2.6 on 2021-09-30 08:27

from django.db import migrations, models
import django.db.models.deletion


def migrate_fits_headers(apps, schema_editor):
    FITSHeader = apps.get_model("metadata", "FITSHeader")
    Metadata = apps.get_model("metadata", "Metadata")

    for metadata in Metadata.objects.all():
        FITSHeader.objects.get_or_create(data_cube=metadata.data_cube, fits_header=metadata.fits_header)


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0001_initial'),
        ('metadata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FITSHeader',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fits_header', models.TextField(blank=True, null=True)),
                ('data_cube', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fits_header', to='observations.datacube')),
            ],
            options={
                'verbose_name': 'FITS Header',
            },
        ),
        migrations.RunPython(migrate_fits_headers),
        migrations.RemoveField(
            model_name='metadata',
            name='fits_header',
        ),
    ]
