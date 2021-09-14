#!/usr/bin/env python

import argparse
import os

import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import astropy_mpl_style


def generate_image_preview(data_cube, preview_file):
    plt.style.use(astropy_mpl_style)

    image_data = data_cube[0].data

    fig, ax = plt.subplots()

    plt.axis('off')
    plt.imshow(image_data[0][0][0])
    plt.savefig(preview_file, transparent=True)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Export primary FITS cube data to video.')
    parser.add_argument('image_file', help='file to export data from')
    parser.add_argument('output', default=None, help='output image file')
    args = parser.parse_args()

    if not args.output:
        image_file_path, ext = os.path.splitext(args.image_file)
        output_file = os.path.join(image_file_path, 'png')
    else:
        output_file = args.output

    data_cube = fits.open(args.image_file)

    generate_image_preview(data_cube, output_file)


if __name__ == '__main__':
    main()
