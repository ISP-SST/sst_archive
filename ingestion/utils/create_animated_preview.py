#!/usr/bin/env python

import argparse
from pathlib import Path

import ffmpeg
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import os
from astropy.visualization import astropy_mpl_style
from astropy.io import fits


def _get_frame_data(image_data, index, wavelength_index=0):
    frame_data = image_data[index][0][wavelength_index]
    return frame_data


def generate_animated_gif_preview(gif_file, wavelength_pos=0.0, data_cube_path=None, data_cube=None, fits_hdus=None):
    # FIXME(daniel): The animated preview has the same issue with scaling/rotation as the
    #                static preview. See generate_image_preview.py.

    matplotlib.rc('font', family='sans-serif')
    matplotlib.rc('font', serif='Helvetica Neue')
    matplotlib.rc('text', usetex='false')
    matplotlib.rcParams.update({'font.size': 12})

    plt.style.use(astropy_mpl_style)

    index = 0

    fig, ax = plt.subplots()

    if not fits_hdus:
        if not data_cube_path and data_cube:
            data_cube_path = data_cube.path

        with fits.open(data_cube_path) as fits_hdus:
            image_data = fits_hdus[0].data
    else:
        image_data = fits_hdus[0].data

    max_wavelength_index = len(image_data[0][0]) - 1
    wavelength_index = round(max_wavelength_index * wavelength_pos)

    im = plt.imshow(_get_frame_data(image_data, index, wavelength_index), animated=True, interpolation="nearest")

    def _update_video(index):
        print('Updating video with frame index %d' % index)
        im.set_array(_get_frame_data(image_data, index, wavelength_index))
        return im,

    n_frames = len(image_data)
    print('Number of frames: %d' % n_frames)

    ani = animation.FuncAnimation(fig, _update_video, frames=n_frames, interval=50, blit=True, repeat_delay=2000)
    ani.save(gif_file)

    plt.close()


def create_animated_preview(preview_file, generate_if_missing=False, scale_x=-1,
                                               scale_y=-1, data_cube_path=None, data_cube=None, fits_hdus=None):
    if not data_cube_path and data_cube:
        data_cube_path = data_cube.path

    data_cube_path = Path(data_cube_path)

    prospective_mov = data_cube_path.with_suffix('.mov')

    if prospective_mov.exists() and prospective_mov.is_file():
        ffmpeg_stream = ffmpeg.input(prospective_mov)

        if scale_x > 0 or scale_y > 0:
            ffmpeg_stream = ffmpeg_stream.filter('scale', scale_x, scale_y)

        ffmpeg_stream = ffmpeg_stream.output(str(preview_file)).overwrite_output()

        ffmpeg_stream.run(capture_stdout=True, capture_stderr=True)

    elif generate_if_missing:
        generate_animated_gif_preview(preview_file, data_cube_path=data_cube_path, fits_hdus=fits_hdus)


def main():
    parser = argparse.ArgumentParser(description='Export primary FITS cube data to video.')
    parser.add_argument('image_file', help='file to export data from')
    parser.add_argument('output', default=None, help='output image file')
    parser.add_argument('--wavelength-pos', type=float, default=0.0, help='normalized wavelength position (0.0 - 1.0)')

    args = parser.parse_args()

    if args.output:
        gif_file = args.output
    else:
        image_file_path, ext = os.path.splitext(args.image_file)
        gif_file = os.path.join(image_file_path, 'gif')

    create_animated_preview(gif_file, args.wavelength_pos, data_cube_path=args.image_file)


if __name__ == '__main__':
    main()
