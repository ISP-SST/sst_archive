from django.db import migrations

from metadata.models import update_parent_observation


def update_observation_date_fields_through_resave(apps, schema_editor):
    Observation = apps.get_model("observations", "Observation")
    for observation in Observation.objects.all():
        update_parent_observation(observation)


class Migration(migrations.Migration):
    dependencies = [
        ('observations', '0011_auto_20211115_1250'),
        ('metadata', '0004_alter_metadata_data_cube')
    ]

    operations = [
        migrations.RunPython(
            update_observation_date_fields_through_resave
        )
    ]
