from django.core.management.base import BaseCommand, CommandError
from astropy.io import fits
import os.path
from datetime import date, datetime


from dataset.models import DataLocation, Dataset
from data_access.models import AccessControl


def _generate_observation_id(fits_header):
    # "2019-04-16T08:20:18.96758_6173_0-36,38,39"
    date_beg = fits_header['DATE-BEG']
    filter1 = fits_header['FILTER1']
    scannum = fits_header['SCANNUM']
    if isinstance(scannum, list):
        scannum = scannum.join(',')
    else:
        scannum = str(scannum)
    return '%s_%s_%s' % (date_beg.strip(), filter1.strip(), scannum)


class Command(BaseCommand):
    help = 'Ingests the specified FITS cube into the database.'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--fits_cube', required=True, type=str)
        parser.add_argument('-o', '--observation-id', required=False, default=None)

    def handle(self, *args, **options):
        fits_cube = options['fits_cube']

        if not os.path.exists(fits_cube):
            raise CommandError('Provided FITS cube does not exist: %s' % fits_cube)

        try:
            hdus = fits.open(fits_cube)
            fits_header = hdus[0].header
        except:
            raise CommandError('Cannot open provided FITS cube: %s' % fits_cube)

        # TODO(daniel): Check that 'INSTRUME' key exists in header.
        instrument = str(fits_header['INSTRUME']).strip().lower()

        dataset = Dataset.objects.get(name__iexact=instrument)

        (fits_cube_path, fits_cube_name) = os.path.split(fits_cube)
        cube_size = os.path.getsize(fits_cube)

        try:
            data_location = DataLocation.objects.get(dataset=dataset, file_path=fits_cube_path, file_name=fits_cube_name)
            data_location.file_size = cube_size
        except DataLocation.DoesNotExist:
            data_location = DataLocation(dataset=dataset, file_path=fits_cube_path, file_size=cube_size,
                                         file_name=fits_cube_name)

        data_location.save()

        # Create access control row for this observation.
        release_date_str = fits_header['RELEASE']
        release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
        access_control = AccessControl(data_location=data_location, release_date=release_date)
        access_control.save()

        # access_control.assign_permission_to_user()

        new_model_type = dataset.metadata_model

        fields = [field.name for field in new_model_type._meta.get_fields()]

        properties = {}
        properties['fits_header'] = fits_header.tostring()

        if options['observation_id']:
            oid = options['observation_id']
        else:
            oid = _generate_observation_id(fits_header)


        for key in fits_header:
            model_keyword = str(key).lower().replace('-', '_')
            if model_keyword in fields:
                properties[model_keyword] = fits_header.get(key)

        properties['oid'] = oid

        new_model = new_model_type(**properties)
        new_model.data_location = data_location
        new_model.save()
