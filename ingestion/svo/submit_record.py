#!/usr/bin/env python3
"""Example script for a dataset provider to submit metadata and data location records to the SOLARNET Virtual Observatory (SVO) RESTful API"""
import argparse
import logging
import os
import sys
from urllib.parse import urljoin

from astropy.io import fits
from dateutil.parser import parse, ParserError
from slumber import API
# Set with proper base URL of data, or set file URL explicitly through script argument
from slumber.exceptions import HttpNotFoundError

BASE_FILE_URL = 'https://dubshen.astro.su.se/data/'

# The default hdu name or index to use for extracting the metadata from the FITS file (can be specified here to avoid
# passing it by parameter to the script)
DEFAULT_FITS_HDU = 0

# If data should be offline by default (can be specified here to avoid passing it by parameter to the script)
DEFAULT_OFFLINE = False

# Default dataset name to use (can be specified here to avoid passing it by parameter to the script)
DEFAULT_DATASET = None

# Default username and API key of the user in the SVO owning the data (can be specified here to avoid passing it by
# parameter to the script)
DEFAULT_USERNAME = None
DEFAULT_API_KEY = None

# Keyword to use to generate a default oid
DATE_KEYWORD = 'date_obs'

# URL of the SVO RESTful API
# Don't change this
DEFAULT_API_URL = 'https://solarnet.oma.be/service/api/svo'

KNOWN_DATASETS = ['CRISP', 'CHROMIS']

"""
TODO(daniel): This file is a bit of a mess right now. It started as a straight forward example script for
              submitting metadata to the SVO. It has since been modified to support very specific use cases
              that make sense for the synchronization from the SST Archive to the SVO. We basically need to
              clean it up a bit and remove the parts that we don't expect to use.
"""


class SvoApi(API):
    """RESTful API interface for the SVO"""

    def __init__(self, api_url, username, api_key):
        self.username = username
        self.api_key = api_key
        super().__init__(api_url, auth=self.api_key_auth)

    def api_key_auth(self, request):
        """Sets the API key authentication in the request header"""
        request.headers['Authorization'] = 'ApiKey %s:%s' % (self.username, self.api_key)
        return request

    def __call__(self, resource_uri):
        """Return a resource from a resource URI"""
        return getattr(self, resource_uri)


class SvoRecord:
    """
    Specify one of fits_header and fits_file.
    """

    def __init__(self, fits_header=None, fits_file=None, fits_hdu=DEFAULT_FITS_HDU, file_url=None, file_path=None,
                 file_size=None, thumbnail_url=None, offline=DEFAULT_OFFLINE, oid=None, dataset=DEFAULT_DATASET,
                 username=DEFAULT_USERNAME, api_key=DEFAULT_API_KEY, api_url=DEFAULT_API_URL, **kwargs):
        self.fits_header = fits_header
        self.fits_file = fits_file
        self.fits_hdu = fits_hdu
        self.file_url = file_url
        self.file_path = file_path
        self.file_size = file_size
        self.thumbnail_url = thumbnail_url
        self.offline = offline
        self.dataset = dataset
        self.oid = oid
        self.api = SvoApi(api_url, username, api_key)

    def get_file_url(self):
        """Override to return the proper URL for the file"""
        if self.file_url:
            return self.file_url
        elif BASE_FILE_URL:
            return urljoin(BASE_FILE_URL, self.get_file_path())
        else:
            raise ValueError('file_url must be provided or BASE_FILE_URL must be set')

    def get_file_path(self):
        """Override to return the proper relative file path for the file"""
        if self.file_path:
            return self.file_path
        else:
            return self.fits_file.lstrip('./')

    def get_file_size(self):
        if self.file_size:
            return self.file_size
        elif self.fits_file:
            return os.path.getsize(self.fits_file)
        else:
            raise ValueError('Cannot retrieve the size of the FITS file')

    def get_fits_header(self):
        if self.fits_header:
            return self.fits_header
        else:
            with fits.open(self.fits_file) as hdus:
                fits_header = hdus[self.fits_hdu].header
                return fits_header

    def get_thumbnail_url(self):
        """Override to return the proper URL for the thumbnail"""
        return self.thumbnail_url

    def get_oid(self, metadata=None):
        """Override to return the proper OID for the metadata"""
        if self.oid:
            return self.oid
        elif not metadata:
            raise ValueError('oid or metadata must be provided')
        else:
            try:
                return parse(metadata[DATE_KEYWORD]).strftime('%Y%m%d%H%M%S')
            except ParserError as why:
                raise ValueError('Cannot parse keyword "%s" into an oid: %s' % (DATE_KEYWORD, why)) from why
            except KeyError as why:
                raise ValueError(
                    'Keyword "%s" missing in FITS header, cannot generate default oid' % DATE_KEYWORD) from why

    def _data_location_needs_updating(self, data_location_dict):
        return data_location_dict['file_url'] != self.file_url or data_location_dict['file_size'] != self.file_size or \
               data_location_dict['file_path'] != self.file_path or data_location_dict[
                   'thumbnail_url'] != self.thumbnail_url or data_location_dict['offline'] != self.offline

    def _is_data_location_shared(self, data_location_id, datasets):
        # TODO(daniel): This is a really inelegant way of determining if the data_location is shared between
        #               two or more metadata entries. Perhaps we can make a quick initial check to bypass the
        #               bulk of the work in a majority of cases.

        data_location_ref_count = 0

        def get_data_location_id(metadata):
            return metadata.get('data_location', {'id': None})['id']

        for dataset_name in datasets:
            dataset = self.api.dataset(dataset_name).get()
            metadata_root_uri = dataset['metadata']['resource_uri']

            all_metadata = self.api(metadata_root_uri).get(limit=0)['objects']

            data_location_ref_count += sum(
                get_data_location_id(metadata) == data_location_id for metadata in all_metadata)

        return data_location_ref_count > 1

    def _generate_data_location(self, dataset_name):
        dataset = self.api.dataset(dataset_name).get()

        data_location = {
            'dataset': dataset['resource_uri'],
            'file_url': self.get_file_url(),
            'file_size': self.get_file_size(),
            'file_path': self.get_file_path(),
            'thumbnail_url': self.get_thumbnail_url(),
            'offline': self.offline,
        }

        return data_location

    def _update_data_location(self, data_location):
        data_location.update({
            'file_url': self.get_file_url(),
            'file_size': self.get_file_size(),
            'file_path': self.get_file_path(),
            'thumbnail_url': self.get_thumbnail_url(),
            'offline': self.offline,
        })
        return data_location

    def get_data_location(self):
        """Return the data_location URI or info for creating a new metadata record"""
        # If a data_location record for this file already exist, we reuse it
        # Else we need to create a new one, with all the necessary info

        # The pair dataset/file_url must be unique in the database so we can search by it
        data_locations = self.api.data_location.get(dataset__name=self.dataset, file_url=self.get_file_url())

        if data_locations['objects']:
            data_location = data_locations['objects'][0]['resource_uri']
        else:
            data_location = self._generate_data_location(self.dataset)

        return data_location

    def get_metadata(self, remove_oid=False):
        """Return the metadata info for creating a new metadata record"""

        fits_header = self.get_fits_header()

        # Create a new metadata record from the FITS file header
        metadata = {
            'fits_header': fits_header.tostring().strip()
        }

        for keyword in self.api.keyword.get(limit=0, dataset__name=self.dataset)['objects']:
            try:
                metadata[keyword['name']] = fits_header[keyword['verbose_name']]
            except KeyError:
                logging.warning('Missing keyword "%s" in header, skipping!', keyword['verbose_name'])
            else:
                logging.debug('Header keyword "%s" = "%s"', keyword['verbose_name'], metadata[keyword['name']])

        if not remove_oid:
            metadata['oid'] = self.get_oid(metadata)

        return metadata

    def get_remote_metadata(self):
        dataset = self.api.dataset(self.dataset).get()
        metadata_root_uri = dataset['metadata']['resource_uri']
        oid = self.get_oid()

        return self.api(metadata_root_uri)(oid).get()

    def exists_in_svo(self):
        dataset = self.api.dataset(self.dataset).get()
        metadata_root_uri = dataset['metadata']['resource_uri']
        oid = self.get_oid()

        try:
            self.api(metadata_root_uri)(oid).get()
            return True
        except HttpNotFoundError:
            return False

    def create(self):
        """Create the metadata and data_location records in the API"""

        # Retrieve the metadata resource URI from the dataset
        dataset = self.api.dataset(self.dataset).get()
        resource_uri = dataset['metadata']['resource_uri']

        # Get the data to send to the API
        metadata = self.get_metadata()
        metadata['data_location'] = self.get_data_location()

        # To create a new record, POST to the resource URI of the metadata record
        result = self.api(resource_uri).post(metadata)
        return result

    def update(self):
        """Update the metadata and data_location records in the API"""

        dataset = self.api.dataset(self.dataset).get()
        metadata_root_uri = dataset['metadata']['resource_uri']

        # Get the data to send to the API
        metadata = self.get_metadata(remove_oid=True)

        oid = self.get_oid()

        existing_metadata = self.api(metadata_root_uri)(oid).get()
        existing_data_location = existing_metadata['data_location']

        if self._data_location_needs_updating(existing_data_location):
            data_location_id = existing_data_location['id']

            # If the data_location is shared with other metadata, create a new one. If not, simply update the existing
            # data_location.
            if self._is_data_location_shared(data_location_id, KNOWN_DATASETS):
                # Generate a new data_location.
                metadata['data_location'] = self._generate_data_location(self.dataset)
            else:
                self._update_data_location(existing_data_location)
                metadata['data_location'] = existing_data_location

        # We update the existing record by adding the 'oid' to the root URI for
        # the metadata and executing a PATCH request.
        result = self.api(metadata_root_uri)(oid).patch(metadata)
        return result

    def delete(self):
        """Remove this metadata record from in the API."""

        dataset = self.api.dataset(self.dataset).get()
        metadata_root_uri = dataset['metadata']['resource_uri']
        oid = self.get_oid()
        result = self.api(metadata_root_uri)(oid).delete()
        return result


if __name__ == "__main__":

    # Get the arguments
    parser = argparse.ArgumentParser(description='Submit metadata from a FITS file to the SVO')
    parser.add_argument('--debug', '-d', action='store_true', help='Set the logging level to debug')
    parser.add_argument('fits_file', metavar='FITS FILE', help='The FITS file to submit to the SVO')
    parser.add_argument('--fits-hdu', metavar='FITS HDU', default=argparse.SUPPRESS,
                        help='The FITS HDU index or name from which to extract the metadata to submit to the SVO')
    parser.add_argument('--file-url', metavar='FILE URL', default=argparse.SUPPRESS, help='The URL of the file')
    parser.add_argument('--file-path', metavar='FILE PATH', default=argparse.SUPPRESS,
                        help='The relative path of the file')
    parser.add_argument('--thumbnail-url', metavar='THUMBNAIL URL', default=argparse.SUPPRESS,
                        help='The URL of the thumbnail')
    offline_parser = parser.add_mutually_exclusive_group(required=False)
    offline_parser.add_argument('--offline', dest='offline', default=argparse.SUPPRESS, action='store_true',
                                help='Set the record as offline')
    offline_parser.add_argument('--online', dest='offline', default=argparse.SUPPRESS, action='store_false',
                                help='Set the record as online (or not offline)')
    parser.add_argument('--dataset', default=argparse.SUPPRESS, help='The name of the dataset in the SVO')
    parser.add_argument('--oid', default=argparse.SUPPRESS, help='The unique observation ID of the metadata')
    parser.add_argument('--username', '-u', default=argparse.SUPPRESS,
                        help='The username (email) of the user owning the data')
    parser.add_argument('--api-key', '-k', default=argparse.SUPPRESS, help='The API key of the user owning the data')

    args = parser.parse_args()

    # Setup the logging
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s: %(funcName)s %(message)s')
    else:
        logging.basicConfig(level=logging.INFO, format='%(levelname)-8s: %(message)s')

    try:
        svo_record = SvoRecord(**vars(args))
        result = svo_record.create()
    except Exception as why:
        logging.critical('Could not submit data: %s', why)
        if getattr(why, 'content', False):
            logging.error(why.content)
        sys.exit(1)
    else:
        logging.info('Successfully submitted data')
        logging.debug(result)
