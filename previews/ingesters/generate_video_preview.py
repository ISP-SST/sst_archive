#!/usr/bin/env python

import argparse
import os
from pathlib import Path

import ffmpeg


def generate_video_preview(preview_file, scale_x=-1, scale_y=-1, data_cube_path=None, data_cube=None, fits_hdus=None):
    if not data_cube_path and data_cube:
        data_cube_path = data_cube.path

    data_cube_path = Path(data_cube_path)

    prospective_mov = data_cube_path.with_suffix('.mov')

    if prospective_mov.exists() and prospective_mov.is_file():
        ffmpeg_stream = ffmpeg.input(prospective_mov)

        if scale_x > 0 or scale_y > 0:
            ffmpeg_stream = ffmpeg_stream.filter('scale', scale_x, scale_y)

        ffmpeg_stream = ffmpeg_stream.output(str(preview_file), vcodec='vp9').overwrite_output()
        ffmpeg_stream.run(capture_stdout=True, capture_stderr=True)
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser(description='Creates SST Archive video preview from FITS cube video.')
    parser.add_argument('image_file', help='file to export data from')
    parser.add_argument('output', default=None, help='output image file')

    args = parser.parse_args()

    if args.output:
        webm_file = args.output
    else:
        image_file_path, ext = os.path.splitext(args.image_file)
        webm_file = os.path.join(image_file_path, 'webm')

    if generate_video_preview(webm_file, data_cube_path=args.image_file):
        print('Created .webm file: %s' % webm_file)
    else:
        print('Unable to create .webm file')


if __name__ == '__main__':
    main()
