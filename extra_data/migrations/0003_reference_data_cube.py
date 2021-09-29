from django.db import migrations


def reference_data_cubes(apps, schema_editor):
    ImagePreview = apps.get_model('extra_data', 'ImagePreview')
    AnimatedGifPreview = apps.get_model('extra_data', 'AnimatedGifPreview')
    DataCube = apps.get_model('observations', 'DataCube')

    def update_object(obj):
        data_location = obj.data_location
        try:
            data_cube = DataCube.objects.get(filename=data_location.file_name)
        except:
            return
        obj.data_cube = data_cube
        obj.save()

    [update_object(o) for o in ImagePreview.objects.all()]
    [update_object(o) for o in AnimatedGifPreview.objects.all()]


class Migration(migrations.Migration):

    dependencies = [
        ('extra_data', '0002_auto_20210929_1407'),
    ]

    operations = [
        migrations.RunPython(reference_data_cubes),
    ]
