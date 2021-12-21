#!/usr/bin/env python

import argparse
import datetime
import os
import re
import statistics
import subprocess
import sys

import matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits


def _get_datetime(ref_datetime, elapsed_seconds):
    return ref_datetime + datetime.timedelta(seconds=elapsed_seconds)


def generate_spectral_line_profile_plot(fits_hdus, plot_file, size=(4, 1)):
    hfont = {'fontname': 'Helvetica'}
    matplotlib.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})

    primary_hdu = fits_hdus[0]

    fig = plt.figure(figsize=size, tight_layout=True)

    plt.tight_layout(pad=0.2)

    marker_color = '#909090'

    ax = plt.axes(xticks=[], yticks=[])

    for spine_name in ['left', 'top', 'right', 'bottom']:
        ax.spines[spine_name].set_visible(False)

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

    n_hpln = coord_dims[i_hpln] if TabulateHPLN else 1
    n_hplt = coord_dims[i_hplt] if TabulateHPLT else 1
    n_wave = coord_dims[i_wave] if TabulateWAVE else 1
    n_time = coord_dims[i_time] if TabulateTIME else 1

    coord_dims = [n_hpln, n_hplt, n_wave, n_time]

    factor = 10e7

    amplitude_values = [[v[0][0] * factor for v in data_median_values[scan_index][0]] for scan_index in range(n_time)]
    amplitude_values = [statistics.mean([amplitude_values[scan_index][wl_index] for scan_index in range(n_time)]) for
                        wl_index in range(n_wave)]

    wcs_values = wcs_tab_hdu.data.field(ttype)[0]

    if n_time == 1:
        wavelength_values = [v[0][0][i_wave] for v in wcs_values]
    else:
        wavelength_values = [v[0][0][i_wave] for v in wcs_values[scan_index]]

    plt.plot(wavelength_values, amplitude_values, marker='o', ls='', lw=4, markerfacecolor=marker_color,
             markeredgecolor="None")

    plt.savefig(plot_file)
    plt.close()


def generate_spectral_line_profile_plot_in_separate_process(data_cube_file, output_file, size=(4, 1)):
    script_path = os.path.realpath(__file__)
    size_arg = '%dx%d' % (size[0], size[1])
    subprocess.check_call([sys.executable, script_path, data_cube_file, output_file, '--size', size_arg])


def main():
    parser = argparse.ArgumentParser(description='Create Spectral Line Profile plot from FITS file.')
    parser.add_argument('fits_file', help='file to export data from')
    parser.add_argument('output', default=None, help='output image file')
    parser.add_argument('--size', default=(4, 2), help='size of the output plot on the format <WIDTH>x<HEIGHT>')

    args = parser.parse_args()

    if not args.output:
        image_file_path, ext = os.path.splitext(args.image_file)
        output_file = os.path.join(image_file_path, 'png')
    else:
        output_file = args.output

    match = re.match(r'^(\d+)x(\d+)$', args.size)
    if not match:
        raise Exception('Size must be provided on the form <WIDTH>x<HEIGHT>. Eg: 2x4')

    size = (int(match.group(1)), int(match.group(2)))

    with fits.open(args.fits_file) as data_cube:
        generate_spectral_line_profile_plot(data_cube, output_file, size)


if __name__ == '__main__':
    main()
