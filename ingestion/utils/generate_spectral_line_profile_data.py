#!/usr/bin/env python

import argparse
import datetime
import json
import os

from astropy.io import fits


def _get_datetime(ref_datetime, elapsed_seconds):
    return ref_datetime + datetime.timedelta(seconds=elapsed_seconds)


def generate_spectral_line_profile_data(fits_hdus):

    primary_hdu = fits_hdus[0]

    datamean_hdu_index = fits_hdus.index_of('VAR-EXT-DATAMEDN')
    datamean_hdu = fits_hdus[datamean_hdu_index]

    data_median_ttype = datamean_hdu.header['TTYPE1']

    data_median_values = datamean_hdu.data.field(data_median_ttype)
    data_median_values = data_median_values[0]

    scan_index = 0

    wcs_tab_hdu_index = fits_hdus.index_of('WCS-TAB')
    wcs_tab_hdu = fits_hdus[wcs_tab_hdu_index]

    # This part has been borrowed from the red_fitscube_getwcs.pro.
    tdim = wcs_tab_hdu.header['TDIM1']
    ttype = wcs_tab_hdu.header['TTYPE1']

    indices = ttype.split('+')
    coord_dims = [int(v) for v in tdim[1:-1].split(',')][1:]

    ctypes = primary_hdu.header['CTYPE*']

    TabulateHPLN = ctypes[0].endswith('-TAB')
    TabulateHPLT = ctypes[1].endswith('-TAB')
    TabulateWAVE = ctypes[2].endswith('-TAB')
    TabulateTIME = ctypes[4].endswith('-TAB')

    if TabulateHPLN:
        i_hpln = indices.index('HPLN')
    if TabulateHPLT:
        i_hplt = indices.index('HPLT')
    if TabulateWAVE:
        i_wave = indices.index('WAVE')
    if TabulateTIME:
        i_time = indices.index('TIME')
        if i_time == 3 and len(coord_dims) == 3:
            coord_dims = coord_dims + [1]

    N_hpln = coord_dims[i_hpln] if TabulateHPLN else 1
    N_hplt = coord_dims[i_hplt] if TabulateHPLT else 1
    N_wave = coord_dims[i_wave] if TabulateWAVE else 1
    N_time = coord_dims[i_time] if TabulateTIME else 1

    coord_dims = [N_hpln, N_hplt, N_wave, N_time]

    factor = 10e7

    amplitude_values = [[v[0][0] * factor for v in data_median_values[scan_index][0]] for scan_index in range(N_time)]
    amplitude_values = [[amplitude_values[j][i] for j in range(N_time)] for i in range(N_wave)]

    wcs_values = wcs_tab_hdu.data.field(ttype)[0]

    wavelength_values = [v[0][0][i_wave] for v in wcs_values[scan_index]]

    json_struct = {
        'wavelengths': wavelength_values,
        'amplitude_values': amplitude_values
    }

    return json_struct


def main():
    parser = argparse.ArgumentParser(description='Create Spectral Line Profile JSON description from FITS file.')
    parser.add_argument('fits_file', help='file to export data from')
    parser.add_argument('output', default=None, help='output JSON file')

    args = parser.parse_args()

    if not args.output:
        fits_file_path, ext = os.path.splitext(args.fits_file)
        output_file = os.path.join(fits_file_path, 'json')
    else:
        output_file = args.output

    with fits.open(args.fits_file) as fits_hdus, open(output_file, 'w') as outfile:
        data = generate_spectral_line_profile_data(fits_hdus)
        json.dump(data, outfile)


if __name__ == '__main__':
    main()
