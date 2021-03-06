# Generated by Django 3.2.6 on 2021-10-13 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0003_alter_datacube_path'),
        ('previews', '0002_auto_20211001_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='R0Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_json', models.TextField(verbose_name='JSON blob with data for the plot')),
                ('data_version', models.IntegerField(verbose_name='Version number that indicates the format of the JSON blob. If the JSON blob data format changes this field should be bumped as well')),
                ('data_cube', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='r0data', to='observations.datacube')),
            ],
        ),
    ]
