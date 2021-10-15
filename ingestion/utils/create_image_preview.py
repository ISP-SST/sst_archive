#!/usr/bin/env python

import argparse
import os
from pathlib import Path

import ffmpeg
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style


def _get_frame_data(image_data, index, wavelength_index=0):
    frame_data = image_data[index][0][wavelength_index]
    return frame_data


def generate_image_preview(fits_hdus, preview_file, wavelength_pos=0.0):
    plt.style.use(astropy_mpl_style)

    image_data = fits_hdus[0].data

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


def create_image_preview(fits_hdus, data_cube, preview_file, generate_if_missing=False, scale_x=-1,
                                               scale_y=-1):
    data_cube_path = Path(data_cube.path)

    prospective_png = data_cube_path.with_suffix('.png')

    if prospective_png.exists() and prospective_png.is_file():
        ffmpeg_stream = ffmpeg.input(prospective_png)\

        if scale_x > 0 or scale_y > 0:
            ffmpeg_stream = ffmpeg_stream.filter('scale', scale_x, scale_y)

        ffmpeg_stream = ffmpeg_stream.output(str(preview_file), vframes=1).overwrite_output()

        ffmpeg_stream.run(capture_stdout=True, capture_stderr=True)
    elif generate_if_missing:
        generate_image_preview(fits_hdus, preview_file)


def main():
    parser = argparse.ArgumentParser(description='Export primary FITS cube data to video.')
    parser.add_argument('image_file')
    parser.add_argument('output', default=None, help='output image file')
    parser.add_argument('--generate-if-missing', default=False, action='store_true')

    args = parser.parse_args()

    if not args.output:
        image_file_path, ext = os.path.splitext(args.image_file)
        output_file = os.path.join(image_file_path, 'png')
    else:
        output_file = args.output

    create_image_preview(args.image_file, output_file, generate_if_missing=args.generate_if_missing)


if __name__ == '__main__':
    main()
