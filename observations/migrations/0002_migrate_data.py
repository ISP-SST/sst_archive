import os

from django.db import migrations


def migrate_data(apps, schema_editor):
    OldInstrument = apps.get_model('dataset', 'Instrument')
    DataLocation = apps.get_model('dataset', 'DataLocation')
    Metadata = apps.get_model('metadata', 'Metadata')

    NewInstrument = apps.get_model('observations', 'Instrument')
    DataCube = apps.get_model('observations', 'DataCube')

    for instrument in OldInstrument.objects.all():
        instrument, created = NewInstrument.objects.get_or_create(name=instrument.name, description=instrument.description)

    for data_location in DataLocation.objects.all():
        try:
            metadata = Metadata.objects.get(data_location=data_location)
        except:
            continue

        filename = data_location.file_name
        full_path = os.path.join(data_location.file_path, filename)
        file_size = data_location.file_size
        instrument = NewInstrument.objects.get(name=data_location.instrument.name)

        oid = metadata.oid

        cube, created = DataCube.objects.get_or_create(filename=filename, defaults={'path': full_path, 'size': file_size,
                                                                           'instrument': instrument, 'oid': oid})
        if not created:
            cube.update(path=full_path, size=file_size, instrument=instrument, oid=oid)
            cube.save()


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_data),
    ]
