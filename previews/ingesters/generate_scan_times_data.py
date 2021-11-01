#!/usr/bin/env python

import argparse
import json
import os

import datetime
from astropy.io import fits


def _get_timestamp(dt):
    return round(dt.timestamp() * 1000)


def _parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%f')
    except ValueError:
        return datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')


def _find_earliest_date(t, scan, n_wavelengths):
    earliest_date = None

    for i in range(n_wavelengths):
        date = _parse_date(t[scan][0][i][0][0])
        if not earliest_date or date < earliest_date:
            earliest_date = date

    return earliest_date


def _find_latest_date(t, scan, n_wavelengths):
    latest_date = None

    for i in range(n_wavelengths):
        date = _parse_date(t[scan][0][i][0][0])
        if not latest_date or date > latest_date:
            latest_date = date

    return latest_date


def generate_scan_times_data(fits_hdus: fits.HDUList):
    date_beg_hdu_index = fits_hdus.index_of('VAR-EXT-DATE-BEG')
    date_end_hdu_index = fits_hdus.index_of('VAR-EXT-DATE-END')
    scannum_hdu_index = fits_hdus.index_of('VAR-EXT-SCANNUM')

    date_beg_hdu = fits_hdus[date_beg_hdu_index]
    date_end_hdu = fits_hdus[date_end_hdu_index]
    scannum_hdu = fits_hdus[scannum_hdu_index]

    date_beg_field_name = date_beg_hdu.header['TTYPE1']
    date_end_field_name = date_end_hdu.header['TTYPE1']
    scannum_field_name = scannum_hdu.header['TTYPE1']

    date_beg_dims = date_beg_hdu.header['TDIM1']
    date_end_dims = date_end_hdu.header['TDIM1']

    _, _, _, n_wavelengths, _, n_scans = tuple(int(d) for d in date_beg_dims[1:-1].split(','))
    date_beg_values_all = date_beg_hdu.data.field(date_beg_field_name)[0]
    date_beg_series = [_find_earliest_date(date_beg_values_all, si, n_wavelengths) for si in range(n_scans)]

    _, _, _, n_wavelengths, _, n_scans = tuple(int(d) for d in date_end_dims[1:-1].split(','))
    date_end_values_all = date_end_hdu.data.field(date_end_field_name)[0]
    date_end_series = [_find_latest_date(date_end_values_all, si, n_wavelengths) for si in range(n_scans)]

    scannum_values_all = scannum_hdu.data.field(scannum_field_name)[0]
    scannum = [int(scannum[0][0][0][0]) for scannum in scannum_values_all]

    json_data = {
        'date_beg': [_get_timestamp(dt) for dt in date_beg_series],
        'date_end': [_get_timestamp(dt) for dt in date_end_series],
        'scannum': scannum
    }

    return json_data


def main():
    parser = argparse.ArgumentParser(description='Create scan times JSON data from FITS cube.')
    parser.add_argument('fits_file', help='file to export data from')
    parser.add_argument('output', default=None, help='output JSON file')

    args = parser.parse_args()

    if not args.output:
        image_file_path, ext = os.path.splitext(args.fits_file)
        output_file = os.path.join(image_file_path, 'json')
    else:
        output_file = args.output

    with fits.open(args.fits_file) as fits_hdus, open(output_file, 'w') as outfile:
        json.dump(generate_scan_times_data(fits_hdus), outfile)


if __name__ == '__main__':
    main()
