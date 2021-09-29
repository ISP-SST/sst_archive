# Generated by Django 3.2.7 on 2021-09-27 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dataset', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Category name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'Tag Category',
                'verbose_name_plural': 'Tag Categories',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='tags.tagcategory')),
            ],
            options={
                'unique_together': {('name', 'category')},
            },
        ),
        migrations.CreateModel(
            name='DataLocationTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='dataset.datalocation')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.tag')),
            ],
            options={
                'unique_together': {('data_location', 'tag')},
            },
        ),
    ]