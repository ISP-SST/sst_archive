#!/usr/bin/env python

import argparse
import os

import datetime
import matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits


def _get_datetime(ref_datetime, elapsed_seconds):
    return ref_datetime + datetime.timedelta(seconds=elapsed_seconds)


def generate_r0_plot(data_cube, plot_file):
    hfont = {'fontname': 'Helvetica'}
    matplotlib.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})

    primary_hdu = data_cube[0]

    ref_datetime = datetime.datetime.fromisoformat(primary_hdu.header['DATEREF'])

    fig, ax = plt.subplots()

    hmm = plt.figure(figsize=(8,2))

    ax.grid(color='#d0d0d0', linestyle='-.', linewidth=0.7)
    ax.set_ylim(bottom=0.0, top=0.25)

    r0_hdu_index = data_cube.index_of('VAR-EXT-ATMOS_R0')
    r0_hdu = data_cube[r0_hdu_index]

    r0_field_name = r0_hdu.header['TTYPE1']

    r0_values_all = r0_hdu.data.field(r0_field_name)[0]

    r0_values_low = [v[0] for v in r0_values_all]
    r0_values_low_high = [v[1] for v in r0_values_all]
    r0_datetimes = [_get_datetime(ref_datetime, t[0]) for t in r0_hdu.data.field('TIME-ATMOS_R0')[0]]

    plt.plot(r0_datetimes, r0_values_low, label='First', lw=2, color='#33cc33')
    plt.plot(r0_datetimes, r0_values_low_high, label='Second', lw=2, color='black')
    plt.title('Atmos $r_{0}$', **hfont)

    plt.xlabel('Time', **hfont)
    plt.ylabel('$r_{0}$ (m)', **hfont)

    ax.legend()

    plt.savefig(plot_file)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Create R0 plot from FITS file.')
    parser.add_argument('fits_file', help='file to export data from')
    parser.add_argument('output', default=None, help='output image file')

    args = parser.parse_args()

    if not args.output:
        image_file_path, ext = os.path.splitext(args.image_file)
        output_file = os.path.join(image_file_path, 'png')
    else:
        output_file = args.output

    data_cube = fits.open(args.fits_file)

    generate_r0_plot(data_cube, output_file)


if __name__ == '__main__':
    main()

