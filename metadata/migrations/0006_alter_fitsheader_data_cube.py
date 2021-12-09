# Generated by Django 3.2.6 on 2021-12-09 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0012_auto_20211206_1035'),
        ('metadata', '0005_resave_metadata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fitsheader',
            name='data_cube',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fits_header', to='observations.datacube'),
        ),
    ]
