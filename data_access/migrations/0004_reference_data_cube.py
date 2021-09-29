from django.db import migrations


def reference_data_cubes(apps, schema_editor):
    DataLocationAccessControl = apps.get_model('data_access', 'DataLocationAccessControl')
    DataLocationAccessGrant = apps.get_model('data_access', 'DataLocationAccessGrant')
    DataLocationAccessToken = apps.get_model('data_access', 'DataLocationAccessToken')
    DataCube = apps.get_model('observations', 'DataCube')

    def update_object(obj):
        data_location = obj.data_location
        try:
            data_cube = DataCube.objects.get(filename=data_location.file_name)
        except:
            return
        obj.data_cube = data_cube
        obj.save()

    [update_object(o) for o in DataLocationAccessControl.objects.all()]
    [update_object(o) for o in DataLocationAccessGrant.objects.all()]
    [update_object(o) for o in DataLocationAccessToken.objects.all()]


class Migration(migrations.Migration):

    dependencies = [
        ('data_access', '0003_auto_20210929_1407'),
    ]

    operations = [
        migrations.RunPython(reference_data_cubes),
    ]
