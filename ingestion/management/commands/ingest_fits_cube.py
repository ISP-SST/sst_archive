from django.core.management.base import BaseCommand, CommandError
from astropy.io import fits
import os.path
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.utils.timezone import make_aware

from dataset.models import DataLocation, Instrument
from data_access.models import DataLocationAccessControl
from extra_data.models import AnimatedGifPreview, ImagePreview
from ingestion.utils.generate_animated_preview import generate_animated_gif_preview
from ingestion.utils.generate_image_preview import generate_image_preview
from metadata.models import Metadata, FITSHeader
from observations.models import DataCube


def _generate_observation_id(fits_header):
    # "2019-04-16T08:20:18.96758_6173_0-36,38,39"
    date_beg = fits_header['DATE-BEG']
    filter1 = fits_header['FILTER1']
    # BUG(daniel): SCANNUM header does not contain what we need. We need to look into the
    #              VAR-EXT-SCANNUM extension table and read the list of scans from there.
    scannum = fits_header['SCANNUM']
    if isinstance(scannum, list):
        scannum = scannum.join(',')
    else:
        scannum = str(scannum)
    return '%s_%s_%s' % (date_beg.strip(), filter1.strip(), scannum)


def _generate_access_control_entities(data_cube, fits_header):
    # Create access control row for this observation.
    release_date_str = fits_header['RELEASE']
    release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()

    release_comment = fits_header['RELEASEC']
    try:
        access_control = DataLocationAccessControl.objects.get(data_cube=data_cube)
        access_control.release_date = release_date
        access_control.release_comment = release_comment
    except DataLocationAccessControl.DoesNotExist:
        access_control = DataLocationAccessControl(data_cube=data_cube,
                                                   release_date=release_date,
                                                   release_comment=release_comment)
    access_control.save()


def _create_or_update_data_cube(fits_cube, instrument):
    (fits_cube_path, fits_cube_name) = os.path.split(fits_cube)
    cube_size = os.path.getsize(fits_cube)

    try:
        data_cube = DataCube.objects.get(instrument=instrument, file_path=fits_cube_path, file_name=fits_cube_name)
        data_cube.size = cube_size
    except DataLocation.DoesNotExist:
        data_cube = DataLocation(instrument=instrument, file_path=fits_cube_path, file_size=cube_size,
                                     file_name=fits_cube_name)

    data_cube.save()
    return data_cube


def _create_gif_preview(hdus, data_cube):
    try:
        preview = AnimatedGifPreview.objects.get(data_cube=data_cube)
        gif_uri = preview.animated_gif
        filename = os.path.basename(gif_uri)
        expected_gif_uri = os.path.join(settings.GIF_URL_ROOT, filename)
        gif_path = os.path.join(settings.GIF_ROOT, filename)

        if gif_uri != expected_gif_uri:
            preview.animated_gif = expected_gif_uri
            preview.save()
    except AnimatedGifPreview.DoesNotExist:
        gif_filename = Path(data_cube.filename).with_suffix('.gif')
        gif_path = os.path.join(settings.GIF_ROOT, gif_filename)
        gif_uri = os.path.join(settings.GIF_URL_ROOT, gif_filename)
        preview = AnimatedGifPreview(data_cube=data_cube, animated_gif=gif_uri)
        preview.save()

    if not os.path.isfile(gif_path):
        generate_animated_gif_preview(hdus, gif_path)


def _create_image_preview(hdus, data_cube):
    try:
        preview = ImagePreview.objects.get(data_cube=data_cube)
        image_path = preview.image_path
        image_url_path = preview.image_url
    except ImagePreview.DoesNotExist:
        image_filename = Path(data_cube.filename).with_suffix('.png')
        image_path = os.path.join(settings.GENERATED_ROOT, 'images', image_filename)
        image_url_path = os.path.join(settings.GENERATED_URL_ROOT, 'images', image_filename)
        preview = ImagePreview(data_cube=data_cube, image_path=image_path, image_url=image_url_path)

    if not os.path.isfile(image_path):
        generate_image_preview(hdus, image_path)

    preview.save()


def _create_or_update_metadata(fits_header, data_cube, oid=None):
    model_type = Metadata

    fields = [field.name for field in model_type._meta.get_fields()]

    properties = {}

    if not oid:
        oid = _generate_observation_id(fits_header)

    for key in fits_header:
        model_keyword = str(key).lower().replace('-', '_').replace(' ', '_')
        if model_keyword in fields:
            properties[model_keyword] = fits_header.get(key)

    properties['oid'] = oid

    try:
        model = model_type.objects.get(oid=oid)
    except model_type.DoesNotExist:
        model = model_type(**properties)

    for (key, value) in properties.items():
        attr = getattr(model, key)
        if isinstance(attr, datetime):
            try:
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')

            try:
                import zoneinfo
            except ImportError:
                from backports import zoneinfo

            timezone = zoneinfo.ZoneInfo(settings.OBSERVATION_TIMEZONE)
            value = make_aware(value, timezone=timezone)

        setattr(model, key, value)

    model.data_cube = data_cube
    model.save()


def _create_or_update_fits_header(fits_header, data_cube):
    header, created = FITSHeader.objects.get_or_create(data_cube=data_cube)
    header.fits_header = fits_header.tostring()
    header.save()


class Command(BaseCommand):
    help = 'Ingests the specified FITS cube into the database.'

    def add_arguments(self, parser):
        parser.add_argument('-f', '--fits-cube', required=True, type=str)
        parser.add_argument('-o', '--observation-id', required=False, default=None)
        parser.add_argument('--generate-image-previews', action='store_true')
        parser.add_argument('--generate-animated-previews', action='store_true')

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

        instrument, created = Instrument.objects.get_or_create(name=instrument.upper())

        data_cube = _create_or_update_data_cube(fits_cube, instrument)

        _generate_access_control_entities(data_cube, fits_header)

        oid = options.get('observation_id', None)
        print('Extracting metadata from FITS cube...')
        _create_or_update_metadata(fits_header, data_cube, oid)

        print('Ingesting raw FITS header...')
        _create_or_update_fits_header(fits_header, data_cube)

        if options['generate_image_previews']:
            # Generate static image preview.
            print('Generating image preview...')
            _create_image_preview(hdus, data_cube)

        if options['generate_animated_previews']:
            # Generate an animated GIF as a preview.
            print('Generating animated GIF preview...')
            _create_gif_preview(hdus, data_cube)

