#!/usr/bin/env python

import argparse
import os

import datetime
from astropy.io import fits


def _get_timestamp(ref_datetime, elapsed_seconds):
    dt = ref_datetime + datetime.timedelta(seconds=elapsed_seconds)
    return round(dt.timestamp() * 1000)


def generate_r0_plot_data_v1(fits_hdus: fits.header.Header):
    primary_hdu = fits_hdus[0]

    ref_datetime = datetime.datetime.fromisoformat(primary_hdu.header['DATEREF'])
    ref_datetime.replace(tzinfo=datetime.timezone.utc)

    r0_hdu_index = fits_hdus.index_of('VAR-EXT-ATMOS_R0')
    r0_hdu = fits_hdus[r0_hdu_index]

    r0_field_name = r0_hdu.header['TTYPE1']

    r0_values_all = r0_hdu.data.field(r0_field_name)[0]

    r0_values_0 = [float(v[0]) for v in r0_values_all]
    r0_values_1 = [float(v[1]) for v in r0_values_all]
    r0_timestamps = [_get_timestamp(ref_datetime, t[0]) for t in r0_hdu.data.field('TIME-ATMOS_R0')[0]]

    json_struct = {
        'r0_0': r0_values_0,
        'r0_1': r0_values_1,
        'r0_timestamps': r0_timestamps
    }

    return json_struct


def generate_r0_plot_data_v2(fits_hdus: fits.header.Header):
    primary_hdu = fits_hdus[0]

    ref_datetime = datetime.datetime.fromisoformat(primary_hdu.header['DATEREF'])
    ref_datetime.replace(tzinfo=datetime.timezone.utc)

    r0_hdu_index = fits_hdus.index_of('VAR-EXT-ATMOS_R0')
    r0_hdu = fits_hdus[r0_hdu_index]

    r0_field_name = r0_hdu.header['TTYPE1']

    r0_values_all = r0_hdu.data.field(r0_field_name)[0]

    r0_timestamps = [_get_timestamp(ref_datetime, t[0]) for t in r0_hdu.data.field('TIME-ATMOS_R0')[0]]

    r0_values_low = [[ r0_timestamps[i], float(r0_values_all[i][0])] for i in range(len(r0_values_all))]
    r0_values_low_high = [[ r0_timestamps[i], float(r0_values_all[i][1])] for i in range(len(r0_values_all))]

    json_struct = {
        'r0_low': r0_values_low,
        'r0_low_high': r0_values_low_high
    }

    return json_struct


def main():
    parser = argparse.ArgumentParser(description='Create r0 plot data JSON blob from FITS file.')
    parser.add_argument('fits_file', help='file to export data from')
    parser.add_argument('output', default=None, help='output JSON file')

    args = parser.parse_args()

    if not args.output:
        output_file = os.path.join(os.path.splitext(args.output)[0], 'json')
    else:
        output_file = args.output

    data_cube = fits.open(args.fits_file)

    json_data = generate_r0_plot_data_v1(data_cube)

    with open(output_file, 'w') as outfile:
        outfile.write(json_data)


if __name__ == '__main__':
    main()
