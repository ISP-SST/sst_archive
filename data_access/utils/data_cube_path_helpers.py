import os

from django.conf import settings


def generate_absolute_path_to_data_cube(relative_path):
    # Do not allow navigation upwards in the directory tree.
    relative_path = relative_path.replace('..', '')
    return os.path.join(settings.SCIENCE_DATA_ROOT, relative_path)
