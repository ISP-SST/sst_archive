#!/usr/bin/env python

import argparse
import os

import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import astropy_mpl_style


def _get_frame_data(image_data, index, wavelength_index=0):
    frame_data = image_data[index][0][wavelength_index]
    return frame_data


def generate_image_preview(data_cube, preview_file, wavelength_pos=0.0):
    plt.style.use(astropy_mpl_style)

    image_data = data_cube[0].data

    # FIXME(daniel): This plot does not take into consideration the WCS coordinates
    #                included in the FITS cube. Rotation and scaling is likely off.
    #                Perhaps these kinds of previews should rather be created in IDL
    #                since crispex, for example, already knows how to display the data
    #                properly.

    max_wavelength_index = len(image_data[0][0]) - 1
    wavelength_index = round(max_wavelength_index * wavelength_pos)

    fig, ax = plt.subplots()

    plt.axis('off')
    plt.imshow(_get_frame_data(image_data, 0, wavelength_index))
    plt.savefig(preview_file, transparent=True)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Export primary FITS cube data to video.')
    parser.add_argument('image_file', help='file to export data from')
    parser.add_argument('output', default=None, help='output image file')
    parser.add_argument('--wavelength-pos', type=float, default=0.0, help='normalized wavelength position (0.0 - 1.0)')

    args = parser.parse_args()

    if not args.output:
        image_file_path, ext = os.path.splitext(args.image_file)
        output_file = os.path.join(image_file_path, 'png')
    else:
        output_file = args.output

    data_cube = fits.open(args.image_file)

    generate_image_preview(data_cube, output_file, args.wavelength_pos)


if __name__ == '__main__':
    main()
