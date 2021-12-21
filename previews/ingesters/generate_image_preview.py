#!/usr/bin/env python

import argparse
import os
import subprocess
import sys
from pathlib import Path

import ffmpeg
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.visualization import astropy_mpl_style


def _get_frame_data(image_data, index, wavelength_index=0):
    frame_data = image_data[index][0][wavelength_index]
    return frame_data


def generate_new_image_preview(preview_file, wavelength_pos=0.0, data_cube_path=None, data_cube=None, fits_hdus=None):
    """
    This function provides a very simple way of generating a preview of the image data in a FITS cube.
    """

    plt.style.use(astropy_mpl_style)

    if not fits_hdus:
        if not data_cube_path and data_cube:
            data_cube_path = data_cube.path

        with fits.open(data_cube_path) as fits_hdus:
            image_data = fits_hdus[0].data
    else:
        image_data = fits_hdus[0].data

    max_wavelength_index = len(image_data[0][0]) - 1
    wavelength_index = round(max_wavelength_index * wavelength_pos)

    fig, ax = plt.subplots()

    plt.axis('off')
    plt.imshow(_get_frame_data(image_data, 0, wavelength_index))
    plt.savefig(preview_file, transparent=True)
    plt.close()


def generate_new_image_preview_in_separate_process(preview_file, data_cube_path, wavelength_pos=0.0):
    script_path = os.path.realpath(__file__)
    python_executable = sys.executable
    subprocess.check_call(
        [python_executable, script_path, data_cube_path, preview_file, '--wavelength', str(wavelength_pos)])


def generate_image_preview(preview_file, generate_if_missing=False, scale_x=-1,
                           scale_y=-1, fits_hdus=None, data_cube_path=None, data_cube=None):
    if not data_cube_path and data_cube:
        data_cube_path = data_cube.path

    data_cube_path = Path(data_cube_path)

    prospective_png = data_cube_path.with_suffix('.png')

    if prospective_png.exists() and prospective_png.is_file():
        ffmpeg_stream = ffmpeg.input(prospective_png)

        if scale_x > 0 or scale_y > 0:
            ffmpeg_stream = ffmpeg_stream.filter('scale', scale_x, scale_y)

        ffmpeg_stream = ffmpeg_stream.output(str(preview_file), vframes=1).overwrite_output()

        ffmpeg_stream.run(capture_stdout=True, capture_stderr=True)
    elif generate_if_missing:
        generate_new_image_preview_in_separate_process(preview_file, data_cube_path)


def main():
    parser = argparse.ArgumentParser(description='Create an preview image from primary FITS cube data.')
    parser.add_argument('image_file')
    parser.add_argument('output', default=None, help='output image file')
    parser.add_argument('--wavelength', type=float, default=0.0, help='Normalized wavelength position in relation to '
                                                                      'range (0.0 is the smallest wavelength, 1.0 is '
                                                                      'the largest).')

    args = parser.parse_args()

    if not args.output:
        image_file_path, ext = os.path.splitext(args.image_file)
        output_file = os.path.join(image_file_path, 'png')
    else:
        output_file = args.output

    generate_new_image_preview(output_file, data_cube_path=args.image_file, wavelength_pos=args.wavelength)


if __name__ == '__main__':
    main()
