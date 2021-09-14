#!/usr/bin/env python

import argparse
import matplotlib
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import os
from astropy.visualization import astropy_mpl_style
from astropy.io import fits


def _get_frame_data(image_data, index):
    frame_data = image_data[index][0][0]
    return frame_data


def generate_animated_gif_preview(data_cube, gif_file):
    matplotlib.rc('font', family='sans-serif')
    matplotlib.rc('font', serif='Helvetica Neue')
    matplotlib.rc('text', usetex='false')
    matplotlib.rcParams.update({'font.size': 12})

    plt.style.use(astropy_mpl_style)

    image_data = data_cube[0].data

    # FIXME(daniel): The animated preview has the same issue with scaling/rotation as the
    #                static preview. See generate_image_preview.py.

    print('Image data shape: ')
    print(image_data.shape)

    index = 0

    fig, ax = plt.subplots()

    im = plt.imshow(_get_frame_data(image_data, index), animated=True, interpolation="nearest")

    def _update_video(index):
        print('Updating video with frame index %d' % index)
        im.set_array(_get_frame_data(image_data, index))
        return im,

    n_frames = len(image_data)
    print('Number of frames: %d' % n_frames)

    ani = animation.FuncAnimation(fig, _update_video, frames=n_frames, interval=50, blit=True, repeat_delay=2000)
    ani.save(gif_file)

    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Export primary FITS cube data to video.')
    parser.add_argument('image_file', help='file to export data from')
    parser.add_argument('output', default=None, help='output image file')

    args = parser.parse_args()

    if args.output:
        gif_file = args.output
    else:
        image_file_path, ext = os.path.splitext(args.image_file)
        gif_file = os.path.join(image_file_path, 'gif')

    data_cube = fits.open(args.image_file)

    generate_animated_gif_preview(data_cube, gif_file)


if __name__ == '__main__':
    main()
