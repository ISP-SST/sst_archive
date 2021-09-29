# Generated by Django 3.2.6 on 2021-09-29 15:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('name', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, help_text='Instrument description', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(help_text='Path to the file, relative to the file root and excluding the name of the file', max_length=191)),
                ('file_name', models.CharField(help_text='Full file name including extension (.fits)', max_length=120, unique=True)),
                ('file_size', models.PositiveBigIntegerField(help_text='Size of the file in bytes')),
                ('instrument', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dataset.instrument')),
            ],
        ),
    ]
