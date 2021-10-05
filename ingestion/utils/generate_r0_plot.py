#!/usr/bin/env python

import argparse
import os

import datetime
import matplotlib
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import astropy_mpl_style


def _get_datetime(ref_datetime, elapsed_seconds):
    return ref_datetime + datetime.timedelta(seconds=elapsed_seconds)


def generate_r0_plot(data_cube, plot_file):
    hfont = {'fontname': 'Helvetica'}
    matplotlib.rc('font', **{'family': 'sans-serif', 'sans-serif': ['Helvetica']})

    #matplotlib.rc('font', **hfont)

    plt.style.use(astropy_mpl_style)

    phdu = data_cube[0]

    ref_datetime = datetime.datetime.fromisoformat(phdu.header['DATEREF'])

    fig, ax = plt.subplots()

    ax.grid(color='#d0d0d0', linestyle='-.', linewidth=0.7)

    r0_hdu_index = data_cube.index_of('VAR-EXT-ATMOS_R0')
    r0_hdu = data_cube[r0_hdu_index]

    r0_values_0 = [v[0] for v in r0_hdu.data.field('ATMOS_R0')[0]]
    r0_values_1 = [v[1] for v in r0_hdu.data.field('ATMOS_R0')[0]]
    r0_values_both = [(v[0], v[1]) for v in r0_hdu.data.field('ATMOS_R0')[0]]
    r0_datetimes = [_get_datetime(ref_datetime, t[0]) for t in r0_hdu.data.field('TIME-ATMOS_R0')[0]]

    #plt.plot(r0_datetimes, r0_values_0, label='0', lw=2)
    #plt.plot(r0_datetimes, r0_values_1, label='1', lw=2)
    plt.title('Atmos $r_{0}$', **hfont)

    plt.boxplot(r0_values_both)

    plt.xlabel('Time', **hfont)
    plt.ylabel('$r_{0}$ (m)', **hfont)

    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')

    plt.savefig(plot_file, dpi=600)
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

