# Generated by Django 3.2.6 on 2021-11-19 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_userprofile_email_reverification_disabled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='affiliation',
            field=models.CharField(blank=True, help_text='University or research center affiliation.', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email_reverification_disabled',
            field=models.BooleanField(default=False, help_text="When checked the user's email address will not needto be periodcally renewed.", verbose_name='E-mail re-verification disabled'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='purpose',
            field=models.CharField(blank=True, help_text='The reason why the account was created.', max_length=190, null=True, verbose_name='Account purpose'),
        ),
    ]
