#!/usr/bin/env python3

import argparse
import os
from datetime import date

from astropy.io import fits
from slumber import API

DEFAULT_SCIENCE_DATA_ROOT = '/storage/science_data'

DEFAULT_SST_API_INGESTION_ENDPOINT = 'https://dubshen.astro.su.se/sst_archive/api/v1'
DEFAULT_SST_API_KEY = '0633a8f415ca554ce807d1eaf9765447c08842b7'


def get_bullet_list_str(items):
    return ' * ' + '\n * '.join(items)


def prompt_for_is_swedish_data():
    response = input('Is this data cube Swedish data (y/N)? ')
    if response.strip().lower() in ['y', 'yes']:
        return True
    return False


def prompt_for_owner_email_addresses():
    print('Please enter the e-mail addresses of the users owning this data. If the data is owned by a university, '
          'enter the Stockholm SST Archive account e-mail for that university.')

    has_more = True
    addresses = []

    while has_more:
        address = input('Enter e-mail address (empty address ends input): ')

        if address:
            addresses.append(address)
        else:
            has_more = False

    print('')

    if addresses:
        print('The following owner e-mail addresses were provided:')
        print(get_bullet_list_str(addresses))
    else:
        print('No owner e-mail addresses were provided. An admin will need to manually add access rights for this data'
              'cube in the database.')

    print('')

    return addresses


def get_release_date_from_fits_file(science_data_root, fits_file):
    """
    Opens up a FITS file, pulls out the RELEASE keyword from the primary header and returns it as a date.
    """
    fits_file_abs_path = os.path.join(science_data_root, fits_file)

    try:
        with fits.open(fits_file_abs_path) as hdus:
            primary_header = hdus[0].header
            release = primary_header.get('RELEASE')
            release_date = date.fromisoformat(release)
            return release_date
    except (KeyError, ValueError, IndexError):
        return date.fromtimestamp(0)


class SstArchiveApi(API):
    """
    RESTful API interface for the Stockholm SST Archive.
    """

    def __init__(self, api_url, api_key):
        self.api_key = api_key
        super().__init__(api_url, auth=self.api_key_auth)

    def api_key_auth(self, request):
        request.headers['Authorization'] = 'Token %s' % self.api_key
        return request

    def __call__(self, resource_uri):
        return getattr(self, resource_uri)


def submit_fits_cube(fits_file, swedish_data=None, owner_emails=None, oid=None, interactive=False,
                     api_endpoint=DEFAULT_SST_API_INGESTION_ENDPOINT, api_key=DEFAULT_SST_API_KEY,
                     science_data_root=DEFAULT_SCIENCE_DATA_ROOT):
    """
    Sends information about a FITS data cube to the ingestion endpoint of the Stockholm SST Archive.
    """

    release_date = get_release_date_from_fits_file(science_data_root, fits_file)
    data_is_restricted = release_date > date.today()
    should_prompt = data_is_restricted and interactive

    if swedish_data is None:
        swedish_data = prompt_for_is_swedish_data() if should_prompt else False

    if owner_emails is None:
        owner_emails = prompt_for_owner_email_addresses() if should_prompt else []

    api = SstArchiveApi(api_endpoint, api_key)

    request_data = {
        'relative_path': fits_file,
        'owner_email_addresses': owner_emails,
        'swedish_data': swedish_data,
    }

    if oid:
        request_data['oid'] = oid

    print('Submitting data cube to the Stockholm SST Archive:\n')
    print('  ' + '\n  '.join([('%s: %s' % (key, request_data[key])) for key in request_data.keys()]))

    api.ingest.post(request_data)

    print('')
    print('Data cube submitted.')


def main():
    parser = argparse.ArgumentParser(description='Submits a FITS file to the Stockholm SST Archive.')

    parser.add_argument('fits_file', help='The FITS data cube to submit to the archive, relative to the '
                                          'root of the science_data/ directory')
    parser.add_argument('--oid', default=None, help='Observation ID')
    parser.add_argument('--swedish-data', action='store_true', default=None, help='Tag the FITS cube as Swedish data')
    parser.add_argument('--owner-emails', nargs='*', default=None,
                        help='Register the e-mails of the owners of this data')
    parser.add_argument('--interactive', action='store_true', help='Interactively prompt the user for owner e-mails and'
                                                                   'Swedish data status')
    parser.add_argument('--api-endpoint', default=DEFAULT_SST_API_INGESTION_ENDPOINT,
                        help='Override the HTTP ingestion endpoint')
    parser.add_argument('--api-key', default=DEFAULT_SST_API_KEY, help='API key for the ingestion endpoint')
    parser.add_argument('--science-data-root', default=DEFAULT_SCIENCE_DATA_ROOT)

    args = parser.parse_args()

    submit_fits_cube(**vars(args))


if __name__ == '__main__':
    main()
