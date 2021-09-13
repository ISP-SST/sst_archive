# Generated by Django 3.2.6 on 2021-09-06 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0002_alter_datalocation_unique_together'),
        ('extra_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='extradata',
            name='data_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='extra_data_extradata', to='dataset.datalocation'),
        ),
    ]
