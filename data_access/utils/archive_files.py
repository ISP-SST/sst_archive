#!/usr/bin/env python

import os
import subprocess
import uuid


def archive_files(root_dir, files):
    tmp_path = '/Users/dani2978/tmp'
    out_file = os.path.join(tmp_path, '%s.tar.gz' % uuid.uuid4())

    command = ['tar', '-czf', out_file] + files
    subprocess.run(command, check=True, cwd=root_dir)

    return out_file


def schedule_archiving_of_files(root_dir, files):
    from django_q.tasks import async_task
    return async_task(archive_files, root_dir, files)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('files', metavar='N', type=str, nargs='+',
                        help='files to compress')
    parser.add_argument('--root-dir', type=str)

    args = parser.parse_args()

    result = archive_files(args.root_dir, args.files)
    print("Archiving completed: %s" % result)
