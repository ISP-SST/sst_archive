# Generated by Django 3.2.6 on 2021-09-29 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0002_migrate_data'),
        ('data_access', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datalocationaccesscontrol',
            name='data_cube',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='access_control', to='observations.datacube'),
        ),
        migrations.AddField(
            model_name='datalocationaccessgrant',
            name='data_cube',
            field=models.ForeignKey(help_text='The data cube that this token gives provides access to.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='access_grants', to='observations.datacube', verbose_name='Data Cube'),
        ),
        migrations.AddField(
            model_name='datalocationaccesstoken',
            name='data_cube',
            field=models.ForeignKey(help_text='The data cube that this token gives provides access to.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='access_token', to='observations.datacube', verbose_name='Data Cube'),
        ),
    ]
