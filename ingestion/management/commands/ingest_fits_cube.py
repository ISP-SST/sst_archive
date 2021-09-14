import uuid

from django.core.management.base import BaseCommand, CommandError
from astropy.io import fits
import os.path
from datetime import datetime

from django.conf import settings

from dataset.models import DataLocation, Dataset
from data_access.models import DataLocationAccessControl
from extra_data.models import AnimatedGifPreview, ImagePreview
from ingestion.utils.generate_animated_preview import generate_animated_gif_preview
from ingestion.utils.generate_image_preview import generate_image_preview


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


def _generate_access_control_entities(data_location, fits_header):
    # Create access control row for this observation.
    release_date_str = fits_header['RELEASE']
    release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()

    release_comment = fits_header['RELEASEC']
    try:
        access_control = DataLocationAccessControl.objects.get(data_location=data_location)
        access_control.release_date = release_date
        access_control.release_comment = release_comment
    except DataLocationAccessControl.DoesNotExist:
        access_control = DataLocationAccessControl(data_location=data_location,
                                                   release_date=release_date,
                                                   release_comment=release_comment)
    access_control.save()


def _create_or_update_data_location(fits_cube, dataset):
    (fits_cube_path, fits_cube_name) = os.path.split(fits_cube)
    cube_size = os.path.getsize(fits_cube)

    try:
        data_location = DataLocation.objects.get(dataset=dataset, file_path=fits_cube_path, file_name=fits_cube_name)
        data_location.file_size = cube_size
    except DataLocation.DoesNotExist:
        data_location = DataLocation(dataset=dataset, file_path=fits_cube_path, file_size=cube_size,
                                     file_name=fits_cube_name)

    data_location.save()
    return data_location


def _create_gif_preview(hdus, data_location):
    try:
        preview = AnimatedGifPreview.objects.get(data_location=data_location)
        gif_uri = preview.animated_gif
        filename = os.path.basename(gif_uri)
        expected_gif_uri = os.path.join(settings.GIF_URL_ROOT, filename)
        gif_path = os.path.join(settings.GIF_ROOT, filename)

        if gif_uri != expected_gif_uri:
            preview.animated_gif = expected_gif_uri
            preview.save()
    except AnimatedGifPreview.DoesNotExist:
        gif_filename = '%s.gif' % uuid.uuid4()
        gif_path = os.path.join(settings.GIF_ROOT, gif_filename)
        gif_uri = os.path.join(settings.GIF_URL_ROOT, gif_filename)
        preview = AnimatedGifPreview(data_location=data_location, animated_gif=gif_uri)
        preview.save()

    generate_animated_gif_preview(hdus, gif_path)


def _create_image_preview(hdus, data_location):
    try:
        preview = ImagePreview.objects.get(data_location=data_location)
        image_path = preview.image_path
        image_url_path = preview.image_url
    except ImagePreview.DoesNotExist:
        image_filename = '%s.png' % uuid.uuid4()
        image_path = os.path.join(settings.GENERATED_ROOT, 'images', image_filename)
        image_url_path = os.path.join(settings.GENERATED_URL_ROOT, 'images', image_filename)
        preview = ImagePreview(data_location=data_location, image_path=image_path, image_url=image_url_path)

    generate_image_preview(hdus, image_path)

    preview.save()


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

        data_location = _create_or_update_data_location(fits_cube, dataset)

        _generate_access_control_entities(data_location, fits_header)

        # Generate an animated GIF as a preview.
        _create_gif_preview(hdus, data_location)

        # Generate static image preview.
        _create_image_preview(hdus, data_location)

        new_model_type = dataset.metadata_model

        fields = [field.name for field in new_model_type._meta.get_fields()]

        properties = {'fits_header': fits_header.tostring()}

        if options['observation_id']:
            oid = options['observation_id']
        else:
            oid = _generate_observation_id(fits_header)

        for key in fits_header:
            model_keyword = str(key).lower().replace('-', '_')
            if model_keyword in fields:
                properties[model_keyword] = fits_header.get(key)

        properties['oid'] = oid

        try:
            model = new_model_type.objects.get(oid=oid)
            for (key, value) in properties.items():
                setattr(model, key, value)
        except new_model_type.DoesNotExist:
            model = new_model_type(**properties)

        model.data_location = data_location
        model.save()
