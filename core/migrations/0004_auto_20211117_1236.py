# Generated by Django 3.2.6 on 2021-11-17 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_userprofile_purpose'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='affiliation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='purpose',
            field=models.CharField(blank=True, help_text='The reason why the account was created', max_length=190, null=True),
        ),
    ]
