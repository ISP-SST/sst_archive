# Generated by Django 3.2.6 on 2021-11-17 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20211117_0848'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='purpose',
            field=models.CharField(blank=True, max_length=190),
        ),
    ]