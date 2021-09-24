# Generated by Django 3.2.6 on 2021-09-24 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tagcategory',
            options={'verbose_name': 'Tag category', 'verbose_name_plural': 'Tag categories'},
        ),
        migrations.AlterField(
            model_name='tagcategory',
            name='description',
            field=models.TextField(null=True, verbose_name='Description'),
        ),
    ]
